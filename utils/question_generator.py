"""
question_generator.py
Uses the 500+ question bank to generate non-repeating, skill-matched questions.
Falls back to Gemini AI for skills not in the bank.
"""
import os
import json
import random

from utils.questions_bank import get_technical_questions, get_management_questions

# Optional: Gemini AI for skills not covered by bank
try:
    import google.generativeai as genai
    GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
    GEMINI_AVAILABLE = bool(GEMINI_KEY)
except ImportError:
    GEMINI_AVAILABLE = False


def generate_questions(skills: list, interview_type: str, used_questions: list = None, count: int = 5) -> list:
    """
    Generate 'count' unique interview questions.
    - Pulls from local bank first (no API cost, no repeats).
    - Falls back to Gemini for niche skills not in bank.
    - used_questions: list of question strings already asked to this candidate.
    """
    used_questions = used_questions or []

    if interview_type == 'management':
        return get_management_questions(count=count, used_questions=used_questions)

    # Technical: try bank first
    questions = get_technical_questions(skills, count=count, used_questions=used_questions)

    # If we didn't get enough from the bank, top up with Gemini
    if len(questions) < count and GEMINI_AVAILABLE:
        remaining = count - len(questions)
        extra = _generate_with_gemini(skills, interview_type, remaining, used_questions + questions)
        questions.extend(extra)

    # Last resort fallback
    if not questions:
        questions = _fallback_questions(skills, count)

    return questions[:count]


def _generate_with_gemini(skills: list, interview_type: str, count: int, used_questions: list) -> list:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        skills_str = ', '.join(skills[:8])
        used_str = '\n'.join(f'- {q}' for q in used_questions[:20])
        prompt = f"""Generate exactly {count} unique {interview_type} interview questions for a candidate with skills: {skills_str}.

IMPORTANT:
- Do NOT repeat or paraphrase any of these already-used questions:
{used_str}
- Return ONLY a JSON array of strings, no explanation.
- Make questions specific and practical.

Example format: ["Question 1?", "Question 2?"]"""

        response = model.generate_content(prompt)
        text = response.text.strip()
        # Strip markdown fences if present
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return []


def _fallback_questions(skills: list, count: int) -> list:
    """Hardcoded fallback when everything else fails."""
    fallback = [
        "Tell me about yourself and your technical background.",
        "What is your strongest programming skill and why?",
        "Describe a project you are most proud of.",
        "How do you stay updated with new technologies?",
        "What are your short-term and long-term career goals?",
    ]
    random.shuffle(fallback)
    return fallback[:count]