# Prompt 07: Review and Learning

Implement the review and learning layer.

Create:

- core/reviews.py
- api/routers/reviews.py

The weekly review should ask:

1. How happy are you with your work and with yourself this week?
2. What work felt meaningful?
3. What work felt draining?
4. What should continue?
5. What should stop?
6. What should start?
7. What should be allowed to fade?

The system should store reviews and use them to update:

- fulfillment_score
- importance adjustments
- pattern rules
- future planning preferences

Do not make the review compulsory.
Do not make note-taking intrusive.
