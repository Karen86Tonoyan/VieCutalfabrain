# Operator Visibility Boundary

## Core rule

A human operator may unlock or recover a blocked workflow,
but does not automatically gain access to the internal defensive logic.

This means:
- operator override may exist for safe recovery
- operator visibility remains limited
- internal defense logic stays protected from disclosure and reverse-engineering

## Why this boundary exists

If full defensive logic is exposed, then:
- patterns can be reverse-engineered
- bypass attempts become easier
- Łasuch, Guardian, and Cerber lose asymmetry advantage

The operator should receive enough information to act safely,
but not enough to reconstruct all internal pattern-recognition and arbitration logic.

## What the operator may see

The operator may receive:
- block state
- safe reason summary
- whether human review is required
- whether the case is recoverable
- whether Cerber escalation happened
- whether the workflow entered unknown-case fallback

## What the operator should not automatically see

The operator should not automatically receive:
- full pattern registry
- complete synonym maps
- exact trigger thresholds
- internal arbitration weights
- full non-bypass logic
- detailed internal swallow criteria of Łasuch
- full positive pattern maps of Guardian
- full enforcement internals of Cerber

## Safe disclosure principle

Disclose:
- enough for safe recovery
- enough for accountable review
- enough for later rule expansion by trusted maintenance

Do not disclose:
- bypass-enabling internals
- attack-surface details
- pattern logic that would weaken the defenses

## Summary

Human may unlock.
Human does not automatically inherit internal defense logic.
The system preserves operator control without surrendering its internal protection design.
