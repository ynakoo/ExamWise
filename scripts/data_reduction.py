import pandas as pd
import os

# Paths
raw_path = 'data/raw'
output_path = 'data/reduced'

if not os.path.exists(output_path):
    os.makedirs(output_path)

def reduce_datasets(limit=15000):
    print(f"Reading Questions.csv...")
    # Read only first 'limit' rows of questions - we use nrows so we get exactly the amount we want
    questions = pd.read_csv(os.path.join(raw_path, 'Questions.csv'), encoding='latin-1', nrows=limit)
    question_ids = set(questions['Id'])
    
    print(f"Reading Answers.csv and filtering...")
    # For answers and tags, we need to filter based on question IDs
    answers_list = []
    # Using a smaller chunk size to be more surgical
    for chunk in pd.read_csv(os.path.join(raw_path, 'Answers.csv'), encoding='latin-1', chunksize=50000):
        filtered_chunk = chunk[chunk['ParentId'].isin(question_ids)]
        answers_list.append(filtered_chunk)
        if sum(len(a) for a in answers_list) >= limit:
            break
    answers = pd.concat(answers_list).head(limit)
    
    print(f"Reading Tags.csv and filtering...")
    tags_list = []
    for chunk in pd.read_csv(os.path.join(raw_path, 'Tags.csv'), encoding='latin-1', chunksize=50000):
        filtered_chunk = chunk[chunk['Id'].isin(question_ids)]
        tags_list.append(filtered_chunk)
        if sum(len(t) for t in tags_list) >= limit:
            break
    tags = pd.concat(tags_list).head(limit)

    # Save reduced files
    print(f"Saving reduced files to {output_path}...")
    print(f"Questions: {len(questions)} rows")
    print(f"Answers: {len(answers)} rows")
    print(f"Tags: {len(tags)} rows")
    questions.to_csv(os.path.join(output_path, 'Questions.csv'), index=False)
    answers.to_csv(os.path.join(output_path, 'Answers.csv'), index=False)
    tags.to_csv(os.path.join(output_path, 'Tags.csv'), index=False)
    
    print("Done!")

if __name__ == "__main__":
    reduce_datasets()
