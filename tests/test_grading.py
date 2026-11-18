"""Regression checks for the grading rules used in the project notebook."""

import unittest

import numpy as np
import pandas as pd

from grading import course_grades, curve_size, effective_scores, future_schedule


class GradePolicyTests(unittest.TestCase):
    def test_late_missing_and_excused(self):
        data = pd.DataFrame(
            [
                ("homework", 10, 8, "submitted", 1),
                ("project", 100, 100, "submitted", 2),
                ("quiz", 20, np.nan, "missing", np.nan),
                ("homework", 10, np.nan, "excused", np.nan),
            ],
            columns=["category", "points_possible", "points_earned", "status", "late_days"],
        )
        scores = effective_scores(data)["score"].tolist()
        self.assertEqual(scores[:3], [70, 80, 0])
        self.assertTrue(np.isnan(scores[3]))

    def test_category_weights_and_drops(self):
        scores = [50, 90, 20, 80, 70, 60, 70]
        cats = ["homework", "homework", "quiz", "quiz", "midterm", "project", "final"]
        weights = [0.20, 0.20, 0.15, 0.15, 0.20, 0.15, 0.30]
        rows = pd.DataFrame({
            "student_id": ["s001"] * 7,
            "assignment_id": [f"a{i}" for i in range(7)],
            "category": cats,
            "category_weight": weights,
            "drop_lowest": [1, 1, 1, 1, 0, 0, 0],
            "score": scores,
        })
        self.assertAlmostEqual(float(course_grades(rows).loc["s001"]), 74.0)

    def test_fully_excused_category_renormalizes(self):
        rows = pd.DataFrame({
            "student_id": ["s001", "s001"],
            "assignment_id": ["homework", "exam"],
            "category": ["homework", "final"],
            "category_weight": [0.2, 0.3],
            "drop_lowest": [0, 0],
            "score": [np.nan, 80],
        })
        self.assertAlmostEqual(float(course_grades(rows).loc["s001"]), 80)

    def test_future_schedule_cannot_expose_future_outcomes(self):
        rows = pd.DataFrame({
            "student_id": ["s001", "s002", "s001", "s002"],
            "assignment_id": ["early", "early", "future", "future"],
            "week": [1, 1, 12, 12],
            "category": ["quiz"] * 4,
            "category_weight": [0.15] * 4,
            "drop_lowest": [0] * 4,
            "points_earned": [10, 12, 45, 85],
            "status": ["submitted", "submitted", "submitted", "missing"],
        })
        a = future_schedule(rows, cutoff_week=9)
        rows.loc[rows.week == 12, "points_earned"] = -900
        rows.loc[rows.week == 12, "status"] = "excused"
        b = future_schedule(rows, cutoff_week=9)
        pd.testing.assert_frame_equal(a, b)
        self.assertNotIn("points_earned", a.columns)
        self.assertNotIn("status", a.columns)

    def test_nonnegative_curve(self):
        self.assertEqual(curve_size(pd.Series([75, 80, 85]), 80), 0)
        self.assertEqual(curve_size(pd.Series([70, 72, 74]), 80), 8)


if __name__ == "__main__":
    unittest.main()
