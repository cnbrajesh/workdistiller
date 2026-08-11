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
4. Review
5. Completed

Additional states:

- Faded
- Archived

The UI will eventually represent backlog, planning, and executing as concentric circles rather than a Kanban board. Review and completed work will be represented separately.

## Priority System

Work is prioritized using:

- Eisenhower matrix
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

- local-first data storage
- R-IDEAS item modeling
- capture from Markdown files
- simple prioritization
- aging and fading logic
- daily balanced planning
- simple review capture

The MVP does not yet include:

- full desktop attention tracking
- automatic The Brain synchronization
- advanced AI learning
- complex visual concentric UI

## Privacy Principles

This system is local-first.

It should not send private work data to external services without explicit user consent.

Attention tracking, when introduced, should capture only metadata such as app name, window title, and duration. It should not capture content by default.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
