"""Grade-policy calculations for the synthetic STAT 344 course.

Keep the grading rules separate from the forecast: a model predicts future
assignment scores, whereas the policy turns those into a final course grade.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def effective_scores(gradebook: pd.DataFrame) -> pd.DataFrame:
    """Apply published penalties; assume missing=0 and omit excused work.

    The CSV's policy does not resolve missing grades, so treating missing as
    zero is a modeling assumption, not a policy fact. This is documented in
    decisions.md and should be confirmed with a real instructor.
    """
    out = gradebook.copy()
    allowed = {"submitted", "missing", "excused"}
    unknown = set(out["status"].dropna()) - allowed
    if unknown:
        raise ValueError(f"Unknown submission status: {unknown}")

    raw = 100 * out["points_earned"] / out["points_possible"]
    if not (out["points_possible"] > 0).all():
        raise ValueError("All assignments must have positive point totals")
    is_late_penalty = out["category"].isin(["homework", "project"])
    late_days = out["late_days"].fillna(0).clip(lower=0, upper=3)
    penalized = (raw - np.where(is_late_penalty, 10 * late_days, 0)).clip(0, 100)
    out["score"] = np.where(
        out["status"] == "excused",
        np.nan,
        np.where(out["status"] == "missing", 0.0, penalized),
    )
    return out


def course_grades(rows: pd.DataFrame) -> pd.Series:
    """Apply category means, allowed drops, weights, and excused exclusions.

    The input has one row per student and assignment, with an already adjusted
    ``score`` column. Drop-lowest is applied within each student/category; a
    fully excused category has its weight excluded and remaining weights are
    renormalized. This function never reads the held-out labels itself.
    """
    if rows.duplicated(["student_id", "assignment_id"]).any():
        raise ValueError("Each student-assignment pair must be unique")
    results = {}
    for student, student_rows in rows.groupby("student_id", sort=True):
        weighted_sum = 0.0
        weight_sum = 0.0
        for category, block in student_rows.groupby("category", sort=True):
            scores = block["score"].dropna().sort_values().to_numpy(dtype=float)
            if len(scores) == 0:
                continue
            if block["category_weight"].nunique() != 1:
                raise ValueError(f"Conflicting weights for category {category}")
            drops = int(block["drop_lowest"].max())
            # Drop at most n-1 so a category retains one observation.
            scores = scores[min(drops, len(scores) - 1) :]
            weight = float(block["category_weight"].iloc[0])
            weighted_sum += weight * float(scores.mean())
            weight_sum += weight
        results[student] = weighted_sum / weight_sum if weight_sum else np.nan
    return pd.Series(results, name="course_percent", dtype=float)


def future_schedule(gradebook: pd.DataFrame, cutoff_week: int) -> pd.DataFrame:
    """Build future rows using *only* known assignment schedule and weights.

    No future student points, submission statuses, or late-day values enter.
    """
    meta = ["assignment_id", "week", "category", "category_weight", "drop_lowest"]
    assignments = gradebook.loc[gradebook["week"] > cutoff_week, meta].drop_duplicates()
    students = gradebook[["student_id"]].drop_duplicates()
    return students.merge(assignments, how="cross").copy()


def projected_grades(
    observed: pd.DataFrame, schedule: pd.DataFrame, predictions: pd.Series
) -> pd.Series:
    """Combine early actual grades with future forecasts under the policy."""
    future = schedule.copy()
    if len(predictions) != len(future):
        raise ValueError("Predictions must match scheduled future rows")
    future["score"] = np.asarray(predictions, dtype=float)
    if future["score"].isna().any():
        raise ValueError("Future score predictions cannot be missing")
    return course_grades(pd.concat([observed, future], ignore_index=True))


def curve_size(course_percent: pd.Series, target_median: float) -> float:
    """Nonnegative number of points needed to reach a specified median."""
    return max(0.0, float(target_median - course_percent.median()))
