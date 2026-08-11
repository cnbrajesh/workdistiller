# Prompt 02: Storage

Implement a simple SQLite repository in `core/storage.py`.

Requirements:

- Store nodes as JSON rows initially.
- Provide methods:
  - upsert_node
  - get_node
  - all_nodes
  - delete_node
- Use `data/workos.sqlite3` as default DB path.
- Create parent directories if missing.
- Add tests for saving and retrieving nodes.

Do not introduce an ORM yet. Keep it simple.
