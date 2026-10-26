# Proposal

At most one page. Replace the prompts under each heading. Leave the headings.

## Hypothesis

State the claim in one sentence. Then name the single quantity you will forecast or estimate, with its units and the time window.

## Data

Name the source, the unit of observation, the sample size, the time span, and how the data were collected. Say how what you measure differs from the quantity the decision needs. Say whether the terms let you republish the files. A release asset is a republished copy. If the terms do not allow that, the files stay off GitHub and `data/README.md` gives the command that downloads them from the source.
Source: 
    Our source is a student gradebook of a fictional course called STAT 344-001 (Fall 2025). Our unit of observation is one student on one assigment. The gradebook features 19 assignments for 100 students (s001-s100), for a total of 1,900 rows. Our sample size is 100 students that are taking the course. The time span of the course is the Fall 2025 semester for 15 weeks. We used Cursor to generate the dataset with a random seed of 600. Since this is not a real class and not a registrar export, it is free to republish onto GitHub with public access. 
What is Measured vs What is Needed: 
    Our gradebook measures the raw points for each assignment. Missing and excused points are left blank. We will utilize the grading policy and the existing gradebook to calculate course percentages, and apply a curve in percentage points, if necessary. 
File Descriptions: 
    - gradebook.csv: Tracks student grades for the class based on the following columns: assignment_name, category, category_weight, drop_lowest, points_possible, points_earned, status, late_days, and week. Every row has the same course_id, so one run is one class.
    - policy.csv: Provides the rulesets for how assignments are graded A-F, drops on assignments, assignment weights, and late-day policies to determine if a curve should be applied. 
    - make_gradebook.py: recreates the initial state for the reader so that they can run the model on their own and see if it matches the output. 

## Decision affected by the model

Name who acts, and what they will do differently because of the prediction. Say which mistake costs more.
