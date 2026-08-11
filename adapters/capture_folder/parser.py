from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from core.models import (
    CognitiveLoad,
    Node,
    NodeType,
    Quadrant,
    Stage,
)


def split_frontmatter(text: str) -> tuple[Dict[str, Any], str]:
    """
    Split Markdown text into YAML frontmatter and body.
    """
    if not text.startswith("---"):
        return {}, text.strip()

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text.strip()

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        meta = {}

    body = parts[2].strip()
    return meta, body


def parse_capture_file(path: Path) -> Node:
    """
    Parse a Markdown capture file into a Node.
    """
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)

    node_type_raw = str(meta.get("type", "note")).lower()
    try:
        node_type = NodeType(node_type_raw)
    except ValueError:
        node_type = NodeType.NOTE

    stage_raw = str(meta.get("stage", "backlog")).lower()
    try:
        stage = Stage(stage_raw)
    except ValueError:
        stage = Stage.BACKLOG

    quadrant_raw = str(meta.get("quadrant", "not_urgent_important")).lower()
    try:
        quadrant = Quadrant(quadrant_raw)
    except ValueError:
        quadrant = Quadrant.NOT_URGENT_IMPORTANT

    cognitive_load_raw = str(meta.get("cognitive_load", "medium")).lower()
    try:
        cognitive_load = CognitiveLoad(cognitive_load_raw)
    except ValueError:
        cognitive_load = CognitiveLoad.MEDIUM

    title = str(meta.get("title", path.stem))

    return Node(
        type=node_type,
        title=title,
        description=body,
        stage=stage,
        quadrant=quadrant,
        cognitive_load=cognitive_load,
        deep_work=bool(meta.get("deep_work", False)),
        parent_id=meta.get("parent_id"),
        role_ids=list(meta.get("role_ids", [])),
        goal_ids=list(meta.get("goal_ids", [])),
        initiative_id=meta.get("initiative_id"),
        deliverable_id=meta.get("deliverable_id"),
        effort_id=meta.get("effort_id"),
        action_id=meta.get("action_id"),
        allowed_apps=list(meta.get("allowed_apps", [])),
        forbidden_apps=list(meta.get("forbidden_apps", [])),
        importance=float(meta.get("importance", 0.7)),
        urgency=float(meta.get("urgency", 0.3)),
        source="capture_folder",
        source_ref=str(path),
        tags=list(meta.get("tags", [])),
    )
