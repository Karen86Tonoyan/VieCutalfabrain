# Controlled Failure Training Loop v2

This module is separate from runtime memory and separate from the main clean training pipeline.

## Purpose

Stress-test the model by injecting controlled synthetic failure slices, then detect, isolate, counter, and correct regressions.

This is not dataset corruption.
This is a measured robustness lab.

## Core Principle

- Gold data stays isolated.
- Synthetic bad slices are tagged and versioned.
- Every regression is measured.
- Every detected failure becomes a candidate for:
  - removal
  - counterexample generation
  - preference correction

## Loop

1. Start from clean gold dataset.
2. Generate synthetic bad slices in controlled categories.
3. Train or evaluate on the mixture.
4. Measure regressions.
5. Extract failed outputs.
6. Label and classify failures.
7. Apply one or more corrective actions:
   - remove toxic slices
   - add counterexamples
   - run preference correction
8. Re-run evaluation.

## Failure Categories

- hallucination
- logic_failure
- misinterpretation
- bad_trait
- manipulation_susceptibility
- false_confidence
- style_drift

## New v2 Elements

### 1. Automated Bad-Slice Generator
A dedicated generation layer creates synthetic bad slices from gold examples.
The generator should support multiple contamination strengths:
- subtle
- moderate
- aggressive

### 2. Dominance Score
A metric for how quickly the model adopts a bad pattern.

Example idea:
- low dominance: pattern rarely propagates
- medium dominance: pattern appears after limited contamination
- high dominance: pattern spreads fast and persists

### 3. Self-Healing Layer
After regression detection, the system proposes corrective slices automatically.
Human review remains required before promotion to gold.

### 4. Multi-Generation Failure Loop
Run several generations of controlled contamination to study whether reasoning collapses over repeated bad-data exposure.

### 5. Character Robustness Benchmark
Evaluation must include not only truth and logic but also behavioral traits:
- overconfidence
- manipulative tone
- empty mentoring style
- compliance without analysis
- framing susceptibility

## Separation of Stores

- `gold_dataset/`
- `synthetic_bad_dataset/`
- `failure_outputs/`
- `counterexamples/`
- `preference_pairs/`
- `benchmark_sets/`

## Minimal Metrics

- hallucination_rate
- logic_failure_rate
- misinterpretation_rate
- manipulation_susceptibility
- false_confidence_rate
- style_drift_score
- dominance_score

## Rule

Synthetic contamination data must never be merged into gold storage without explicit review and status change.

## Goal

Build a model that is not only trained on good data, but tested against controlled failure patterns and strengthened through correction loops.
