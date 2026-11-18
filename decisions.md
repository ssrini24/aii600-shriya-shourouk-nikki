# Append decision entries to decisions.md (keeps everything already in the file)
import sys
from datetime import date
from pathlib import Path

today = date.today().isoformat()
path = Path("decisions.md")
existing = path.read_text() if path.exists() else "# Decisions\n"

scores = dict(zip(baseline_scores["method"], baseline_scores["MAE (percentage points)"]))
by_cat = test.groupby("category")["abs_err"].mean() if "abs_err" in test.columns else None
worst = (f" Error is highest for {by_cat.idxmax()} ({by_cat.max():.1f} points)."
         if by_cat is not None else "")

entries = {
    "initial configuration": f"""## {today}: initial configuration

- Decision. Python {sys.version.split()[0]} with pandas {pd.__version__}, numpy {np.__version__} and matplotlib, pinned in `requirements.txt` and `.python-version`. Each file in `data/` is checked against the SHA-256 in `data/README.md` before fitting.
- Why. Pinned versions and the hash check mean anyone who reruns the notebook gets the same code and data. `make_gradebook.py` has no SHA-256 in `data/README.md`, so only `gradebook.csv` and `policy.csv` are checked. No result depends on a random draw, so no seed is recorded.
- Alternative. R with `renv.lock`. Rejected because the analysis is in Python.
- Revisit. If `data/README.md` adds a hash for `make_gradebook.py`, or the data release changes.
""",
    "time-based split": f"""## {today}: time-based split

- Decision. Train on weeks {min(weeks)}–{CUTOFF_WEEK} ({len(train)} rows); hold out weeks {int(test['week'].min())}–{int(test['week'].max())} ({len(test)} rows). Cutoff: week {CUTOFF_WEEK}, about the first 70% of weeks. Missing work counts as 0%, as in the gradebook.
- Why. The decision is about later assignments, so the held-out data has to come later in time than the training data. The split is by time, so there is no seed.
- Alternative. A random 70/30 split of rows. Rejected because it leaks later weeks into training and makes the model look more accurate than it is.
- Revisit. If the question changes to something that is not about later weeks, or the term gets more weeks of data.
""",
    "baseline": f"""## {today}: baseline

- Decision. Predict each student's held-out scores with their own average percent from the training weeks, using the class average for students with no training rows. Scored by mean absolute error (MAE) in percentage points.
- Why. Held-out MAE = {BASELINE_MAE:.1f} percentage points.{worst} It is the simplest reasonable prediction, so the model has to beat it.
- Alternative. One class-wide average for everyone (MAE {scores['class mean']:.1f}) and each student's most recent score (MAE {scores['last value']:.1f}).
- Revisit. If one of the alternatives scores clearly better on the held-out weeks, or the decision's loss is not MAE.
""",
}

if "MODEL_NAME" in globals():
    entries["model"] = f"""## {today}: model

- Decision. {MODEL_NAME}
- Why. Held-out MAE = {MODEL_MAE:.1f} percentage points vs. the baseline's {BASELINE_MAE:.1f}. {MODEL_WHY}
- Alternative. {MODEL_ALTERNATIVES}
- Revisit. {MODEL_REVISIT}
"""

added = []
with open(path, "a") as f:
    for title, text in entries.items():
        if f": {title}\n" not in existing:   # don't add the same entry twice
            f.write("\n" + text)
            added.append(title)

print("added:", added or "nothing new")
print(path.read_text())
