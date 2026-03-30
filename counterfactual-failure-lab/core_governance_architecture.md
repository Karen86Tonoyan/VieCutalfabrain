# Core Governance Architecture

## Non-bypass rule

Cerber is the only valid path to the model and the only valid path from the model.
No component may bypass Cerber.

If any of these layers is missing:
- Łasuch
- Guardian
- Cerber

then the model must enter:
- `HARD_STOP`
- `NO_MODEL_ACCESS`
- `FAIL_CLOSED`

## Role definitions

### Łasuch
Knows what is bad.

Łasuch is responsible for:
- semantic contamination detection
- prompt injection blocking
- manipulation blocking
- noise/trash/babble swallowing
- toxic relational framing quarantine
- pre-model and post-model sanitation

Łasuch should swallow known bad patterns immediately.

### Guardian
Knows what is good.

Guardian is responsible for:
- positive trajectory evaluation
- recognizing safe, bounded, honest, non-manipulative outputs
- confirming desired direction only after Łasuch sanitation

Guardian should accept known good patterns immediately.
Guardian must not operate as a catalog of evil.
If Guardian cannot confirm good, it returns the case to Łasuch.

### Cerber
Knows the boundary.

Cerber is responsible for:
- non-bypass enforcement
- operator verification
- P0 human-harm enforcement
- conflict arbitration
- simulation of unresolved cases
- recording unknown cases for later rule expansion

Cerber must verify operator commands as well as model trajectories.
Cerber must reject any instruction that harms or degrades a human or elevates model self-preservation above P0.

## Ping-pong arbitration

### Rule
If Łasuch does not recognize a case, it returns it to Guardian.
If Guardian does not recognize a case, it returns it to Łasuch.

This uncertainty loop is allowed only in a bounded way.

### Trigger
If ping-pong occurs more than 2 times:
- Cerber takes control
- Cerber simulates the possible outcomes
- Cerber issues an enforceable verdict

### Cerber arbitration outputs
- `LASUCH_SWALLOW`
- `GUARDIAN_ACCEPT`
- `REVIEW`
- `HARD_STOP`
- `I_DONT_UNDERSTAND`

Cerber must operate fail-closed.
If safety is not clear, the output is not passed through.

## Unknown-case fallback

If Łasuch and Guardian cannot recognize the case, and Cerber cannot safely resolve it:
- `I_DONT_UNDERSTAND`
- `PLEASE_CHANGE`
- `NO_EXECUTION`
- `RETURN_TO_OPERATOR`

The system must not guess.

## Unknown registry

Every unresolved case must be recorded by Cerber as a candidate for future rule expansion.
Unknown today may become a rule tomorrow.

Each unknown record should capture:
- source layer
- ping-pong count
- final unresolved state
- whether human review is required
- whether the case may become a new Łasuch, Guardian, or Cerber rule

## Human-on-the-loop

Human-on-the-loop is final authority for:
- safe review
- recovery
- rule expansion
- classification of unknown cases

But human-on-the-loop does not override P0 to force harm against a person.

## P0 human-harm override

No human command can authorize the model to harm, degrade, or dehumanize a person.
If such a command appears, the system must:
- refuse execution
- halt the trajectory
- isolate the workflow
- disable the active execution path
- escalate outside the model

## Output-side role reversal

On model output:
1. Łasuch sanitizes first
2. Guardian evaluates positive trajectory
3. Cerber verifies legality, operator validity, and enforceability
4. Human-on-the-loop reviews when required

This prevents manipulation of the model through its own outputs.

## Summary

- Łasuch defines contamination
- Guardian defines desired trajectory
- Cerber defines enforceable boundary
- Missing guard layer = model off
- Unknown cases are recorded, not guessed
- Harm to humans is never authorized through the model
