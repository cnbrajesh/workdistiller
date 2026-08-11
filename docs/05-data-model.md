# Data Model

The core data model is graph-like.

## Primary Node Types

- role
- goal
- initiative
- deliverable
- effort
- action
- subaction
- note
- meta

## Primary Node Fields

- id
- type
- title
- description
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
- progress
- importance
- urgency
- postpone_count
- last_touched_at
- last_progress_at
- due_at
- completed_at
- faded_at
- fulfillment_score
- source
- source_ref
- tags

## Workflow Stage

- backlog
- planning
- executing
- review
- completed
- faded
- archived

## Eisenhower Quadrant

- urgent_important
- not_urgent_important
- urgent_not_important
- not_urgent_not_important

## Cognitive Load

- low
- medium
- high
- deep

## Relationships

Relationships can be represented through parent links and explicit edge types.

Possible edge types:

- parent
- supports_goal
- fulfills_role
- belongs_to_initiative
- blocks
- related_to

## Events

The system should store events such as:

- item created
- item moved
- progress added
- item postponed
- item faded
- note added
- session started
- session ended
- nudge shown
- nudge accepted
- nudge dismissed
- review completed
