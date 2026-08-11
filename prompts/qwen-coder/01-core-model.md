# Prompt 01: Core Model

Implement the core domain model for Emperor's PoV Work OS.

Use the existing documentation in:

- docs/02-core-concepts.md
- docs/05-data-model.md

Implement Pydantic models in `core/models.py` for:

- Node
- Link
- WorkNote
- ProgressEvent
- AppSession
- Nudge
- Review
- PatternRule

Node types must include:

- role
- goal
- initiative
- deliverable
- effort
- action
- subaction
- note
- meta

Stages must include:

- backlog
- planning
- executing
- review
- completed
- faded
- archived

Priority must include Eisenhower quadrants.

Cognitive load must include:

- low
- medium
- high
- deep

Add timestamp fields for:

- created/touched
- progress
- due
- completed
- faded
- archived

Keep the model local-first and simple.
