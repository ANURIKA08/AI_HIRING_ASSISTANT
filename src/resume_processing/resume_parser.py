import re
import spacy
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

EDUCATION_KEYWORDS = [
    "B.Tech", "BTech", "B.E", "BE", "B.Sc", "BSc", "BCA", "BBA",
    "M.Tech", "MTech", "M.Sc", "MSc", "MCA", "MBA",
    "PhD", "Ph.D", "Doctorate",
    "12th", "10th", "High School", "Intermediate", "Diploma"
]

EDUCATION_SCORES = {
    "10th": 1, "12th": 2, "High School": 2, "Intermediate": 2,
    "Diploma": 2, "BCA": 3, "BBA": 3, "B.Sc": 3, "BSc": 3,
    "B.Tech": 3, "BTech": 3, "B.E": 3, "BE": 3,
    "MCA": 4, "MBA": 4, "M.Sc": 4, "MSc": 4,
    "M.Tech": 4, "MTech": 4,
    "PhD": 5, "Ph.D": 5, "Doctorate": 5
}

CERTIFICATION_KEYWORDS = [
    "certified", "certification", "certificate", "aws", "azure",
    "google cloud", "coursera", "udemy", "nptel", "microsoft",
    "oracle", "cisco", "pmp", "scrum", "agile"
]


def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_phone(text):
    pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_name(text):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    first_line = text.strip().split('\n')[0]
    return first_line[:50] if first_line else "Unknown"


def extract_education(text):
    found = []
    text_lower = text.lower()
    for keyword in EDUCATION_KEYWORDS:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return found if found else ["Not specified"]


def extract_education_score(education_list):
    max_score = 0
    for edu in education_list:
        score = EDUCATION_SCORES.get(edu, 0)
        if score > max_score:
            max_score = score
    return max_score


def extract_experience(text):
    """Catches explicit phrases like '5 years experience'"""
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'(\d+)\+?\s*years?\s*experience',
        r'experience\s*of\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s*experience',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    return 0


def extract_experience_smart(text):
    """
    Main experience extractor.
    First tries explicit phrases like '5 years experience'.
    If not found, falls back to detecting actual date ranges
    (e.g. '2018 - 2022', '2020 to Present') instead of grabbing
    any two unrelated years in the resume.
    """
    explicit = extract_experience(text)
    if explicit > 0:
        return explicit

    range_pattern = r'(20\d{2}|19\d{2})\s*(?:-|–|to)\s*(20\d{2}|19\d{2}|present|current)'
    matches = re.findall(range_pattern, text, re.IGNORECASE)

    current_year = datetime.now().year
    total_years = 0
    for start, end in matches:
        start_year = int(start)
        end_year = current_year if end.lower() in ['present', 'current'] else int(end)
        if end_year >= start_year:
            total_years += (end_year - start_year)

    return min(total_years, 40) if total_years > 0 else 0


def extract_graduation_year(text):
    years = re.findall(r'\b(19|20)\d{2}\b', text)
    if years:
        return min(int(y) for y in years)
    return None


def extract_certifications(text):
    text_lower = text.lower()
    found = []
    for keyword in CERTIFICATION_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword.title())
    return list(set(found))


def parse_resume(raw_text):
    """
    Main function
    Input:  raw text from OCR (string)
    Output: dictionary with all extracted fields
    """
    education = extract_education(raw_text)
    certifications = extract_certifications(raw_text)

    parsed = {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "education": education,
        "education_score": extract_education_score(education),
        "experience_years": extract_experience_smart(raw_text),
        "graduation_year": extract_graduation_year(raw_text),
        "certifications": certifications,
        "certification_score": len(certifications),
        "raw_text": raw_text
    }

    return parsed


# ---------- TEST IT ----------
if __name__ == "__main__":
    sample_text = """
    John Doe
    Email: john.doe@gmail.com
    Phone: 9876543210

    Education: B.Tech in Computer Science, 2018 - 2022

    Worked at TCS from 2022 to 2025 as a Python Developer.

    Skills: Python, SQL, TensorFlow, Machine Learning, Deep Learning

    Certifications: AWS Certified, Google Cloud Certificate
    """

    result = parse_resume(sample_text)
    print("=== PARSED RESUME ===")
    for key, value in result.items():
        if key != "raw_text":
            print(f"{key}: {value}")