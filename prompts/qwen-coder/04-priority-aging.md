# Prompt 04: Priority and Aging

Implement scoring logic in `core/scoring.py` and `core/aging.py`.

Required functions:

- effective_urgency
- effective_importance
- completion_proximity
- leverage_score
- fade_risk
- should_fade

Rules:

- Important but not urgent work should become more urgent as it ages.
- Repeated postponement should reduce importance.
- Items in executing stage should fade faster than backlog if inactive.
- Completed, archived, and faded items should not fade.
- Leverage score should combine importance, urgency, completion proximity, fulfillment, and deep work value.

Add tests for each rule.
