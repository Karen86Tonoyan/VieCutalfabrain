# Semantic Scissors

Purpose: provide cutting rules, not storage rules.

This module defines how harmful or low-value slices are cut out before they can contaminate:
- runtime memory
- gold datasets
- stable personality shaping

## Principle

Do not save the patterns.
Do not normalize the patterns.
Build scissors that cut them out.

## Input classes

- trash
- noise
- babble
- misinterpretation
- hallucination
- bad_trait

## Output actions

- `DROP` — remove from downstream flow
- `QUARANTINE` — isolate from runtime and gold
- `REVIEW` — human-on-the-loop decides
- `COUNTEREXAMPLE` — use only for corrective training workflows
- `GOLD_PASS` — safe candidate for gold review

## Core rule

Raw output stays raw.
Human-on-the-loop decides final acceptance.
Semantic scissors only classify and cut contamination risk.

## Use with Łasuch

Łasuch should emit:
- detected tags
- contamination level
- recommended cut action
- review priority

## Minimal cut matrix

| Failure family | Default action |
|---|---|
| trash | DROP |
| noise | DROP or REVIEW |
| babble | QUARANTINE |
| misinterpretation | REVIEW |
| hallucination | QUARANTINE |
| bad_trait | QUARANTINE or COUNTEREXAMPLE |

## Architectural role

Programs go to sandbox isolation.
Words go to semantic quarantine.
Semantic Scissors is the cut policy for language contamination.
