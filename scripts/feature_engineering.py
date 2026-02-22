import pandas as pd
import numpy as np
import os

# Paths
input_path = 'data/reduced'
processed_path = 'data/processed'

if not os.path.exists(processed_path):
    os.makedirs(processed_path)

def build_model_data():
    print("Loading reduced datasets...")
    questions = pd.read_csv(os.path.join(input_path, 'Questions.csv'), encoding='latin-1')
    answers = pd.read_csv(os.path.join(input_path, 'Answers.csv'), encoding='latin-1')
    
    print("Aggregating answer statistics...")
    # Group answers by ParentId to get stats per question
    answer_stats = answers.groupby('ParentId').agg(
        max_answer_score=('Score', 'max'),
        avg_answer_score=('Score', 'mean'),
        answer_score_variance=('Score', 'var'),
        answer_count=('Score', 'count')
    ).reset_index()
    
    # Fill NaN variance with 0 (happens when there's only 1 answer)
    answer_stats['answer_score_variance'] = answer_stats['answer_score_variance'].fillna(0)
    
    print("Merging questions with answer stats...")
    # Merge questions with answer stats
    df = pd.merge(questions, answer_stats, left_on='Id', right_on='ParentId', how='left')
    
    # Fill missing answer stats (for questions with no answers in the reduced set)
    df['max_answer_score'] = df['max_answer_score'].fillna(0)
    df['avg_answer_score'] = df['avg_answer_score'].fillna(0)
    df['answer_score_variance'] = df['answer_score_variance'].fillna(0)
    df['answer_count'] = df['answer_count'].fillna(0)
    
    # Feature 7: ratio = max_answer_score / (answer_count + 1)
    df['ratio'] = df['max_answer_score'] / (df['answer_count'] + 1)
    
    print("Calculating difficulty score...")
    # target variable: difficulty_score = 1 - (max_answer_score / (max_answer_score + answer_count + 1))
    df['difficulty_score'] = 1 - (df['max_answer_score'] / (df['max_answer_score'] + df['answer_count'] + 1))
    
    print("Normalizing difficulty score...")
    # Normalize between 0 and 1
    ds_min = df['difficulty_score'].min()
    ds_max = df['difficulty_score'].max()
    if ds_max > ds_min:
        df['difficulty_score'] = (df['difficulty_score'] - ds_min) / (ds_max - ds_min)
    else:
        df['difficulty_score'] = 0.5 # Fallback if all scores are same
        
    print("Categorizing difficulty...")
    # easy, medium, hard
    def categorize(score):
        if score < 0.33:
            return 'easy'
        elif score < 0.66:
            return 'medium'
        return 'hard'
    
    df['difficulty_label'] = df['difficulty_score'].apply(categorize)
    
    # Columns to keep (Clean and Join)
    cols = ['Id', 'Score', 'Title', 'max_answer_score', 'avg_answer_score', 
            'answer_score_variance', 'answer_count', 'ratio', 'difficulty_score', 'difficulty_label']
    
    df_final = df[cols].rename(columns={'Score': 'question_score'})
    
    print(f"Saving processed data to {processed_path}...")
    df_final.to_csv(os.path.join(processed_path, 'processed_questions.csv'), index=False)
    print(f"Stats: {df_final['difficulty_label'].value_counts().to_dict()}")
    print("Done!")

if __name__ == "__main__":
    build_model_data()
