import os

SKILLS_FILE = "datasets/skills_list.txt"

def load_skills():
    """Load skills from the text file"""
    if not os.path.exists(SKILLS_FILE):
        return []
    with open(SKILLS_FILE, "r") as f:
        skills = [line.strip() for line in f.readlines() if line.strip()]
    return skills


def extract_skills(raw_text):
    """
    Main function
    Input:  raw resume text (string)
    Output: list of matched skills
    """
    skills_list = load_skills()
    text_lower = raw_text.lower()
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def get_skill_score(candidate_skills, required_skills):
    """
    Calculate how many required skills the candidate has
    Input:  candidate_skills (list), required_skills (list)
    Output: score 0-100
    """
    if not required_skills:
        return 0
    candidate_set = set(s.lower() for s in candidate_skills)
    required_set = set(s.lower() for s in required_skills)
    matched = candidate_set.intersection(required_set)
    return round((len(matched) / len(required_set)) * 100, 2)


# ---------- TEST IT ----------
if __name__ == "__main__":
    sample_text = """
    Experienced in Python, Machine Learning, TensorFlow, SQL, Power BI,
    Deep Learning and Natural Language Processing. 
    Worked with AWS and Docker for deployment.
    """

    skills = extract_skills(sample_text)
    print("=== EXTRACTED SKILLS ===")
    print(skills)
    print(f"Total skills found: {len(skills)}")