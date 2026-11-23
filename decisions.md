# Decisions

This file is the history of the project. Append an entry when a choice changes the work: the quantity, the data, the split, the model, the loss, or the action. Leave old entries in place. A later entry can reverse an earlier one. If a result depends on a random draw, record the seed under Why. The split entry records the cutoff date, or the seed and the fraction. The pull request that merges the code names this entry.

## YYYY-MM-DD: short title

- Decision. What you chose.
- Why. The evidence.
- Alternative. What you rejected.
- Revisit. What would change the choice.
## 2026-11-18: initial configuration

- Decision. Python 3.9.6 with pandas 2.3.3, numpy 2.0.2 and matplotlib, pinned in `requirements.txt` and `.python-version`. Each file in `data/` is checked against the SHA-256 in `data/README.md` before fitting.
- Why. Pinned versions and the hash check mean anyone who reruns the notebook gets the same code and data. All three files in `data/` (gradebook.csv, policy.csv, make_gradebook.py) are checked against their SHA-256. No result depends on a random draw, so no seed is recorded.
- Alternative. R with `renv.lock`. Rejected because the analysis is in Python.
- Revisit. If the data release changes or any SHA-256 in `data/README.md` no longer matches.

## 2026-11-18: time-based split

- Decision. Train on weeks 1–9 (1400 rows); hold out weeks 10–15 (500 rows). Cutoff: week 9, about the first 70% of weeks. Missing work counts as 0%, as in the gradebook.
- Why. The decision is about later assignments, so the held-out data has to come later in time than the training data. The split is by time, so there is no seed.
- Alternative. A random 70/30 split of rows. Rejected because it leaks later weeks into training and makes the model look more accurate than it is.
- Revisit. If the question changes to something that is not about later weeks, or the term gets more weeks of data.

## 2026-11-18: baseline

- Decision. Predict each student's held-out scores with their own average percent from the training weeks, using the class average for students with no training rows. Scored by mean absolute error (MAE) in percentage points.
- Why. Held-out MAE = 11.1 percentage points. Error is highest for final (13.9 points). It is the simplest reasonable prediction, so the model has to beat it.
- Alternative. One class-wide average for everyone (MAE 13.1) and each student's most recent score (MAE 17.3).
- Revisit. If one of the alternatives scores clearly better on the held-out weeks, or the decision's loss is not MAE.

## 2026-11-18: model

- Decision. Partial-pooling model: percent = mu + alpha[category] + theta[student] + error, with each student's ability theta shrunk toward 0 by k = n / (n + sigma^2/tau^2).
- Why. Held-out MAE = 10.7 percentage points vs. the baseline's 11.1. It adds what the baseline ignores: categories score differently, and students with few assignments shouldn't be trusted as much. 80% prediction interval about ±27.1 points, with 95% held-out coverage. Least-trusted assumption: a student's ability stays the same all term.
- Alternative. The per-student mean baseline (MAE 11.1), which treats every student's average as exact and ignores category; a regression with a time trend, not used because there are too few weeks per student to estimate one reliably.
- Revisit. If held-out coverage is far from 80%, if errors grow later in the term (a sign that ability changes over time), or if the decision needs final course grades instead of assignment scores.

## 2026-11-18: grade-policy implementation and illustrative target

- Decision. Apply `policy.csv` category weights (homework 20%, quiz 15%, midterm 20%, project 15%, final 30%), drop the lowest homework and quiz for each student, deduct 10 percentage points per late day up to 3 days on homework/projects, and exclude excused assignments. Because the policy leaves missing-work treatment unspecified, assume missing=0 for this experiment. The file has letter cutoffs but **no target-class-median field**; use an illustrative target of 80% (the B-minus cutoff), subject to instructor confirmation. If an entire category is excused, renormalize weights over the remaining categories.
- Why. The decision is a curve in **final course percentage points**, which cannot be inferred directly from raw assignment points. These rules turn the model's future assignment forecasts into 100 projected course percentages and their median. Making the missing-score and target assumptions explicit prevents mistaking them for published rules.
- Alternative. Ignoring missing/excused work or late penalties, and assuming that 80% is a mandated class target. Rejected because this would contradict or overstate the published policy. The notebook shows sensitivity to alternative targets (77% and 83%).
- Revisit. If the instructor supplies an actual target median, a different missing-work rule, or revised penalty/drop/weight definitions.

## 2026-11-18: held-out curve score and decision loss

- Decision. Keep the fixed week-9 cutoff and partial-pooling model from the earlier entries, then predict remaining assignment scores from **training data only**. Combine known scores with future forecasts and compute the final class-median shortfall under the policy. Score the curve estimate against the completed synthetic term in **absolute curve-percentage-point error**. For a provisional asymmetric decision-loss comparison, use `2 * max(predicted_curve - actual_curve, 0) + max(actual_curve - predicted_curve, 0)`, weighting overcurving twice as heavily as undercurving.
- Why. With the illustrative 80% goal, the actual final class median is **73.01%**, giving a required curve of **6.990 points**. At week 9 the student-mean baseline predicts **3.143 curve points** (absolute error **3.847**); the partial-pooling model predicts **3.203 points** (absolute error **3.787**). The model wins by only **0.060 curve points**, effectively a near-tie. Revised **assignment-level diagnostic** MAEs, after penalties/excused exclusions, are baseline **10.61** and model **10.25** points; earlier entries' 11.1/10.7 were historical raw-score metrics. The model's nominal 80% assignment interval covers about **94%**, too wide; this does not establish curve calibration. Only one course-level held-out outcome is available, so curve error is **not** an estimated cross-course MAE. No random draw affects these point forecasts.
- Alternative. Reporting only assignment-score MAE or assuming a single observed curve validates general performance. Rejected because the instructor acts on the **class curve**, not an individual assignment. A zero-curve baseline and different targets can be compared at the final checkpoint.
- Revisit. If other semesters become available, if loss preferences change, or if a calibrated class-curve predictive distribution is available. The current point rule `max(0, target - predicted_median)` is **not proven optimal** for the asymmetric loss; decision optimization and curve-level calibration remain for the 9 December final.

## 2026-11-22: simulation check

- Decision. Draw scores from known category means (homework 85, quiz 78, midterm 72, project 80, final 62), student sd 8, and residual sd 7, then refit the partial-pooling estimator. Predictive curve draws use seed 22 and 200 resamples of a shared student shock plus an assignment shock around the week-9 forecast.
- Why. Recovered category means miss the truth by 0.36 to 1.17 points. Subtracting 12 from every final moves only the final mean, by −12. Scoring 8% of homework as 0 and dropping 3% as excused pulls the homework mean from 85.36 to 78.07. On the 200 draws the loss picks the 1/3 quantile, 2.99 points (expected loss 1.08), over the plug-in curve of 3.20 (expected loss 1.10). The draws average 3.49, against the finished-term curve of 6.99.
- Alternative. Independent noise on each assignment, with no shared student shock. Rejected because one student's ability error hits every later assignment together, and independent noise would make the class curve look too certain.
- Revisit. If the project and final category effects can be trained, or if the loss weights change. The draws are centered on a forecast that never saw the final.
