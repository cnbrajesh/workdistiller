# Inbox Capture Folder

This folder is used for quick capture notes.

Files can be created from:

- a laptop
- a mobile device
- a synced notepad app
- cloud storage
- manual Markdown notes

The system will parse these notes and convert them into R-IDEAS nodes.

## File Naming Convention

Recommended:

```text
YYYY-MM-DD--TYPE--short-title.md

```
```examples
2026-08-11--task--prepare-nagendra-ppt.md
2026-08-11--note--emperor-pov-graph-idea.md
2026-08-11--meta--feeling-about-nafdec.md
``` 
```yaml
---
type: task
title: Prepare presentation
stage: backlog
quadrant: important_not_urgent
cognitive_load: medium
deep_work: true
role_ids:
  - role-consultant
goal_ids:
  - goal-financial-stability
initiative_id: initiative-dr-nagendra
allowed_apps:
  - Qwen
  - Canva
  - NotebookLM
---
```
