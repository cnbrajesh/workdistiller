# Prompt 03: Capture Import

Implement Markdown capture parsing in `adapters/capture_folder/parser.py`.

Requirements:

- Parse YAML frontmatter.
- Parse body text.
- Convert file into a Node.
- Support fields:
  - type
  - title
  - stage
  - quadrant
  - cognitive_load
  - deep_work
  - parent_id
  - role_ids
  - goal_ids
  - initiative_id
  - allowed_apps
  - forbidden_apps
  - importance
  - urgency
  - tags
- Use safe fallbacks when fields are missing or invalid.
- Add tests using sample files in `inbox/examples/`.
