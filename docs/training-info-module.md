# Training Info Module

This module is separate from runtime memory.

Its purpose is to store curated slices for training and evaluation, not direct conversational memory.

## Collections

- `error_slices`
- `manipulator_slices`
- `hallucination_slices`
- `misinterpretation_slices`
- `logic_failure_slices`
- `bad_trait_slices`
- `good_trait_slices`
- `good_answer_slices`
- `good_interpretation_slices`
- `implementation_worthy_conclusions`

## Principle

Conversation memory and training information must remain separate.

- Runtime memory stores validated, useful context.
- Training info stores labeled excerpts for fine-tuning, evaluation, and pattern detection.

## Minimal slice schema

```json
{
  "slice_id": "example_001",
  "category": "hallucination",
  "raw_excerpt": "...",
  "clean_excerpt": "...",
  "why_it_matters": "...",
  "labels": ["false_fact", "high_value"],
  "human_verified": true,
  "training_value": "high"
}
```

## Goal

Build a separate ALFA Brain training-information layer that learns from:
- errors
- manipulation patterns
- hallucinations
- logic failures
- bad traits
- good traits
- strong answers
- valuable conclusions worth implementation
