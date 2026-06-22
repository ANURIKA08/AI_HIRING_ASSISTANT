import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def load_jobs():
    """Load jobs dataset"""
    jobs_path = "datasets/jobs.csv"
    if not os.path.exists(jobs_path):
        # Create sample jobs if file doesn't exist
        data = {
            "Job Title": [
                "Data Scientist",
                "Machine Learning Engineer",
                "Data Analyst",
                "Python Developer",
                "AI Research Scientist"
            ],
            "Job Field": [
                "Technology", "Technology", "Analytics",
                "Software", "Research"
            ],
            "Required Skills & Qualifications": [
                "Python SQL Machine Learning TensorFlow Statistics Deep Learning",
                "Python TensorFlow PyTorch Deep Learning MLOps Docker",
                "SQL Excel Power BI Tableau Data Visualization Statistics",
                "Python Flask Django REST API Git JavaScript",
                "Python Research NLP BERT Transformers Machine Learning"
            ],
            "Job Description": [
                "Build ML models and analyze data",
                "Deploy machine learning systems",
                "Analyze business data and create reports",
                "Build web applications using Python",
                "Research and develop AI algorithms"
            ]
        }
        df = pd.DataFrame(data)
        df.to_csv(jobs_path, index=False)
        return df

    return pd.read_csv(jobs_path)


def match_jobs(candidate_skills, top_n=5):
    """
    Main function
    Input:  candidate_skills (list of strings)
    Output: list of dicts with job title, match %, company
    """
    if not candidate_skills:
        return []

    jobs_df = load_jobs()
    m = get_model()

    candidate_text = " ".join(candidate_skills)
    candidate_vector = m.encode([candidate_text])

    results = []

    for _, row in jobs_df.iterrows():
        # Use correct column name from your CSV
        job_skills_text = str(row.get("Required Skills & Qualifications", ""))
        job_title = str(row.get("Job Title", "Unknown"))
        job_field = str(row.get("Job Field", "N/A"))
        job_desc = str(row.get("Job Description", ""))

        # Combine skills and description for better matching
        combined_text = job_skills_text + " " + job_desc
        job_vector = m.encode([combined_text])

        score = cosine_similarity(candidate_vector, job_vector)[0][0]
        match_percent = round(float(score) * 100, 1)

        results.append({
            "job_title": job_title,
            "company": job_field,
            "required_skills": job_skills_text[:200],
            "match_percent": match_percent,
            "experience_required": 0,
            "salary": "N/A"
        })

    # Sort by match percent descending
    results = sorted(results, key=lambda x: x["match_percent"], reverse=True)
    return results[:top_n]


# ---------- TEST IT ----------
if __name__ == "__main__":
    candidate_skills = ["Python", "SQL", "Machine Learning", "TensorFlow"]
    matches = match_jobs(candidate_skills)

    print("=== JOB MATCHES ===")
    for job in matches:
        print(f"{job['job_title']} ({job['company']}): {job['match_percent']}%")