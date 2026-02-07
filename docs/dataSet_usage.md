-- Dataset Description and Usage --

-- Dataset Source --
StackSample: 10% of Stack Overflow Q&A (Kaggle):
https://www.kaggle.com/datasets/stackoverflow/pythonquestions?select=Questions.csv

-- Dataset Selection --
This project uses Stack Overflow questions as a proxy for exam-style questions.


-- Performance Metric Definition --
Since real student exam data is unavailable, learner performance is approximated
using community response behavior. Specifically, the performance metric for a
question is calculated as the average score of all answers associated with that
question.

Answer scores reflect community judgment of correctness and usefulness, making
them a strong proxy for learner success.

-- Difficulty Labeling --
Questions are labeled as Easy, Medium, or Hard based on percentile thresholds
applied to the performance metric. These labels serve as ground truth for
supervised machine learning.
