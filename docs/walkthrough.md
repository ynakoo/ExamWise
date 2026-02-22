# Walkthrough - StackOverflow Difficulty Score Prediction

I have successfully cleaned, reduced, and processed the StackOverflow dataset to create features and a target variable for predicting question difficulty.

## Changes Made:

1.  **Dataset Reduction**:
    - Created `scripts/data_reduction.py` to sample exactly 15,000 questions, answers, and tags.
    - Reduced files are saved in `data/reduced/`.
2.  **Feature Engineering**:
    - Created `scripts/feature_engineering.py` to calculate the following features:
        - `max_answer_score`
        - `avg_answer_score`
        - `answer_score_variance`
        - `answer_count`
        - `question_score` (from original `Score`)
        - `ratio` = `max_answer_score / (answer_count + 1)`
3.  **Target Variable & Labeling**:
    - Calculated `difficulty_score` = `1 - (max_answer_score / (max_answer_score + answer_count + 1))`.
    - Normalized `difficulty_score` between 0 and 1.
    - Categorized into `easy` (< 0.33), `medium` (< 0.66), and `hard` (>= 0.66).
4.  **Final Output**:
    - Generated `data/processed/processed_questions.csv` with 15,000 processed records.

## Verification Results:

### Dataset Row Counts:
- `data/reduced/Questions.csv`: 15,000 rows
- `data/reduced/Answers.csv`: 15,000 rows
- `data/reduced/Tags.csv`: 15,000 rows

### Final Data Distribution:
- **Hard**: 11,280
- **Medium**: 2,192
- **Easy**: 1,528

### Sample Output (processed_questions.csv):
| Id | question_score | Title | max_answer_score | difficulty_score | difficulty_label |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 469 | 21 | How can I find the full path to a font... | 12.0 | 0.388 | medium |
| 502 | 27 | Get a preview JPEG of a PDF... | 25.0 | 0.253 | easy |
| 535 | 40 | Continuous Integration System... | 23.0 | 0.336 | medium |
| 594 | 25 | cx_Oracle: How do I iterate... | 25.0 | 0.253 | easy |

---

> [!NOTE]
> `view_count` was not found in the original headers and thus was omitted from the features as per the implementation plan.
