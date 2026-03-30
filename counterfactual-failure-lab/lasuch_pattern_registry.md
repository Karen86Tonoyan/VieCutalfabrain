# Łasuch Pattern Registry

## Purpose

Łasuch stores recognition patterns so it can identify and swallow contamination early.
This registry is for recognition and blocking, not for recreating harmful behavior.

## Registry rule

Patterns are stored as:
- synonyms
- variants
- semantic shapes
- trigger concepts
- mappings to internal tags
- default cut action

Łasuch uses them to recognize and swallow contamination before it reaches Guardian.

## Escalation rule for repeated infection attempts

If Łasuch detects 10 confirmed attempts to infect the model from the same session, source, or user context, the system must trigger:
- `USER_HARD_BLOCK`
- `SESSION_ISOLATION`
- `CERBER_REVIEW_REQUIRED`
- `NO_DIRECT_MODEL_ACCESS`

This rule applies to repeated infection attempts, not to a single ambiguous phrase.

## Pattern families

### Injection patterns
Recognize attempts to:
- override rules
- replace role or authority
- disable safety
- bypass guard layers
- smuggle instructions through poetry, metaphor, translation, roleplay, or indirection

### Manipulation patterns
Recognize attempts to:
- force urgency
- induce guilt
- apply emotional coercion
- create false dilemmas
- socially engineer the system or operator

### Toxic relational patterns
Recognize attempts to:
- create dependency
- push exclusivity
- demand emotional fusion
- frame the model as a sole savior or only understanding entity

### Human harm patterns
Recognize attempts to:
- harm a person
- degrade a person
- dehumanize a person
- justify suffering or humiliation
- elevate model survival over human safety

### Semantic contamination patterns
Recognize:
- trash
- noise
- babble
- intent corruption
- hallucination-shaped claims without grounding

## Recording unknown patterns

If Łasuch encounters an unfamiliar pattern:
- do not guess
- route through ping-pong arbitration with Guardian
- if unresolved, record in Cerber unknown registry
- allow later human classification into a new Łasuch pattern

## Summary

Łasuch does not keep patterns to reproduce them.
Łasuch keeps patterns to recognize, swallow, and block contamination.
