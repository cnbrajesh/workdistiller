from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List

from .models import Node


DEFAULT_DB_PATH = Path("data/workos.sqlite3")


class Repository:
    """
    Very simple SQLite repository for MVP.

    Later this can be replaced with a more structured relational schema
    or a graph database if needed.
    """

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                stage TEXT NOT NULL,
                json TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def upsert_node(self, node: Node) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO nodes (id, type, title, stage, json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                node.id,
                node.type.value,
                node.title,
                node.stage.value,
                node.model_dump_json(),
            ),
        )
        self.conn.commit()

    def get_node(self, node_id: str) -> Node | None:
        cursor = self.conn.execute(
            "SELECT json FROM nodes WHERE id = ?",
            (node_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return Node.model_validate_json(row[0])

    def all_nodes(self) -> List[Node]:
        cursor = self.conn.execute("SELECT json FROM nodes")
        rows = cursor.fetchall()
        return [Node.model_validate_json(row[0]) for row in rows]

    def delete_node(self, node_id: str) -> None:
        self.conn.execute("DELETE FROM nodes WHERE id = ?", (node_id,))
        self.conn.commit()
