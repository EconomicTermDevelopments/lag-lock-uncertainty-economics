"""
lag-lock uncertainty: computational implementation for climate economics analysis.

lag-lock uncertainty refers to the compounding uncertainty arising from temporal lags between climate policy actions and observable climate system responses, where committed future warming from past emissions (climate inertia) combines with uncertainty about threshold locations and feedback strengths to create decision-making paralysis and difficulty in attributing outcomes to specific interventions. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# lag-lock uncertainty channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "climate_inertia",  # Climate inertia captures a distinct economic channel.
    "policy_response_lag",  # Policy response lag captures a distinct economic channel.
    "threshold_uncertainty",  # Threshold uncertainty captures a distinct economic channel.
    "feedback_strength",  # Feedback strength captures a distinct economic channel.
    "attribution_noise",  # Attribution noise captures a distinct economic channel.
    "adaptation_gap",  # Adaptation gap captures a distinct economic channel.
    "monitoring_capacity",  # Monitoring capacity mitigates exposure when it is high.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "climate_inertia",
    "policy_response_lag",
    "threshold_uncertainty",
    "feedback_strength",
    "attribution_noise",
    "adaptation_gap",
    "monitoring_capacity",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "climate_inertia": 0.2,  # Climate inertia captures a distinct economic channel.
    "policy_response_lag": 0.16,  # Policy response lag captures a distinct economic channel.
    "threshold_uncertainty": 0.18,  # Threshold uncertainty captures a distinct economic channel.
    "feedback_strength": 0.14,  # Feedback strength captures a distinct economic channel.
    "attribution_noise": 0.12,  # Attribution noise captures a distinct economic channel.
    "adaptation_gap": 0.1,  # Adaptation gap captures a distinct economic channel.
    "monitoring_capacity": 0.1,  # Monitoring capacity mitigates exposure when it is high.
}


class LagLockUncertaintyCalculator:
    """
    Compute lag-lock uncertainty index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_lag_lock_uncertainty(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing lag-lock uncertainty channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["lag_lock_uncertainty_index"] = (
            + self.weights["climate_inertia"] * out["climate_inertia_norm"]
            + self.weights["policy_response_lag"] * out["policy_response_lag_norm"]
            + self.weights["threshold_uncertainty"] * out["threshold_uncertainty_norm"]
            + self.weights["feedback_strength"] * out["feedback_strength_norm"]
            + self.weights["attribution_noise"] * out["attribution_noise_norm"]
            + self.weights["adaptation_gap"] * out["adaptation_gap_norm"]
            + self.weights["monitoring_capacity"] * (1.0 - out["monitoring_capacity_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["lag_lock_uncertainty_band"] = pd.cut(
            out["lag_lock_uncertainty_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown lag-lock uncertainty channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_lag_lock_uncertainty(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("lag_lock_uncertainty_dataset.csv")
    calc = LagLockUncertaintyCalculator()
    print(calc.calculate_lag_lock_uncertainty(sample)[["lag_lock_uncertainty_index", "lag_lock_uncertainty_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="climate_inertia", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["lag_lock_uncertainty_index"].mean()))
