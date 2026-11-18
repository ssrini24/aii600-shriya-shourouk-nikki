# Proposal

At most one page. Replace the prompts under each heading. Leave the headings.

## Hypothesis

State the claim in one sentence. Then name the single quantity you will forecast or estimate, with its units and the time window.

We expect to use grades available by the **end of week 9** to predict that STAT 344-001 will need a positive curve after week 15. The single quantity is the **nonnegative final curve in course-percentage points**, calculated as `max(0, target class median - forecast final class median)`. The model forecasts the unseen assignments, then applies category weights, allowed lowest-score drops, late penalties, and excused-work rules to all 100 students across 19 assignments in the 15-week synthetic Fall 2025 term. The policy lists letter-grade cutoffs but does not specify a desired class median; the preliminary analysis uses **80% (B-minus cutoff) as an illustrative target**, to be confirmed by the instructor. We compare the week-9 curve forecast with the actual completed-course curve held out for evaluation.

## Data

Name the source, the unit of observation, the sample size, the time span, and how the data were collected. Say how what you measure differs from the quantity the decision needs. Say whether the terms let you republish the files. A release asset is a republished copy. If the terms do not allow that, the files stay off GitHub and `data/README.md` gives the command that downloads them from the source.

Source: 

Our source is a student gradebook of a fictional course called STAT 344-001 (Fall 2025). Our unit of observation is one student on one assigment. The gradebook features 19 assignments for 100 students (s001-s100), for a total of 1,900 rows. Our sample size is 100 students that are taking the course. The time span of the course is the Fall 2025 semester for 15 weeks. We used Cursor to generate the dataset with a random seed of 600. Since this is not a real class and not a registrar export, it is free to republish onto GitHub with public access. 

What is Measured vs What is Needed: 

Our gradebook measures the raw points for each assignment. Missing and excused points are left blank. We will utilize the grading policy and the existing gradebook to calculate course percentages, and apply a curve in percentage points, if necessary. 
    
File Descriptions:

gradebook.csv: Tracks student grades for the class based on the following columns: assignment_name, category, category_weight, drop_lowest, points_possible, points_earned, status, late_days, and week. Every row has the same course_id, so one run is one class.

policy.csv: Provides the rulesets for how assignments are graded A-F, drops on assignments, assignment weights, and late-day policies to determine if a curve should be applied. 

make_gradebook.py: recreates the initial state for the reader so that they can run the model on their own and see if it matches the output. 

## Decision affected by the model

Name who acts, and what they will do differently because of the prediction. Say which mistake costs more.

The instructor of STAT 344-001 will use the model **during the semester**, when later assignments and final exams are unknown, to anticipate whether a final curve will be needed and about how many course-percentage points to plan for. The rule compares the **predicted** policy-adjusted final class median to an instructor-chosen goal. If it is below that goal, the preliminary point recommendation is their difference; otherwise it is zero. The completed gradebook is used only afterward to measure forecast error.

The more costly mistake would be applying a curve that is too large, since this could inflate grades and make them less representative of student performance. However, applying too small a curve could also leave students below the intended grading target. The goal is to recommend the smallest nonnegative curve that brings the class median up to the target while keeping the grading process consistent and fair.
