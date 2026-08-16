# Emperor's PoV Work OS

A personal work operating system based on the R-IDEAS framework.

This system is designed to support meaningful, fulfilling, and balanced work. It is not merely a task manager. It tracks roles, goals, initiatives, deliverables, efforts, actions, cognitive load, energy, attention, aging, fulfillment, and reviews.

## Core Philosophy

The purpose of this system is not to maximize task throughput.

The purpose is to:

1. Create deep, engaging, and fulfilling work.
2. Show the meaning of work, not only the count of tasks.
3. Nudge the user toward fulfillment, contentment, and sustainable energy.
4. Allow interests, roles, goals, and initiatives to fade gracefully when they are no longer alive.
5. Help the user discover and refine their Ikigai over time.

## Core Framework: R-IDEAS

R-IDEAS stands for:

- Roles
- Initiatives
- Deliverables
- Efforts
- Actions
- Sub-actions

### Progression Logic

Completing a sub-action forwards an action.  
Forwarding actions forwards efforts.  
Forwarding efforts forwards deliverables.  
Forwarding deliverables forwards initiatives.  
Fulfilling initiatives fulfills roles and supports goals.

## Workflow Stages

Work moves through:

1. Backlog
2. Planning
3. Executing
4. Review (Waiting for inputs)
5. Acceptance Review
6. Completed

Additional states:

- Faded
- Archived

The UI represents these stages as **concentric circles** with tasks shown as bubbles. The size of each bubble represents complexity, and a progress ring shows task age. Tasks can be dragged between rings and quadrants to update their phase and priority.

## Priority System

Work is prioritized using:

- Eisenhower matrix (4 quadrants as wedges in the radial UI)
- urgency
- importance
- cognitive load
- aging
- postponement decay
- completion proximity
- leverage score
- fulfillment history

## MVP Scope

The MVP focuses on:

- local-first data storage (SQLite)
- R-IDEAS item modeling
- capture from Markdown files
- simple prioritization
- aging and fading logic
- daily balanced planning
- simple review capture
- **Rich concentric-circle UI** with drag-and-drop, side panel editing, and Panchangam preview

The MVP includes:

- 6 phase rings (Backlog → Acceptance, Completed hidden)
- 4 Eisenhower quadrants as wedges
- Bubble size = complexity (linear scale)
- Progress ring = task age
- Click to edit task details
- Offline Panchangam icon (Phase 2 feature preview)

Future enhancements (Phase 2+):

- Full desktop attention tracking
- Automatic The Brain synchronization
- Advanced AI learning
- Configurable ring/wedge counts (max 6 rings, 8 wedges)
- Ring and wedge reordering
- Smooth animations
- Full offline Panchangam calculations
- Mobile app
- Cloud sync

## Privacy Principles

This system is local-first.

It should not send private work data to external services without explicit user consent.

Attention tracking, when introduced, should capture only metadata such as app name, window title, and duration. It should not capture content by default.

## Quickstart

```bash
# Create virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install PyQt5 for the UI
pip install PyQt5

# Seed sample data (optional, for testing the UI)
make seed
# or
PYTHONPATH=. python ui/seed_sample_data.py

# Launch the concentric circle UI
make ui
# or
PYTHONPATH=. python ui/launch.py
```

### Running Without Make

```bash
export PYTHONPATH=/workspace
python ui/seed_sample_data.py  # Optional: load sample tasks
python ui/launch.py            # Start the UI application
```
## UI Controls

### Navigation
- **Drag tasks** between rings to change phase
- **Drag tasks** between wedges to change priority quadrant
- **Click task** to open editor panel
- **Scroll** to zoom in/out (if enabled)

### Editor Panel
- Edit title and description
- Change phase (dropdown)
- Change priority quadrant (dropdown)
- Adjust cognitive load (Low/Medium/High/Deep)
- Set complexity score (1-10 slider)
- Save changes button

### Toolbar
- **🕉️ Panchangam**: View daily Vedic calendar (Phase 2 preview)
- **🔄 Refresh**: Reload tasks from database

## Data Model

The system uses a SQLite database with the following structure:
- `nodes` table storing all R-IDEAS items as JSON
- Stages: backlog, planning, executing, review, acceptance, completed, faded, archived
- Quadrants: urgent_important, not_urgent_important, urgent_not_important, not_urgent_not_important
- Cognitive loads: low, medium, high, deep

## File Structure

```
/workspace/
├── core/              # Core data models and storage
│   ├── models.py      # Node, Stage, Quadrant, etc.
│   └── storage.py     # SQLite repository
├── ui/                # User interface
│   ├── concentric_circle.py  # Main UI implementation
│   ├── launch.py      # Application launcher
│   ├── seed_sample_data.py   # Sample data generator
│   └── README.md      # UI documentation
├── data/              # SQLite database
│   └── workos.sqlite3
├── docs/              # Documentation
└── tests/             # Test suite
```

## License

Personal use only. All rights reserved.
