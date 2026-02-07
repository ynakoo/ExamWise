-- System Architecture (Milestone 1) --

The system follows a modular ML and NLP pipeline designed for exam question
analytics and difficulty prediction.

-- Architecture Flow --

1. Data Layer
   - Raw Stack Overflow question and answer data
   - Processed exam-ready dataset

2. Text Preprocessing
   - Cleaning and normalization of question text

3. Feature Extraction
   - one-hot-encoding of textual features

4. Machine Learning
   - Supervised classifiers such as Knn or Decision Trees
   - Model trained using difficulty labels derived from historical data

5. Evaluation
   - Accuracy, Precision, Recall
   - Confusion Matrix

6. User Interface
   - CSV upload
   - Display of predicted difficulty and analytics

The architecture supports predictive analysis prior to exam execution and
analytical insights after exam completion.
