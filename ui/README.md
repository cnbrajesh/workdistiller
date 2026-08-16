# WorkOS UI Module

Rich Concentric Circle UI implementation for WorkOS MVP.

## Files

- `concentric_circle.py` - Main UI implementation with PyQt5
- `launch.py` - Application launcher script
- `seed_sample_data.py` - Sample data seeder for testing

## Features

### Radial Visualization
- **6 Concentric Rings**: Represent workflow phases
  1. Backlog (Gray)
  2. Planning Review (Blue)
  3. Executing (Green)
  4. Waiting for inputs/Review (Yellow)
  5. Acceptance Review (Purple)
  6. Completed (Dark Green) - tasks here are hidden from view

- **4 Priority Wedges**: Eisenhower Matrix quadrants
  - Q1: Urgent & Important (Red)
  - Q2: Important, Not Urgent (Blue)
  - Q3: Urgent, Not Important (Orange)
  - Q4: Not Urgent, Not Important (Gray)

### Task Representation
- **Bubble Size**: Linear scale based on complexity (1-10)
  - Low complexity (2.0): Small bubbles
  - Medium complexity (5.0): Medium bubbles
  - High complexity (7.5): Large bubbles
  - Deep work (10.0): Largest bubbles

- **Progress Ring**: Outer ring showing task age
  - 0-30 days mapped to 0-100% progress indicator
  - Visual feedback for aging tasks

### Interactions
- **Drag & Drop**: Move tasks between phases and quadrants
  - Automatically updates task stage and quadrant
  - Saves changes to SQLite database
  
- **Click to Edit**: Opens side panel with task details
  - Edit title, description
  - Change phase, priority quadrant
  - Adjust cognitive load
  - Set complexity score (1-10 slider)

- **Panchangam Icon**: Phase 2 preview feature
  - Shows daily Vedic calendar information
  - Currently a placeholder for offline calculations

## Running the Application

```bash
# Seed sample data first
PYTHONPATH=/workspace python ui/seed_sample_data.py

# Launch the UI
PYTHONPATH=/workspace python ui/launch.py
```

## Technical Details

### Architecture
- **PyQt5 Graphics View Framework**: Custom QGraphicsItem classes
- **Polar Coordinate System**: Maps tasks to radial grid positions
- **SQLite Storage**: Local persistence via Repository pattern
- **Dark Theme**: Fusion style with custom color palette

### Key Classes
- `PhaseRing`: Draws concentric phase rings
- `QuadrantWedge`: Draws priority wedge backgrounds
- `TaskBubble`: Interactive task representation
- `RadialGridScene`: Main scene managing all items
- `TaskEditorPanel`: Side panel for editing
- `WorkOSMainWindow`: Application window

### Data Model Extensions
Added `ACCEPTANCE` stage to `core.models.Stage` enum to support the 6-phase workflow.

## Future Enhancements (Phase 2+)

- Configurable number of rings (up to 6)
- Configurable number of wedges (up to 8)
- Ring reordering via drag-drop
- Wedge reordering
- Smooth animations for transitions
- Full offline Panchangam calculations
- Multiple task stacking in same sector
- Collision avoidance algorithms
- Zoom and pan controls
