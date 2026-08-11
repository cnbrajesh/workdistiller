# Prompt 06: Desktop Observer

Design a privacy-first desktop observer adapter.

Do not capture content.

Capture only:

- active application name
- active window title
- start time
- end time
- active duration
- whether application is allowed for current node

Create:

- adapters/desktop_observer/active_window.py
- adapters/desktop_observer/rules.py
- adapters/desktop_observer/nudge_engine.py
- adapters/desktop_observer/app_registry.json

Rules:

- Tracking must be disabled by default.
- User must explicitly enable it.
- Sensitive apps can be excluded.
- Window titles can be redacted.
- Nudges should be questions, not punishments.

Start with interfaces and stubs. Do not implement OS-specific code fully yet.
