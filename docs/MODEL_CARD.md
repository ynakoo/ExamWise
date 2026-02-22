# Model Card: Question Difficulty Classifier

## Model Details
- **Developer:** EPOCH PIONEERS
- **Model Type:** Logistic Regression
- **Task:** Multi-class classification of question difficulty (easy, medium, hard).
- **Features:** Question body text.
- **Vectorization:** CountVectorizer (Bag of Words) with English stop words removal.

## Performance
- **Accuracy:** 0.6571 (65.71%)
- **Test Set size:** 4500 samples (30% of processed data)

### Metrics by Class:
| Class  | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|----------|---------|
| Easy   | 0.14      | 0.10   | 0.12     | 473     |
| Medium | 0.20      | 0.15   | 0.17     | 643     |
| Hard   | 0.76      | 0.83   | 0.80     | 3384    |

> [!NOTE]
> The dataset is imbalanced towards 'hard' questions, which explains the higher performance for that class.

## Training Data
- **Source:** Stack Overflow (reduced dataset).
- **Size:** 15,000 samples initially, split 70/30 for training/testing.
- **Preprocessing:** 
  - HTML tag removal.
  - Non-alphabetical character removal.
  - Case normalization.
  - Stop words exclusion.

## Usage
The model is saved in `models/model.joblib` and the vectorizer in `models/vectorizer.joblib`.

### Reusing in the App:
```python
import joblib
import re

# Load artifacts
model = joblib.load('models/model.joblib')
vectorizer = joblib.load('models/vectorizer.joblib')

def predict_difficulty(text):
    # Basic cleaning (must match training preprocessing)
    text = re.sub('<[^>]*>', '', text)
    text = re.sub('[^a-zA-Z]', ' ', text).lower().strip()
    
    # Vectorize
    vec = vectorizer.transform([text])
    
    # Predict
    return model.predict(vec)[0]

# Example
print(predict_difficulty("How do I use a for loop in Python?"))
```

## Limitations
- Performance on 'easy' and 'medium' classes is relatively low due to class imbalance.
- The model is trained on a subset of data (15,000 rows).
- Only text features are used; other metadata (score, title) were excluded as per request.
