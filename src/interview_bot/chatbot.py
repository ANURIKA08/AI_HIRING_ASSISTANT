from google import genai
import os


def setup_gemini():
    """Setup Gemini API with new package"""
    api_key = ""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if 'GEMINI_API_KEY' in line:
                    api_key = line.split('=')[1].strip()
    except:
        pass

    if not api_key:
        raise ValueError("Gemini API key not found in .env file!")

    client = genai.Client(api_key=api_key)
    return client


def start_interview(candidate_name: str, candidate_skills: list, job_role: str):
    """Start interview session"""
    client = setup_gemini()
    skills_str = ", ".join(candidate_skills) if candidate_skills else "General Skills"

    system_prompt = f"""You are an expert HR interviewer.
Candidate: {candidate_name}
Skills: {skills_str}
Role: {job_role}

Ask exactly 5 technical questions one at a time.
After each answer give Score: X/10 and brief feedback.
Start with Question 1 now."""

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=system_prompt
    )

    return client, [{"role": "assistant", "content": response.text}], response.text


def send_answer(client, history: list, answer: str):
    """Send answer and get next question"""
    history.append({"role": "user", "content": answer})

    full_conversation = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}"
        for msg in history
    ])

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=full_conversation
    )

    history.append({"role": "assistant", "content": response.text})
    return response.text, history


def calculate_interview_score(history: list) -> int:
    """Extract score from chat history"""
    total_score = 0
    score_count = 0

    for msg in history:
        text = msg.get('content', '')
        if 'Score:' in text:
            try:
                score_part = text.split('Score:')[1].split('/')[0].strip()
                score = int(''.join(filter(str.isdigit, score_part[:3])))
                if 0 < score <= 10:
                    total_score += score
                    score_count += 1
            except:
                pass

    if score_count == 0:
        return 50
    return round((total_score / (score_count * 10)) * 100)


# ---------- TEST IT ----------
if __name__ == "__main__":
    print("Testing Gemini Interview Bot...")
    try:
        client, history, first_question = start_interview(
            candidate_name="John Doe",
            candidate_skills=["Python", "Machine Learning", "SQL"],
            job_role="Data Scientist"
        )
        print("✅ Gemini Bot WORKING!")
        print("First Question:")
        print(first_question)
    except Exception as e:
        print(f"❌ Error: {e}")