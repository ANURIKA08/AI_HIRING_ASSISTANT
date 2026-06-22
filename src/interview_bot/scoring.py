def calculate_answer_score(answer: str) -> int:
    """
    Basic scoring based on answer length and keywords
    Input:  answer text
    Output: score 1-10
    """
    if not answer or len(answer.strip()) < 10:
        return 1

    word_count = len(answer.split())

    # Score based on answer length
    if word_count < 10:
        base_score = 3
    elif word_count < 30:
        base_score = 5
    elif word_count < 60:
        base_score = 7
    else:
        base_score = 9

    # Bonus for technical keywords
    technical_words = [
        'algorithm', 'model', 'data', 'function', 'method',
        'example', 'because', 'therefore', 'however', 'implement'
    ]
    answer_lower = answer.lower()
    bonus = sum(1 for word in technical_words if word in answer_lower)
    bonus = min(bonus, 1)

    return min(base_score + bonus, 10)


def get_performance_label(score: int) -> str:
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Below Average"