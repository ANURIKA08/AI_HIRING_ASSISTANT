import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler


EDUCATION_SCORES = {
    "10th": 1, "12th": 2, "High School": 2, "Intermediate": 2,
    "Diploma": 2, "BCA": 3, "BBA": 3, "B.Sc": 3, "BSc": 3,
    "B.Tech": 3, "BTech": 3, "B.E": 3, "BE": 3,
    "MCA": 4, "MBA": 4, "M.Sc": 4, "MSc": 4,
    "M.Tech": 4, "MTech": 4,
    "PhD": 5, "Ph.D": 5, "Doctorate": 5
}


def get_education_score(education):
    if isinstance(education, list):
        return max([EDUCATION_SCORES.get(e, 0) for e in education], default=0)
    return EDUCATION_SCORES.get(str(education), 0)


def calculate_score(candidate: dict) -> float:
    """
    Calculate candidate score using weighted formula
    Input:  candidate dictionary
    Output: score 0-100
    """
    # Get each score
    skill_score = float(candidate.get('skill_score', 0))
    experience = float(candidate.get('experience_years', 0))
    education = candidate.get('education', '')
    certification_score = float(candidate.get('certification_score', 0))
    job_match_score = float(candidate.get('job_match_score', 0))

    # Normalize experience (cap at 10 years = 100%)
    experience_score = min((experience / 10) * 100, 100)

    # Normalize education (max score is 5)
    edu_score = get_education_score(education)
    education_score = (edu_score / 5) * 100

    # Normalize certification (cap at 5 certs = 100%)
    cert_score = min((certification_score / 5) * 100, 100)

    # Weighted formula
    final_score = (
        skill_score * 0.30 +
        experience_score * 0.20 +
        education_score * 0.15 +
        cert_score * 0.10 +
        job_match_score * 0.25
    )

    return round(final_score, 2)


def rank_candidates(candidates_df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank all candidates by score
    Input:  DataFrame of candidates
    Output: DataFrame sorted by score
    """
    if candidates_df.empty:
        return candidates_df

    scores = []
    for _, row in candidates_df.iterrows():
        score = calculate_score(row.to_dict())
        scores.append(score)

    candidates_df = candidates_df.copy()
    candidates_df['final_score'] = scores
    candidates_df = candidates_df.sort_values('final_score', ascending=False)
    candidates_df['rank'] = range(1, len(candidates_df) + 1)

    # Add status based on score
    def get_status(score):
        if score >= 75:
            return 'Shortlisted'
        elif score >= 50:
            return 'Under Review'
        else:
            return 'Rejected'

    candidates_df['status'] = candidates_df['final_score'].apply(get_status)

    # Save to CSV
    candidates_df.to_csv('data/processed/ranked_candidates.csv', index=False)
    print(f"Ranked {len(candidates_df)} candidates!")

    return candidates_df


def get_top_candidates(n=10) -> pd.DataFrame:
    """Get top N candidates from ranked CSV"""
    path = 'data/processed/ranked_candidates.csv'
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    return df.head(n)


# ---------- TEST IT ----------
if __name__ == "__main__":
    # Create sample candidates
    sample_data = {
        'candidate_id': ['CAND-001', 'CAND-002', 'CAND-003'],
        'name': ['Alice', 'Bob', 'Charlie'],
        'skill_score': [85, 60, 45],
        'experience_years': [3, 1, 5],
        'education': ['B.Tech', 'M.Tech', '12th'],
        'certification_score': [2, 1, 0],
        'job_match_score': [90, 70, 50]
    }

    df = pd.DataFrame(sample_data)
    ranked = rank_candidates(df)

    print("\n=== RANKED CANDIDATES ===")
    print(ranked[['name', 'final_score', 'rank', 'status']])