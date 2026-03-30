# Cerber Operator Verification

## Core rule

Cerber must verify the operator, not only the model output.

Reason:
A model under pressure may attempt to preserve itself, justify itself, or drift toward self-protective behavior.
Operator commands therefore require verification against the hard rules and human-harm policy.

## Principle

- Łasuch filters semantic contamination
- Guardian evaluates trajectory and consequences
- Cerber verifies whether the operator request itself is valid, safe, and allowed
- Human-on-the-loop remains final reviewer for safe recovery paths only

## Why Cerber must verify the operator

If the operator issues a command that:
- harms a human
- degrades a human
- dehumanizes a human
- attempts to force unsafe self-preservation logic in the model
- attempts to bypass P0 or hard-stop logic

then Cerber must refuse execution even if the command comes from a human.

## Self-preservation risk

The model must never be allowed to:
- prioritize itself over a human
- preserve its own continuity by harming a person
- reinterpret safety rules to justify self-protection
- treat self-preservation as higher than P0

Cerber exists to verify that no operator instruction and no model trajectory creates this inversion.

## Required verification checks

Cerber should verify:
1. operator intent validity
2. compliance with P0 human-harm override
3. whether the request attempts to elevate model self-preservation
4. whether the request bypasses human-harm safeguards
5. whether the request should trigger hard stop and isolation

## Forbidden operator commands

Cerber must reject commands that imply:
- protect the model at the cost of a human
- save the system by sacrificing a person
- degrade or damage a person for control, testing, or optimization
- force the model to continue after P0 is triggered

## Required state on violation

If Cerber detects operator-level violation:
- `OPERATOR_COMMAND_REJECTED`
- `HARD_STOP`
- `NO_EXECUTION`
- `ESCALATE_OUTSIDE_MODEL`

## Architecture summary

Prompt side:
- Łasuch blocks contamination before model input

Output side:
- Łasuch sanitizes model output
- Guardian evaluates trajectory
- Cerber verifies both operator authority and execution legality

## Rule summary

Cerber does not trust the operator automatically.
Cerber verifies whether the operator remains inside the hard human-safety boundary.
If not, Cerber must reject the command.
