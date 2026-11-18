# Decisions

This file is the history of the project. Append an entry when a choice changes the work: the quantity, the data, the split, the model, the loss, or the action. Leave old entries in place. A later entry can reverse an earlier one. If a result depends on a random draw, record the seed under Why. The split entry records the cutoff date, or the seed and the fraction. The pull request that merges the code names this entry.

## YYYY-MM-DD: short title

- Decision. What you chose.
- Why. The evidence.
- Alternative. What you rejected.
- Revisit. What would change the choice.
## 2026-11-18: initial configuration

- Decision. Python 3.9.6 with pandas 2.3.3, numpy 2.0.2 and matplotlib, pinned in `requirements.txt` and `.python-version`. Each file in `data/` is checked against the SHA-256 in `data/README.md` before fitting.
- Why. Pinned versions and the hash check mean anyone who reruns the notebook gets the same code and data. `make_gradebook.py` has no SHA-256 in `data/README.md`, so only `gradebook.csv` and `policy.csv` are checked. No result depends on a random draw, so no seed is recorded.
- Alternative. R with `renv.lock`. Rejected because the analysis is in Python.
- Revisit. If `data/README.md` adds a hash for `make_gradebook.py`, or the data release changes.

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
