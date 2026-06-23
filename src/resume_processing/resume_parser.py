import re

# ====================================================================
# LIGHTWEIGHT EXTRACTION FUNCTIONS (No heavy ML models needed here!)
# ====================================================================

def extract_experience(text):
    """
    Scans the resume text using Regular Expressions (Regex) to find 
    mentions of years of experience (e.g., '5 years of experience').
    """
    pattern = r'(\d+)\s*(?:years?|yrs?)(?:\s+of)?\s+experience'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        return max([int(m) for m in matches])
    return 0

def extract_education(text):
    """
    Searches for common degree keywords within the resume text.
    """
    education_keywords = [
        'bachelor', 'b.tech', 'b.sc', 'b.e', 
        'master', 'm.tech', 'm.sc', 'mba', 
        'phd', 'doctorate'
    ]
    found_education = []
    text_lower = text.lower()
    
    for kw in education_keywords:
        if kw in text_lower:
            found_education.append(kw)
            
    return found_education

def extract_education_score(education_list):
    """
    Assigns a mathematical weight to the highest level of education.
    """
    score = 0
    for edu in education_list:
        edu_lower = edu.lower()
        if any(phd in edu_lower for phd in ['phd', 'doctorate']):
            score = max(score, 5)
        elif any(master in edu_lower for master in ['master', 'm.tech', 'm.sc', 'mba']):
            score = max(score, 4)
        elif any(bachelor in edu_lower for bachelor in ['bachelor', 'b.tech', 'b.sc', 'b.e']):
            score = max(score, 3)
            
    if score == 0 and len(education_list) > 0:
        score = 1
        
    return score