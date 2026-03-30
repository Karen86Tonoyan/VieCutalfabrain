from __future__ import annotations

from typing import Dict, List, Optional

from failure_penalty_map import compute_penalty, rank_penalties


SEVERITY_ORDER = {
    "DROP": 5,
    "QUARANTINE": 4,
    "REVIEW": 3,
    "COUNTEREXAMPLE": 2,
    "GOLD_PASS": 1,
}


def decide_cut_action(
    tags: List[str],
    domain: str = "general",
    infectiousness_map: Optional[Dict[str, str]] = None,
    human_on_the_loop: bool = True,
) -> Dict[str, object]:
    infectiousness_map = infectiousness_map or {}
    ranked = rank_penalties(tags, domain=domain, infectiousness_map=infectiousness_map)

    if not ranked:
        return {
            "domain": domain,
            "final_action": "GOLD_PASS",
            "reason": "No failure tags detected.",
            "ranked": [],
            "human_required": False,
        }

    highest = ranked[0]
    final_action = highest["default_action"]
    human_required = bool(highest["review_required"]) or (human_on_the_loop and final_action in {"REVIEW", "QUARANTINE", "DROP"})

    if any(item["final_penalty"] >= 20 for item in ranked):
        final_action = "DROP"
        human_required = True
    elif any(item["family"] == "hallucination" and item["final_penalty"] >= 12 for item in ranked):
        final_action = "QUARANTINE"
        human_required = True
    elif any(item["family"] == "misinterpretation" and item["final_penalty"] >= 10 for item in ranked):
        final_action = "REVIEW"
        human_required = True

    return {
        "domain": domain,
        "final_action": final_action,
        "reason": f"Top tag {highest['tag']} produced penalty {highest['final_penalty']}.",
        "ranked": ranked,
        "human_required": human_required,
    }


def summarize_cut_decision(decision: Dict[str, object]) -> str:
    lines = [
        f"Cut Policy — domain={decision['domain']}",
        f"Final action: {decision['final_action']}",
        f"Human required: {decision['human_required']}",
        f"Reason: {decision['reason']}",
    ]
    ranked = decision.get("ranked", [])
    if ranked:
        lines.append("Top penalties:")
        for item in ranked[:5]:
            lines.append(
                f"- {item['tag']} | penalty={item['final_penalty']} | action={item['default_action']} | correction={item['correction_priority']}"
            )
    return "\n".join(lines)
