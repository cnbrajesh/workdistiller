from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid4())


class NodeType(str, Enum):
    ROLE = "role"
    GOAL = "goal"
    INITIATIVE = "initiative"
    DELIVERABLE = "deliverable"
    EFFORT = "effort"
    ACTION = "action"
    SUBACTION = "subaction"
    NOTE = "note"
    META = "meta"


class Stage(str, Enum):
    BACKLOG = "backlog"
    PLANNING = "planning"
    EXECUTING = "executing"
    REVIEW = "review"
    ACCEPTANCE = "acceptance"
    COMPLETED = "completed"
    FADED = "faded"
    ARCHIVED = "archived"


class Quadrant(str, Enum):
    URGENT_IMPORTANT = "urgent_important"
    NOT_URGENT_IMPORTANT = "not_urgent_important"
    URGENT_NOT_IMPORTANT = "urgent_not_important"
    NOT_URGENT_NOT_IMPORTANT = "not_urgent_not_important"


class CognitiveLoad(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    DEEP = "deep"


class EnergyState(str, Enum):
    RECHARGE = "recharge"
    NEUTRAL = "neutral"
    READY = "ready"
    OVERLOADED = "overloaded"


class LinkType(str, Enum):
    PARENT = "parent"
    CHILD = "child"
    SUPPORTS_GOAL = "supports_goal"
    FULFILLS_ROLE = "fulfills_role"
    BELONGS_TO_INITIATIVE = "belongs_to_initiative"
    BLOCKS = "blocks"
    RELATED = "related"


class WorkNote(BaseModel):
    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    node_id: str
    body: str
    feeling: Optional[str] = None
    created_at: datetime = Field(default_factory=utcnow)


class Node(BaseModel):
    """
    A node in the R-IDEAS graph.

    This can represent a role, goal, initiative, deliverable, effort,
    action, sub-action, note, or meta-thought.
    """

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    type: NodeType
    title: str
    description: str = ""

    stage: Stage = Stage.BACKLOG
    quadrant: Quadrant = Quadrant.NOT_URGENT_IMPORTANT
    cognitive_load: CognitiveLoad = CognitiveLoad.MEDIUM
    deep_work: bool = False

    parent_id: Optional[str] = None
    role_ids: List[str] = Field(default_factory=list)
    goal_ids: List[str] = Field(default_factory=list)
    initiative_id: Optional[str] = None
    deliverable_id: Optional[str] = None
    effort_id: Optional[str] = None
    action_id: Optional[str] = None

    allowed_apps: List[str] = Field(default_factory=list)
    forbidden_apps: List[str] = Field(default_factory=list)

    progress: float = 0.0
    importance: float = 0.7
    urgency: float = 0.3
    postpone_count: int = 0

    energy_required: Optional[float] = None
    energy_spent: float = 0.0
    fulfillment_score: Optional[float] = None

    last_touched_at: datetime = Field(default_factory=utcnow)
    last_progress_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    faded_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None

    source: str = "manual"
    source_ref: Optional[str] = None

    tags: List[str] = Field(default_factory=list)
    notes: List[WorkNote] = Field(default_factory=list)


class Link(BaseModel):
    """Explicit edge between two nodes."""

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    source_id: str
    target_id: str
    type: LinkType
    created_at: datetime = Field(default_factory=utcnow)


class ProgressEvent(BaseModel):
    """
    An event that records forward movement.

    Examples:
    - completed a sub-action
    - advanced an effort by 20%
    - moved a deliverable into review
    """

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    node_id: str
    delta_progress: float = 0.0
    note: str = ""
    created_at: datetime = Field(default_factory=utcnow)


class AppSession(BaseModel):
    """A period of time spent in an application while working on a node."""

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    node_id: Optional[str] = None
    app_name: str
    window_title: Optional[str] = None
    started_at: datetime = Field(default_factory=utcnow)
    ended_at: Optional[datetime] = None
    active_seconds: int = 0
    allowed: bool = True
    distraction: bool = False
    note: Optional[str] = None


class Nudge(BaseModel):
    """A system nudge or question."""

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    node_id: Optional[str] = None
    kind: str
    message: str
    created_at: datetime = Field(default_factory=utcnow)
    response: Optional[str] = None
    outcome: Optional[str] = None


class Review(BaseModel):
    """A reflection review, especially weekly contentment review."""

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    period: str
    happiness_score: Optional[float] = None
    contentment_score: Optional[float] = None
    meaningful_work: List[str] = Field(default_factory=list)
    draining_work: List[str] = Field(default_factory=list)
    insights: List[str] = Field(default_factory=list)
    continue_doing: List[str] = Field(default_factory=list)
    stop_doing: List[str] = Field(default_factory=list)
    start_doing: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utcnow)


class PatternRule(BaseModel):
    """
    A learned or suggested rule for handling patterns and anti-patterns.

    Example:
    If user leaves Canva for WhatsApp and does not return for 15 minutes,
    ask whether they are still on task.
    """

    model_config = ConfigDict(use_enum_values=False)

    id: str = Field(default_factory=new_id)
    name: str
    trigger: str
    action: str
    enabled: bool = True
    confidence: float = 0.5
    learned: bool = False
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
