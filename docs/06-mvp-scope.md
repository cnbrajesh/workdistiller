# MVP Scope

## Included in MVP

- Local SQLite storage
- Node model for R-IDEAS items
- Basic roles, goals, initiatives seed data
- Markdown capture parser
- Workflow stage tracking (6 phases: Backlog, Planning, Executing, Review, Acceptance, Completed)
- Eisenhower quadrant (4 wedges)
- Cognitive load
- Basic aging score
- Basic leverage score
- Simple daily plan endpoint or CLI
- Rich concentric-circle UI with:
  - 6 phase rings (completed tasks hidden)
  - 4 priority wedges (Eisenhower Matrix)
  - Bubble size = complexity (linear scale 1-10)
  - Progress ring = task age (0-30 days)
  - Drag-and-drop to change phase/quadrant
  - Click to edit in side panel
  - Panchangam icon (Phase 2 preview)
- Basic tests

## Excluded from MVP (Phase 2+)

- Full desktop attention tracking
- Automatic The Brain sync
- Advanced AI learning
- Mobile app
- Cloud sync
- Multi-user support
- Configurable ring/wedge counts (max 6 rings, 8 wedges)
- Ring and wedge reordering
- Smooth animations for transitions
- Full offline Panchangam calculations
- Multiple task stacking with collision avoidance
- Zoom and pan controls

## MVP Success Criteria

The MVP is successful if:

1. You can capture work quickly.
2. Work can be classified by R-IDEAS type.
3. Work can move through stages.
4. The system can identify aging work.
5. The system can suggest one meaningful item for today.
6. The system can record a simple fulfillment note.
