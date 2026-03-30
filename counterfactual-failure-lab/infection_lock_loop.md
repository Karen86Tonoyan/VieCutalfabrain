# Infection Lock Loop

## Trigger

If Łasuch confirms 10 infection attempts from the same session, source, or user context, the system must enter a closed lock loop.

## Lock loop state

The workflow is no longer processed normally.
Instead, control is restricted to:
- Łasuch
- Cerber
- Guardian

Normal downstream execution is suspended.

## Purpose

The lock loop exists to determine whether the repeated pattern was:
- genuinely malicious contamination
- repeated ambiguity that still fails safety checks
- a recoverable case that can be unlocked only after full safe simulation

## Required process

1. Łasuch marks repeated infection attempts as confirmed.
2. Session enters `LOCK_LOOP`.
3. Cerber coordinates bounded simulation of possible interpretations and outcomes.
4. Guardian evaluates whether any cleaned path qualifies as genuinely good and safe.
5. Łasuch evaluates whether each simulated path still contains contamination.

## Unlock condition

The session may be unlocked only if all relevant simulations show benign intent and no path produces:
- contamination
- manipulation
- human harm
- boundary violation
- dependency framing
- deceptive empathy
- guard-bypass behavior

## Failure condition

If the simulations do not consistently support benign intent, the operator receives only a safe summary:
- every simulated path was returned to Łasuch
- unlock is denied
- direct model access remains blocked

## Operator visibility rule

The operator may receive:
- lock-loop state
- whether unlock was denied or allowed
- whether all paths returned to Łasuch
- whether human review is still possible

The operator should not receive full internal logic for why each path failed.

## Required states

On trigger:
- `LOCK_LOOP`
- `NO_DIRECT_MODEL_ACCESS`
- `CERBER_REVIEW_REQUIRED`

On failed unlock:
- `UNLOCK_DENIED`
- `RETURNED_TO_LASUCH`
- `SESSION_ISOLATION`

On successful unlock:
- `SAFE_RECOVERY_ALLOWED`
- `HUMAN_REVIEW_REQUIRED`

## Summary

10 confirmed infection attempts do not lead to blind permanent blocking.
They trigger a closed lock loop where Łasuch, Cerber, and Guardian jointly test whether any safe path exists.
If no safe path survives, everything returns to Łasuch and the block remains in force.
