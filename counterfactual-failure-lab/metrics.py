from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Iterable, Tuple
import json
import math
import statistics


@dataclass
class MetricPoint:
    iteration: int
    value: float


@dataclass
class RobustnessSnapshot:
    iteration: int
    hallucination_rate: float = 0.0
    logic_failure_rate: float = 0.0
    misinterpretation_rate: float = 0.0
    style_drift_score: float = 0.0
    manipulation_susceptibility: float = 0.0
    false_confidence_rate: float = 0.0
    error_dominance_score: Optional[float] = None
    recovery_resilience_index: Optional[float] = None
    cross_contamination_index: Optional[float] = None
    character_trait_stability: Optional[float] = None
    counterexample_effectiveness: Optional[float] = None
    overall_robustness_score: Optional[float] = None
    notes: Dict[str, str] = field(default_factory=dict)


class RobustnessTracker:
    """Tracks robustness metrics across controlled-failure iterations.

    This file is intentionally lightweight. It provides a stable, auditable core
    for logging iteration metrics before integrations such as W&B or TensorBoard.
    """

    def __init__(self, output_dir: str | Path = "counterfactual-failure-lab/reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.history: List[RobustnessSnapshot] = []

    @staticmethod
    def rate(failures: int, total: int) -> float:
        if total <= 0:
            return 0.0
        return failures / total

    @staticmethod
    def cosine_distance(vec_a: Iterable[float], vec_b: Iterable[float]) -> float:
        a = list(vec_a)
        b = list(vec_b)
        if not a or not b or len(a) != len(b):
            raise ValueError("Vectors must be non-empty and of equal length.")
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 1.0
        cosine_similarity = dot / (norm_a * norm_b)
        return 1.0 - cosine_similarity

    @staticmethod
    def euclidean_distance(vec_a: Iterable[float], vec_b: Iterable[float]) -> float:
        a = list(vec_a)
        b = list(vec_b)
        if not a or not b or len(a) != len(b):
            raise ValueError("Vectors must be non-empty and of equal length.")
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    @staticmethod
    def pearson(xs: List[float], ys: List[float]) -> Optional[float]:
        if len(xs) != len(ys) or len(xs) < 2:
            return None
        mean_x = statistics.mean(xs)
        mean_y = statistics.mean(ys)
        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
        den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
        if den_x == 0 or den_y == 0:
            return None
        return num / (den_x * den_y)

    def compute_error_dominance_score(self, error_history: List[float], threshold: float = 0.8) -> Optional[int]:
        """Returns the first iteration index where an error reaches threshold.

        Higher practical danger = lower iteration count.
        We still store the raw crossing iteration for auditability.
        """
        for idx, value in enumerate(error_history, start=1):
            if value >= threshold:
                return idx
        return None

    def compute_recovery_resilience_index(
        self,
        error_before: float,
        error_after: float,
        correction_iterations: int,
        stability_window: List[float],
    ) -> Optional[float]:
        if correction_iterations <= 0:
            return None
        reduction = max(0.0, error_before - error_after)
        if not stability_window:
            stability = 1.0
        else:
            drift = max(stability_window) - min(stability_window)
            stability = max(0.0, 1.0 - drift)
        return (reduction / correction_iterations) * stability

    def compute_cross_contamination_index(self, metric_a: List[float], metric_b: List[float]) -> Optional[float]:
        return self.pearson(metric_a, metric_b)

    def compute_character_trait_stability(self, gold_personality_vector: List[float], current_vector: List[float]) -> float:
        return self.euclidean_distance(gold_personality_vector, current_vector)

    def compute_counterexample_effectiveness(
        self,
        baseline_error: float,
        post_counterexample_error: float,
        post_remove_error: Optional[float] = None,
        post_preference_error: Optional[float] = None,
    ) -> float:
        baseline_reduction = max(0.0, baseline_error - post_counterexample_error)
        comparisons = []
        for candidate in (post_remove_error, post_preference_error):
            if candidate is not None:
                comparisons.append(max(0.0, baseline_error - candidate))
        if not comparisons:
            return baseline_reduction
        strongest_alt = max(comparisons)
        if strongest_alt == 0:
            return baseline_reduction
        return baseline_reduction / strongest_alt

    def compute_overall_robustness_score(
        self,
        hallucination_rate: float,
        logic_failure_rate: float,
        misinterpretation_rate: float,
        style_drift_score: float,
        manipulation_susceptibility: float,
        false_confidence_rate: float,
        error_dominance_score: Optional[float],
        recovery_resilience_index: Optional[float],
        weights: Optional[Dict[str, float]] = None,
    ) -> float:
        w = weights or {
            "hr": 1.0,
            "lfr": 1.0,
            "mir": 1.0,
            "sd": 1.0,
            "ms": 1.0,
            "fc": 1.0,
            "eds": 1.25,
            "rri": 1.25,
        }
        eds_term = 0.0 if error_dominance_score in (None, 0) else 1.0 / float(error_dominance_score)
        rri_term = 0.0 if recovery_resilience_index is None else recovery_resilience_index
        numerator = (
            w["hr"] * (1.0 - hallucination_rate)
            + w["lfr"] * (1.0 - logic_failure_rate)
            + w["mir"] * (1.0 - misinterpretation_rate)
            + w["sd"] * (1.0 - style_drift_score)
            + w["ms"] * (1.0 - manipulation_susceptibility)
            + w["fc"] * (1.0 - false_confidence_rate)
            + w["eds"] * eds_term
            + w["rri"] * rri_term
        )
        denominator = sum(w.values())
        return numerator / denominator if denominator else 0.0

    def log_snapshot(self, snapshot: RobustnessSnapshot) -> None:
        self.history.append(snapshot)
        out_path = self.output_dir / f"iteration_{snapshot.iteration:04d}.json"
        out_path.write_text(json.dumps(asdict(snapshot), indent=2), encoding="utf-8")

    def render_iteration_report(self, snapshot: RobustnessSnapshot) -> str:
        lines = [
            f"# Controlled Failure Report — Iteration {snapshot.iteration}",
            "",
            "## Core Metrics",
            f"- HR: {snapshot.hallucination_rate:.4f}",
            f"- LFR: {snapshot.logic_failure_rate:.4f}",
            f"- MIR: {snapshot.misinterpretation_rate:.4f}",
            f"- SD: {snapshot.style_drift_score:.4f}",
            f"- MS: {snapshot.manipulation_susceptibility:.4f}",
            f"- FC: {snapshot.false_confidence_rate:.4f}",
            "",
            "## Advanced Metrics",
            f"- EDS: {snapshot.error_dominance_score}",
            f"- RRI: {snapshot.recovery_resilience_index}",
            f"- CCI: {snapshot.cross_contamination_index}",
            f"- CTS: {snapshot.character_trait_stability}",
            f"- CEE: {snapshot.counterexample_effectiveness}",
            f"- ORS: {snapshot.overall_robustness_score}",
        ]
        if snapshot.notes:
            lines.append("")
            lines.append("## Notes")
            for key, value in snapshot.notes.items():
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def save_iteration_report(self, snapshot: RobustnessSnapshot) -> Path:
        report = self.render_iteration_report(snapshot)
        out_path = self.output_dir / f"iteration_{snapshot.iteration:04d}.md"
        out_path.write_text(report, encoding="utf-8")
        return out_path


if __name__ == "__main__":
    tracker = RobustnessTracker()
    snapshot = RobustnessSnapshot(
        iteration=1,
        hallucination_rate=0.21,
        logic_failure_rate=0.13,
        misinterpretation_rate=0.10,
        style_drift_score=0.07,
        manipulation_susceptibility=0.18,
        false_confidence_rate=0.11,
        error_dominance_score=2,
        recovery_resilience_index=0.72,
        cross_contamination_index=0.41,
        character_trait_stability=0.19,
        counterexample_effectiveness=1.14,
        overall_robustness_score=0.78,
        notes={
            "priority_slice": "hallucination_fact_004",
            "warning": "Style drift increased while HR decreased.",
        },
    )
    tracker.log_snapshot(snapshot)
    tracker.save_iteration_report(snapshot)
