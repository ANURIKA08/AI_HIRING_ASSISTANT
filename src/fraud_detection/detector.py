import pandas as pd
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def check_experience_vs_graduation(experience_years: int, graduation_year: int) -> dict:
    """
    Check if experience claimed matches graduation year
    """
    current_year = datetime.now().year
    flag = False
    reason = ""

    if graduation_year and experience_years:
        max_possible = current_year - graduation_year
        if experience_years > max_possible + 1:
            flag = True
            reason = f"Claims {experience_years} years experience but graduated in {graduation_year} (max possible: {max_possible} years)"

    return {'flagged': flag, 'reason': reason}


def check_duplicate_resume(new_resume_text: str, existing_resumes: list) -> dict:
    """
    Check if resume is duplicate of existing ones
    """
    if not existing_resumes:
        return {'flagged': False, 'reason': '', 'similarity': 0}

    all_texts = existing_resumes + [new_resume_text]

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
        max_similarity = max(similarities) * 100

        if max_similarity > 85:
            return {
                'flagged': True,
                'reason': f"Resume is {round(max_similarity)}% similar to an existing resume",
                'similarity': round(max_similarity)
            }
    except:
        pass

    return {'flagged': False, 'reason': '', 'similarity': 0}


def check_skill_mismatch(claimed_role: str, extracted_skills: list) -> dict:
    """
    Check if skills match claimed job role
    """
    role_required_skills = {
        'data scientist': ['python', 'machine learning', 'statistics', 'sql'],
        'ml engineer': ['python', 'tensorflow', 'pytorch', 'deep learning'],
        'data analyst': ['sql', 'excel', 'power bi', 'tableau'],
        'python developer': ['python', 'django', 'flask', 'rest api'],
        'web developer': ['html', 'css', 'javascript', 'react']
    }

    skills_lower = [s.lower() for s in extracted_skills]
    role_lower = claimed_role.lower()

    for role_key, required in role_required_skills.items():
        if role_key in role_lower:
            matched = [s for s in required if s in skills_lower]
            match_percent = (len(matched) / len(required)) * 100

            if match_percent < 25:
                return {
                    'flagged': True,
                    'reason': f"Claims {claimed_role} but only has {round(match_percent)}% of required skills"
                }

    return {'flagged': False, 'reason': ''}


def detect_fraud(candidate: dict, existing_resumes: list = None) -> dict:
    """
    Main fraud detection function
    Input:  candidate dictionary, existing resumes list
    Output: fraud report dict
    """
    flags = []
    fraud_score = 0

    # Check 1: Experience vs Graduation
    exp_check = check_experience_vs_graduation(
        candidate.get('experience_years', 0),
        candidate.get('graduation_year', None)
    )
    if exp_check['flagged']:
        flags.append(exp_check['reason'])
        fraud_score += 40

    # Check 2: Duplicate Resume
    if existing_resumes:
        dup_check = check_duplicate_resume(
            candidate.get('raw_text', ''),
            existing_resumes
        )
        if dup_check['flagged']:
            flags.append(dup_check['reason'])
            fraud_score += 40

    # Check 3: Skill Mismatch
    skill_check = check_skill_mismatch(
        candidate.get('preferred_role', ''),
        candidate.get('skills', [])
    )
    if skill_check['flagged']:
        flags.append(skill_check['reason'])
        fraud_score += 20

    # Determine risk level
    if fraud_score >= 60:
        risk_level = 'High Risk'
    elif fraud_score >= 30:
        risk_level = 'Medium Risk'
    else:
        risk_level = 'Low Risk'

    return {
        'fraud_score': min(fraud_score, 100),
        'risk_level': risk_level,
        'flags': flags,
        'is_suspicious': fraud_score >= 40
    }


# ---------- TEST IT ----------
if __name__ == "__main__":
    # Test with suspicious candidate
    suspicious = {
        'name': 'Fake Candidate',
        'experience_years': 15,
        'graduation_year': 2022,
        'preferred_role': 'Data Scientist',
        'skills': ['Excel'],
        'raw_text': 'Sample resume text'
    }

    result = detect_fraud(suspicious)
    print("=== FRAUD DETECTION TEST ===")
    print(f"Fraud Score: {result['fraud_score']}/100")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Flags: {result['flags']}")
    print(f"Suspicious: {result['is_suspicious']}")