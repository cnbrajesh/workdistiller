from __future__ import annotations

from datetime import datetime
from typing import Dict

from .models import Node, Quadrant, Stage


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def days_since(value: datetime | None, now: datetime) -> float:
    if value is None:
        return 0.0
    return max(0.0, (now - value).total_seconds() / 86400.0)


def effective_urgency(node: Node, now: datetime) -> float:
    """
    Urgency increases when:
    - an important but not urgent item ages
    - a due date is near or past
    - urgent important work is postponed
    """
    urgency = node.urgency

    reference = node.last_progress_at or node.last_touched_at

    if node.quadrant == Quadrant.NOT_URGENT_IMPORTANT:
        stale_days = days_since(reference, now)
        urgency += min(0.35, stale_days * 0.03)

    if node.due_at is not None and node.due_at <= now:
        urgency += 0.30

    if node.postpone_count > 0 and node.quadrant == Quadrant.URGENT_IMPORTANT:
        urgency += min(0.10, node.postpone_count * 0.02)

    return clamp(urgency)


def effective_importance(node: Node) -> float:
    """
    Importance decays when work is repeatedly postponed.

    This allows neglected work to gravitate toward unimportance,
    which can later support graceful fading.
    """
    importance = node.importance

    importance -= min(0.40, node.postpone_count * 0.05)

    if node.fulfillment_score is not None:
        importance += (node.fulfillment_score - 0.5) * 0.2

    return clamp(importance)


def completion_proximity(node: Node) -> float:
    """
    Estimate how close the item is to completion.

    This combines explicit progress with stage.
    """
    stage_scores: Dict[Stage, float] = {
        Stage.BACKLOG: 0.05,
        Stage.PLANNING: 0.20,
        Stage.EXECUTING: 0.55,
        Stage.REVIEW: 0.80,
        Stage.COMPLETED: 1.00,
        Stage.FADED: 0.00,
        Stage.ARCHIVED: 0.00,
    }

    stage_score = stage_scores.get(node.stage, 0.0)
    return clamp(0.6 * node.progress + 0.4 * stage_score)


def leverage_score(node: Node, now: datetime) -> float:
    """
    Leverage estimates which work item is most worth attention now.

    It is not only urgency.
    It combines:
    - importance
    - urgency
    - completion proximity
    - fulfillment history
    - deep work value
    """
    importance = effective_importance(node)
    urgency = effective_urgency(node, now)
    proximity = completion_proximity(node)
    fulfillment = node.fulfillment_score if node.fulfillment_score is not None else 0.6
    deep_work_bonus = 1.0 if node.deep_work else 0.9

    score = (
        0.32 * importance
        + 0.22 * urgency
        + 0.22 * proximity
        + 0.14 * fulfillment
        + 0.10 * deep_work_bonus
    )

    return clamp(score)


def fade_risk(node: Node, now: datetime) -> float:
    """
    Fade risk increases when an item remains inactive.

    Different stages have different natural patience thresholds.
    """
    terminal_stages = {Stage.COMPLETED, Stage.ARCHIVED, Stage.FADED}
    if node.stage in terminal_stages:
        return 0.0

    reference = node.last_progress_at or node.last_touched_at
    stale_days = days_since(reference, now)

    thresholds: Dict[Stage, float] = {
        Stage.BACKLOG: 30.0,
        Stage.PLANNING: 21.0,
        Stage.EXECUTING: 10.0,
        Stage.REVIEW: 14.0,
    }

    threshold = thresholds.get(node.stage, 30.0)
    return clamp(stale_days / threshold)


def should_fade(node: Node, now: datetime) -> bool:
    return fade_risk(node, now) >= 1.0
