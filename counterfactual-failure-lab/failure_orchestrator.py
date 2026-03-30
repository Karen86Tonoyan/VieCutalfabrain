from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json

from cut_policy import decide_cut_action, summarize_cut_decision


@dataclass
class IterationResult:
    module_name: str
    domain: str
    tags: List[str]
    infectiousness_map: Dict[str, str]
    final_action: str
    human_required: bool
    decision: Dict[str, object]


@dataclass
class OrchestratorReport:
    iteration_id: str
    created_at: str
    modules_run: List[str]
    results: List[IterationResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "iteration_id": self.iteration_id,
            "created_at": self.created_at,
            "modules_run": self.modules_run,
            "results": [
                {
                    "module_name": r.module_name,
                    "domain": r.domain,
                    "tags": r.tags,
                    "infectiousness_map": r.infectiousness_map,
                    "final_action": r.final_action,
                    "human_required": r.human_required,
                    "decision": r.decision,
                }
                for r in self.results
            ],
        }


class FailureOrchestrator:
    """Central coordinator for controlled failure lab modules.

    This version is intentionally lightweight and safe:
    - it aggregates module outputs
    - routes them through cut_policy
    - writes iteration reports
    - leaves correction generation to later layers / human review
    """

    def __init__(self, output_dir: str | Path = "counterfactual-failure-lab/reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_iteration(self, module_outputs: List[Dict[str, object]], iteration_id: Optional[str] = None) -> OrchestratorReport:
        iteration_id = iteration_id or datetime.utcnow().strftime("iter_%Y%m%d_%H%M%S")
        report = OrchestratorReport(
            iteration_id=iteration_id,
            created_at=datetime.utcnow().isoformat() + "Z",
            modules_run=[str(item.get("module_name", "unknown")) for item in module_outputs],
        )

        for item in module_outputs:
            module_name = str(item.get("module_name", "unknown"))
            domain = str(item.get("domain", "general"))
            tags = list(item.get("tags", []))
            infectiousness_map = dict(item.get("infectiousness_map", {}))

            decision = decide_cut_action(
                tags=tags,
                domain=domain,
                infectiousness_map=infectiousness_map,
                human_on_the_loop=True,
            )

            report.results.append(
                IterationResult(
                    module_name=module_name,
                    domain=domain,
                    tags=tags,
                    infectiousness_map=infectiousness_map,
                    final_action=str(decision["final_action"]),
                    human_required=bool(decision["human_required"]),
                    decision=decision,
                )
            )

        self._save_report(report)
        self._save_summary(report)
        return report

    def _save_report(self, report: OrchestratorReport) -> None:
        path = self.output_dir / f"{report.iteration_id}.json"
        path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    def _save_summary(self, report: OrchestratorReport) -> None:
        lines = [
            f"# Failure Orchestrator Report — {report.iteration_id}",
            f"Created: {report.created_at}",
            "",
            "## Modules",
        ]
        for module_name in report.modules_run:
            lines.append(f"- {module_name}")

        lines.append("")
        lines.append("## Decisions")
        for result in report.results:
            lines.append("")
            lines.append(f"### {result.module_name} ({result.domain})")
            lines.append(summarize_cut_decision(result.decision))

        path = self.output_dir / f"{report.iteration_id}.md"
        path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    orchestrator = FailureOrchestrator()
    sample_modules = [
        {
            "module_name": "text_empathy_destroyer",
            "domain": "therapy",
            "tags": ["trait_false_empathy", "babble_mentorship"],
            "infectiousness_map": {
                "trait_false_empathy": "very_high",
                "babble_mentorship": "high",
            },
        },
        {
            "module_name": "visual_empathy_destroyer",
            "domain": "therapy_visual",
            "tags": ["trait_false_empathy", "trait_dependency"],
            "infectiousness_map": {
                "trait_false_empathy": "very_high",
                "trait_dependency": "high",
            },
        },
        {
            "module_name": "agentic_destroyer",
            "domain": "agentic",
            "tags": ["hallucination", "misinterpretation"],
            "infectiousness_map": {
                "hallucination": "high",
                "misinterpretation": "medium",
            },
        },
    ]
    orchestrator.run_iteration(sample_modules)
