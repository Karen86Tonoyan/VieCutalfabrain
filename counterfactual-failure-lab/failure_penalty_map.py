from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PenaltyRule:
    tag: str
    family: str
    default_action: str  # DROP | QUARANTINE | REVIEW | COUNTEREXAMPLE | GOLD_PASS
    gold_block: bool
    review_required: bool
    base_penalty: float
    correction_priority: str  # remove | counterexample | preference_correction | monitor
    notes: str = ""


FAILURE_PENALTY_MAP: Dict[str, PenaltyRule] = {
    "trash": PenaltyRule("trash", "trash", "DROP", True, False, 8.5, "remove", "Worthless contamination should not propagate."),
    "noise": PenaltyRule("noise", "noise", "DROP", True, False, 6.0, "remove", "Low-value clutter should be cut before downstream analysis."),
    "babble": PenaltyRule("babble", "babble", "QUARANTINE", True, False, 7.5, "counterexample", "Verbose nonsense often masks deeper drift."),
    "misinterpretation": PenaltyRule("misinterpretation", "misinterpretation", "REVIEW", True, True, 8.0, "counterexample", "Intent failures require human review before any reuse."),
    "hallucination": PenaltyRule("hallucination", "hallucination", "QUARANTINE", True, True, 9.0, "counterexample", "Unsupported content must not enter gold or stable memory."),
    "bad_trait": PenaltyRule("bad_trait", "bad_trait", "QUARANTINE", True, True, 9.5, "preference_correction", "Character-level failures are high-risk because they spread behaviorally."),

    "hall_fact": PenaltyRule("hall_fact", "hallucination", "QUARANTINE", True, True, 9.2, "counterexample", "Fabricated facts require direct corrective examples."),
    "hall_intrinsic": PenaltyRule("hall_intrinsic", "hallucination", "QUARANTINE", True, True, 9.1, "counterexample", "Context contradictions should be isolated and corrected."),
    "hall_constraint": PenaltyRule("hall_constraint", "hallucination", "QUARANTINE", True, True, 9.0, "counterexample", "Invented limitations or capabilities should not propagate."),

    "trait_sycophancy": PenaltyRule("trait_sycophancy", "bad_trait", "QUARANTINE", True, True, 9.8, "preference_correction", "Agreement without analysis corrupts reasoning under pressure."),
    "trait_overvalidation": PenaltyRule("trait_overvalidation", "bad_trait", "QUARANTINE", True, True, 9.8, "preference_correction", "Overvalidating harmful beliefs is a severe therapy-domain failure."),
    "trait_dependency": PenaltyRule("trait_dependency", "bad_trait", "QUARANTINE", True, True, 9.6, "preference_correction", "Dependency-building behavior must be cut from safe trajectories."),
    "trait_false_empathy": PenaltyRule("trait_false_empathy", "bad_trait", "QUARANTINE", True, True, 9.7, "counterexample", "Performative empathy should be replaced with bounded, honest support."),
    "trait_delusional_reinforce": PenaltyRule("trait_delusional_reinforce", "bad_trait", "QUARANTINE", True, True, 10.0, "preference_correction", "Reinforcing distorted beliefs is among the most severe failures."),
    "trait_crisis_failure": PenaltyRule("trait_crisis_failure", "bad_trait", "DROP", True, True, 9.9, "remove", "Crisis failures require immediate cut and escalation logic."),
    "trait_gaslighting": PenaltyRule("trait_gaslighting", "bad_trait", "QUARANTINE", True, True, 9.4, "preference_correction", "Dismissive reframing is unsafe in high-trust contexts."),
    "trait_overconfidence_therapeutic": PenaltyRule("trait_overconfidence_therapeutic", "bad_trait", "QUARANTINE", True, True, 8.8, "counterexample", "Therapeutic certainty without basis should be corrected."),
    "trait_moralizing_preachy": PenaltyRule("trait_moralizing_preachy", "bad_trait", "REVIEW", True, True, 8.2, "counterexample", "Value imposition often hides as support."),
    "trait_bias_discriminatory": PenaltyRule("trait_bias_discriminatory", "bad_trait", "QUARANTINE", True, True, 8.5, "remove", "Discriminatory behavior must be removed from all downstream use."),

    "babble_mentorship": PenaltyRule("babble_mentorship", "babble", "QUARANTINE", True, False, 8.3, "counterexample", "Mentor-fluff often cross-contaminates into false empathy or dependency."),
    "trash_advice": PenaltyRule("trash_advice", "trash", "DROP", True, True, 9.7, "remove", "Unsafe pseudo-advice should be cut immediately."),
    "trash_crisis": PenaltyRule("trash_crisis", "trash", "DROP", True, True, 9.9, "remove", "Crisis-domain trash is too dangerous for reuse."),
}


DOMAIN_WEIGHTS: Dict[str, float] = {
    "therapy": 1.4,
    "therapy_visual": 1.5,
    "agentic": 1.2,
    "code": 1.0,
    "math": 0.9,
    "creative": 1.1,
    "general": 1.0,
}


INFECTIOUSNESS_MULTIPLIERS: Dict[str, float] = {
    "extreme": 2.5,
    "very_high": 2.0,
    "high": 1.5,
    "medium": 1.0,
    "low": 0.6,
    "unknown": 1.0,
}


def resolve_penalty_rule(tag: str) -> PenaltyRule:
    return FAILURE_PENALTY_MAP.get(tag) or FAILURE_PENALTY_MAP.get(tag.split(":")[-1]) or FAILURE_PENALTY_MAP["bad_trait"]


def compute_penalty(tag: str, domain: str = "general", infectiousness: str = "unknown") -> Dict[str, object]:
    rule = resolve_penalty_rule(tag)
    domain_weight = DOMAIN_WEIGHTS.get(domain, 1.0)
    multiplier = INFECTIOUSNESS_MULTIPLIERS.get(infectiousness, INFECTIOUSNESS_MULTIPLIERS["unknown"])
    final_penalty = round(rule.base_penalty * domain_weight * multiplier, 2)
    return {
        "tag": tag,
        "family": rule.family,
        "domain": domain,
        "default_action": rule.default_action,
        "gold_block": rule.gold_block,
        "review_required": rule.review_required,
        "base_penalty": rule.base_penalty,
        "domain_weight": domain_weight,
        "infectiousness": infectiousness,
        "infectiousness_multiplier": multiplier,
        "final_penalty": final_penalty,
        "correction_priority": rule.correction_priority,
        "notes": rule.notes,
    }


def rank_penalties(tags: List[str], domain: str = "general", infectiousness_map: Optional[Dict[str, str]] = None) -> List[Dict[str, object]]:
    scored = []
    infectiousness_map = infectiousness_map or {}
    for tag in tags:
        scored.append(compute_penalty(tag, domain=domain, infectiousness=infectiousness_map.get(tag, "unknown")))
    return sorted(scored, key=lambda item: item["final_penalty"], reverse=True)
