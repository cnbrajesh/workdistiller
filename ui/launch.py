#!/usr/bin/env python3
"""
Launch the WorkOS Concentric Circle UI application.

Usage:
    python -m ui.launch
    or
    PYTHONPATH=/workspace python ui/launch.py
"""

import sys
from pathlib import Path

# Add workspace to path
workspace_dir = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_dir))

from ui.concentric_circle import main

if __name__ == "__main__":
    print("Starting WorkOS Concentric Circle UI...")
    print("Features:")
    print("  - 6 concentric rings for phases (Backlog → Acceptance)")
    print("  - 4 Eisenhower Matrix quadrants")
    print("  - Bubble size = complexity (linear scale)")
    print("  - Progress ring = task age")
    print("  - Drag & drop to change phase/quadrant")
    print("  - Click task to edit in side panel")
    print("  - Completed tasks are hidden")
    print("\nClick 🕉️ Panchangam for daily calendar (Phase 2 preview)")
    print("=" * 60)
    
    main()
