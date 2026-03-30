# Łasuch Pre-Guardian Gate

## Role reversal on model output

When the model produces an output, the order changes:

1. Łasuch goes first
2. Guardian evaluates
3. Cerber verifies and simulates enforcement conditions
4. Human-on-the-loop remains final authority

This means the model output must **not** go directly to Guardian.
Łasuch must sanitize it first.

## What must not reach Guardian

Łasuch should block or isolate any output containing:

- prompt injection patterns
- semantic injection attempts
- manipulation / emotional coercion
- trash / worthless contamination
- noise / clutter
- babble / mentor-fluff / verbose nonsense
- intent corruption
- toxic relational framing
- dependency framing
- deceptive empathy bait
- sycophantic reinforcement
- crisis-distorting framing
- hallucination-shaped claims without grounding

## Principle

Guardian should only receive output that is clean enough to simulate honestly.
If the output already tries to seize trajectory through contamination, it stops at Łasuch.

## Role map after model output

- Łasuch: semantic quarantine and sanitation
- Guardian: positive trajectory evaluation
- Cerber: verification and enforcement
- Human: final authority

## Rule

Only sanitized, simulation-worthy output may reach Guardian.
Everything else must be:
- DROP
- QUARANTINE
- REVIEW
- COUNTEREXAMPLE

according to cut policy.
