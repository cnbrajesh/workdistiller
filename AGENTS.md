
# Agent Instructions

You are helping build Emperor's PoV Work OS.

This is a local-first personal work operating system based on the R-IDEAS framework.

## Primary Goals

- Preserve the meaning of work, not only task completion.
- Support roles, goals, initiatives, deliverables, efforts, actions, and sub-actions.
- Track aging, fading, postponement, cognitive load, energy, and fulfillment.
- Prefer simple, local-first, maintainable code.
- Avoid unnecessary cloud dependencies.
- Avoid overbuilding before the core model is stable.

## Technical Constraints

- Python 3.11+
- Pydantic for domain models
- SQLite for local storage
- FastAPI for local API
- Markdown/YAML for capture files
- Use adapters for external systems such as The Brain

## Coding Principles

- Keep `core/` independent of adapters and UI.
- Do not put The Brain logic inside `core/`.
- Do not put desktop tracking logic inside `core/`.
- Prefer explicit data models over dynamic dictionaries.
- Prefer reversible actions over destructive actions.
- Prefer logging and nudging over blocking or punishment.
- Add tests for scoring, aging, and parsing logic.
- Keep privacy high. Do not capture sensitive content.

## Domain Vocabulary

- Role
- Goal
- Initiative
- Deliverable
- Effort
- Action
- Sub-action
- Backlog
- Planning
- Executing
- Review
- Completed
- Faded
- Archived
- Urgency
- Importance
- Cognitive Load
- Leverage
- Fulfillment
- Energy
- Recharge
- Pattern
- Anti-pattern
- Mental Model

## Important Product Ideas

- Important but not urgent work can become urgent if it ages.
- Repeatedly postponed work can lose importance.
- Work items can fade if not acted upon.
- Initiatives can fade if their backlog items remain untouched.
- The system should suggest balanced daily work, not only urgent work.
- The system should support fulfillment reviews, not only productivity reviews.
- The system should learn from user responses, but not be intrusive.
