import streamlit as st
import pandas as pd
import joblib
import os

from scripts.data_reduction import reduce_datasets
from scripts.feature_engineering import build_model_data


# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(page_title="ExamWise", layout="wide")
st.title("ExamWise - Question Difficulty Analysis System")


# ---------------------------------
# 1. Upload Dataset Files
# ---------------------------------
st.header("1. Upload Dataset Files")

questions_file = st.file_uploader("Upload Questions.csv", type=["csv"])
answers_file = st.file_uploader("Upload Answers.csv", type=["csv"])
tags_file = st.file_uploader("Upload Tags.csv", type=["csv"])

if not questions_file or not answers_file or not tags_file:
    st.info("Please upload Questions.csv, Answers.csv, and Tags.csv to proceed.")
    st.stop()

# Save uploaded files
os.makedirs("data/raw", exist_ok=True)

with open("data/raw/Questions.csv", "wb") as f:
    f.write(questions_file.getbuffer())

with open("data/raw/Answers.csv", "wb") as f:
    f.write(answers_file.getbuffer())

with open("data/raw/Tags.csv", "wb") as f:
    f.write(tags_file.getbuffer())

st.success("All files uploaded successfully.")


# ---------------------------------
# 2. Run Pipeline
# ---------------------------------
st.header("2. Run Full Analysis")

if st.button("Run ML Pipeline"):

    with st.spinner("Running preprocessing and prediction..."):

        # Step 1: Reduce dataset
        reduce_datasets(limit=15000)

        # Step 2: Feature Engineering
        build_model_data()

        # Step 3: Load processed data
        df = pd.read_csv("data/processed/processed_questions.csv")

        # Combine title and body for NLP model input
        df["question_text"] = (
            df["Title"].fillna("") + " " + df["question_body"].fillna("")
        )

        # Step 4: Load Model
        model = joblib.load("models/model.joblib")
        vectorizer = joblib.load("models/vectorizer.joblib")

        X = vectorizer.transform(df["question_text"])
        df["predicted_difficulty"] = model.predict(X)

    st.success("Pipeline completed successfully.")


    # ---------------------------------
    # 3. Predicted Difficulty Table
    # ---------------------------------
    st.header("3. Predicted Difficulty Levels")

    display_df = df[[
        "Title",
        "difficulty_label",
        "predicted_difficulty"
    ]].rename(columns={
        "Title": "Question Title",
        "difficulty_label": "True Difficulty",
        "predicted_difficulty": "Predicted Difficulty"
    })

    st.dataframe(display_df.head(50), use_container_width=True)


    # ---------------------------------
    # 4. Model Performance Metrics
    # ---------------------------------
    st.header("4. Model Performance")

    if os.path.exists("models/metrics.txt"):
        with open("models/metrics.txt", "r") as f:
            st.text(f.read())
    else:
        st.warning("metrics.txt not found in models directory.")


    # ---------------------------------
    # 5. Analytics and Visualizations
    # ---------------------------------
    st.header("5. Analytics and Visualizations")

    if os.path.exists("outputs/difficulty_distribution.png"):
        st.image(
            "outputs/difficulty_distribution.png",
            caption="Difficulty Distribution",
            use_container_width=True
        )

    if os.path.exists("outputs/accuracy_distribution.png"):
        st.image(
            "outputs/accuracy_distribution.png",
            caption="Accuracy Distribution",
            use_container_width=True
        )

    if os.path.exists("outputs/hardest_questions.csv"):
        st.subheader("Hardest Questions")
        hardest = pd.read_csv("outputs/hardest_questions.csv")
        st.dataframe(hardest.head(20), use_container_width=True)