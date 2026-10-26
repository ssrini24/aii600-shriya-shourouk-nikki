# Data

The files the notebook reads are not committed. When the terms let you republish them, they are assets on the GitHub release tagged `data`. The release is public. When the terms let you download the files but not republish them, do not create that release. Write the command that downloads them from the source, and say what it needs (an account, a key in `.env`, a path).

`OWNER/REPO` is your fork, the form `username/aii600-final-project`. In the clone, once:

```bash
gh repo set-default OWNER/REPO
```

Create the release from the project root, after the files are in this folder:

```bash
gh release create data data/your-file.csv --repo OWNER/REPO --title "Data" --notes "See data/README.md"
```

Add every file the notebook reads. When a file changes:

```bash
gh release upload data data/your-file.csv --repo OWNER/REPO --clobber
```

On another machine:

```bash
gh release download data --dir data --repo OWNER/REPO
```

Record a SHA-256 for each file. Replacing a file with `--clobber` does not show up in git, so update the hash in the same commit:

```bash
shasum -a 256 data/your-file.csv
```

Replace the lines below.

- Source: We used Cursor to generate a Student Gradebook of a fictional course called STAT 344-001 (Fall 2025). It features 19 assignments for 100 students (s001-s100), 1,900 rows. Since this is not a real class and not a registrar export, it is free to republish onto GitHub with public access. 
- Designated Files: 
    - gradebook.csv: Tracks student grades for the class based on the following columns: assignment_name, category, category_weight, drop_lowest, points_possible, points_earned, status, late_days, and week. Every row has the same course_id, so one run is one class.
    - policy.csv: Provides the rulesets for how assignments are graded A-F, drops on assignments, assignment weights, and late-day policies to determine if a curve should be applied. 
    - make_gradebook.py: recreates the initial state for the reader so that they can run the model on their own and see if it matches the output. 
- SHA-256:
    - gradebook.csv:
    - policy.csv:
    - make_gradebook.csv: 
- Unit of observation, sample size, and time span.
Each row is one student on one assignment. 
