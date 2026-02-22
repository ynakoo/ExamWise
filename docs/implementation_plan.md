# StackOverflow Difficulty Score Prediction

This plan outlines the steps to prepare a StackOverflow dataset for predicting question difficulty scores.

## User Review Required

> [!IMPORTANT]
> The row counts in the raw datasets do not match:
> - `Questions.csv`: 19,951,745 rows
> - `Answers.csv`: 17,703,968 rows
> - `Tags.csv`: 1,885,079 rows
>
> I will reduce each dataset to approximately 15,000 rows. To maintain data integrity, I will:
> 1. Select the first 15,000 questions.
> 2. Select answers corresponding to those 15,000 questions (sampling down to 15k if there are more).
> 3. Select tags corresponding to those 15,000 questions (sampling down to 15k if there are more).

## Proposed Changes

### Data Preparation

#### [NEW] [data_reduction.py](file:///Users/ashwin/Desktop/ExamWise/scripts/data_reduction.py)
A script to reduce the raw datasets to 15,000 rows each while attempting to maintain linkages between questions, answers, and tags.

#### [NEW] [feature_engineering.py](file:///Users/ashwin/Desktop/ExamWise/scripts/feature_engineering.py)
A script to:
- Join the reduced datasets.
- Calculate metrics: `max_answer_score`, `avg_answer_score`, `answer_score_variance`, `answer_count`, `question_score`, and `ratio`.
- Calculate `difficulty_score` using the formula: `1 - (max_answer_score / (max_answer_score + answer_count + 1))`.
- Normalize `difficulty_score` between 0 and 1.
- Categorize difficulty into `easy`, `medium`, and `hard`.

### Workspace Cleanup [MODIFY]
The `data/raw` files will be replaced with their reduced versions (or backed up first).

## Verification Plan

### Automated Tests
- Run `wc -l` on the reduced files to ensure they are within the 10-15k range.
- Run a verification script `verify_metrics.py` to check if the `difficulty_score` and categories are calculated correctly for a sample of rows.

### Manual Verification
- Inspect the final `processed_questions.csv` to ensure all requested columns and labels are present.
