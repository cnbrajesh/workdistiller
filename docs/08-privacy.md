# Privacy Principles

This system is local-first.

## Core Rules

- Private data should remain on the user's machine by default.
- No external API calls should be made without explicit consent.
- Attention tracking should capture metadata only, not content.
- Window titles should be redactable.
- Sensitive folders should be excluded.
- The user should be able to disable tracking at any time.
- Reviews and feelings are private and should not be sent anywhere by default.

## Future Desktop Observer Rules

The desktop observer may capture:

- active application name
- active window title
- start time
- end time
- duration
- whether app is allowed for current task

It should not capture:

- keystrokes
- screenshots
- document contents
- browser page contents
- message contents

If the system detects possible distraction, it should ask permission before nudging, logging, or learning.
