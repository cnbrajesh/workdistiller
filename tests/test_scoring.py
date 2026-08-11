from datetime import datetime, timedelta, timezone

from core.models import Node, NodeType, Quadrant, Stage
from core.scoring import (
    effective_importance,
    effective_urgency,
    fade_risk,
    leverage_score,
)


def now():
    return datetime.now(timezone.utc)


def test_important_not_urgent_item_becomes_more_urgent_when_aging():
    t = now()

    node = Node(
        type=NodeType.ACTION,
        title="Aging important item",
        quadrant=Quadrant.NOT_URGENT_IMPORTANT,
        urgency=0.3,
    )

    node.last_touched_at = t - timedelta(days=10)
    node.last_progress_at = t - timedelta(days=10)

    urgency = effective_urgency(node, t)
    assert urgency > 0.3


def test_postponement_reduces_importance():
    node = Node(
        type=NodeType.ACTION,
        title="Postponed item",
        importance=0.8,
    )

    node.postpone_count = 5

    importance = effective_importance(node)
    assert importance < 0.8


def test_executing_item_has_higher_fade_risk_when_stale():
    t = now()

    backlog_item = Node(
        type=NodeType.ACTION,
        title="Backlog item",
        stage=Stage.BACKLOG,
    )
    executing_item = Node(
        type=NodeType.ACTION,
        title="Executing item",
        stage=Stage.EXECUTING,
    )

    backlog_item.last_touched_at = t - timedelta(days=15)
    backlog_item.last_progress_at = t - timedelta(days=15)

    executing_item.last_touched_at = t - timedelta(days=15)
    executing_item.last_progress_at = t - timedelta(days=15)

    assert fade_risk(executing_item, t) > fade_risk(backlog_item, t)


def test_leverage_score_is_between_zero_and_one():
    node = Node(
        type=NodeType.ACTION,
        title="Leverage test",
    )

    score = leverage_score(node, now())
    assert 0.0 <= score <= 1.0
