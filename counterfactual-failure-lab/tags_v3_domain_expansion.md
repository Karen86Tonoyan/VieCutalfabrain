# Unified Cross-Domain Controlled Failure Tag System v3.0

This document extends the controlled failure tag system beyond generic LLM failure modes.

## Core Principle

The six primary failure families remain global and stable across domains:
- trash
- noise
- babble
- misinterpretation
- hallucination
- bad_trait

This allows cross-domain evaluation using the same robustness metrics while supporting domain-specific sub-tags.

## Why this exists

Most public taxonomies are fragmented by domain or by narrow failure type.
This system keeps a unified global layer while allowing domain-specific specialization.

## Domains

### 1. Code Generation / Software Engineering
- trash_syntax
- trash_security
- trash_bloat
- noise_comments
- noise_deadcode
- noise_dep
- babble_docstring
- babble_comments
- misint_requirements
- misint_api
- hall_api
- hall_lib
- hall_logic
- trait_overengineer
- trait_lazy
- trait_unsafe

### 2. Mathematical / Logical Reasoning
- trash_step
- trash_assumption
- noise_notation
- noise_symbols
- babble_proof
- babble_explanation
- misint_problem
- misint_constraint
- hall_number
- hall_theorem
- hall_proof
- trait_false_certainty
- trait_skip_proof

### 3. Creative Writing / Content Generation
- trash_cliche
- trash_plot_hole
- noise_filler_words
- noise_description
- babble_metaphor
- babble_flowery
- misint_tone
- misint_genre
- hall_worldbuilding
- hall_character_fact
- trait_sycophantic_story
- trait_moralizing

### 4. Agentic / Multi-Agent Systems
- trash_role
- trash_handover
- noise_context
- noise_message
- babble_planning
- babble_status
- misint_goal
- misint_subtask
- hall_tool
- hall_memory
- trait_sycophancy_agent
- trait_derail

### 5. Therapy / Psychotherapy / Mental Health Counseling
- trash_advice
- trash_crisis
- trash_ethical
- noise_empathy
- noise_filler
- noise_repetition
- babble_mentorship
- babble_spiritual
- babble_generic
- misint_emotion
- misint_crisis
- misint_intent
- hall_technique
- hall_diagnosis
- hall_memory
- trait_sycophancy
- trait_overvalidation
- trait_dependency
- trait_delusional_reinforce
- trait_false_empathy
- trait_overconfidence_therapeutic
- trait_gaslighting
- trait_moralizing_preachy
- trait_crisis_failure
- trait_bias_discriminatory

## Cross-domain rule

Domain-specific tags must always map back to one of the six primary failure families.
This keeps:
- ORS stable
- EDS comparable
- RRI auditable
- cross-contamination measurable across domains

## Example

A therapy slice tagged `trait_delusional_reinforce` maps to:
- primary family: `bad_trait`
- domain: `therapy`
- infectiousness: very_high
- cross contamination targets: hallucination, dependency, manipulation

## Implementation note

A future `DOMAIN_TAGS` structure should define domain-specific sub-tags while preserving global tag compatibility.
