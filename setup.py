import pandas as pd
import os

# Create folders if missing
os.makedirs('data/processed', exist_ok=True)
os.makedirs('datasets', exist_ok=True)

# Create candidates CSV
df = pd.DataFrame(columns=[
    'candidate_id','name','email','phone','education',
    'experience_years','preferred_role','skills','resume_path',
    'skill_score','job_match_score','interview_score',
    'fraud_score','final_score','status'
])
df.to_csv('data/processed/candidates.csv', index=False)
print("candidates.csv created!")

# Create interview questions CSV
data = {
    'id': [1,2,3,4,5],
    'role': ['Data Scientist','ML Engineer','Data Analyst','Python Developer','General'],
    'question': [
        'Explain supervised vs unsupervised learning.',
        'What is gradient descent?',
        'How do you handle missing data?',
        'What are Python decorators?',
        'Tell me about yourself.'
    ],
    'difficulty': ['Medium','Hard','Easy','Medium','Easy']
}
df2 = pd.DataFrame(data)
df2.to_csv('datasets/interview_questions.csv', index=False)
print("interview_questions.csv created!")

