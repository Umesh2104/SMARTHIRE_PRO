"""
evaluator.py
Evaluates interview answers using Gemini AI with rich, personalised feedback.
Falls back to rule-based scoring if Gemini is unavailable.
"""
import os
import json
import re

try:
    import google.generativeai as genai
    GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
    GEMINI_AVAILABLE = bool(GEMINI_KEY)
except ImportError:
    GEMINI_AVAILABLE = False


def evaluate_answers(questions: list) -> tuple:
    """
    Evaluate a list of {question, answer} dicts.
    Returns (scores_dict, feedback_string).

    scores_dict = {
        'technical': float (0-100),
        'communication': float (0-100),
        'overall': float (0-100),
        'per_question': [ {score, technical_score, communication_score, feedback} ]
    }
    """
    if GEMINI_AVAILABLE:
        return _evaluate_with_gemini(questions)
    return _evaluate_rule_based(questions)


def _evaluate_with_gemini(questions: list) -> tuple:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')

        qa_text = ""
        for i, q in enumerate(questions, 1):
            answer = q.get('answer', '').strip()
            qa_text += f"\nQ{i}: {q['question']}\nA{i}: {answer if answer else '[No answer provided]'}\n"

        prompt = f"""You are an expert interview evaluator. Evaluate the following interview Q&A.

{qa_text}

For EACH question, score on:
- technical_score: 0-100 (accuracy, depth of knowledge)
- communication_score: 0-100 (clarity, structure, vocabulary)
- question_feedback: 2-3 sentence specific, encouraging feedback. Mention what was good AND what to improve.

Return ONLY a JSON object in this exact format:
{{
  "evaluations": [
    {{
      "q_index": 1,
      "technical_score": 75,
      "communication_score": 80,
      "question_feedback": "Good explanation of the concept. You correctly identified X. To improve, add a real-world example next time."
    }}
  ],
  "overall_strengths": "2-3 sentences about what the candidate did well overall.",
  "overall_improvements": "2-3 sentences on key areas to work on.",
  "recommended_topics": ["topic1", "topic2", "topic3"]
}}"""

        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('```')[1]
            if text.startswith('json'):
                text = text[4:]
        result = json.loads(text.strip())

        return _parse_gemini_result(result, questions)

    except Exception as e:
        return _evaluate_rule_based(questions)


def _parse_gemini_result(result: dict, questions: list) -> tuple:
    evaluations = result.get('evaluations', [])
    strengths = result.get('overall_strengths', '')
    improvements = result.get('overall_improvements', '')
    recommended = result.get('recommended_topics', [])

    tech_scores = []
    comm_scores = []
    per_question = []

    for i, q in enumerate(questions):
        eval_data = next((e for e in evaluations if e.get('q_index') == i + 1), {})
        ts = float(eval_data.get('technical_score', 0))
        cs = float(eval_data.get('communication_score', 0))
        qf = eval_data.get('question_feedback', 'No feedback available.')

        # Penalise empty answers
        if not q.get('answer', '').strip():
            ts = 0
            cs = 0
            qf = "No answer was provided for this question. Make sure to attempt every question."

        tech_scores.append(ts)
        comm_scores.append(cs)
        per_question.append({
            'technical_score': round(ts, 1),
            'communication_score': round(cs, 1),
            'feedback': qf
        })

    avg_tech = round(sum(tech_scores) / len(tech_scores), 1) if tech_scores else 0
    avg_comm = round(sum(comm_scores) / len(comm_scores), 1) if comm_scores else 0
    overall = round((avg_tech * 0.6 + avg_comm * 0.4), 1)

    scores = {
        'technical': avg_tech,
        'communication': avg_comm,
        'overall': overall,
        'per_question': per_question
    }

    # Build rich feedback string
    feedback_parts = []
    if strengths:
        feedback_parts.append(f"✅ Strengths: {strengths}")
    if improvements:
        feedback_parts.append(f"📈 Areas to Improve: {improvements}")
    if recommended:
        feedback_parts.append(f"📚 Recommended Study Topics: {', '.join(recommended)}")

    for i, pq in enumerate(per_question):
        ans = questions[i].get('answer', '').strip()
        status = '❌ Not Answered' if not ans else f"Tech: {pq['technical_score']}% | Comm: {pq['communication_score']}%"
        feedback_parts.append(f"Q{i+1} [{status}]: {pq['feedback']}")

    return scores, '\n\n'.join(feedback_parts)


def _evaluate_rule_based(questions: list) -> tuple:
    """Simple rule-based fallback evaluator."""
    tech_scores = []
    comm_scores = []
    per_question = []
    feedback_parts = []

    for i, q in enumerate(questions):
        answer = q.get('answer', '').strip()
        if not answer:
            ts, cs = 0, 0
            qf = "No answer was provided. Always attempt every question, even partially."
        else:
            word_count = len(answer.split())
            # Communication score based on length + sentence structure
            cs = min(100, word_count * 3)
            # Technical score: keyword-based rough check
            question_words = set(q['question'].lower().split())
            answer_words = set(answer.lower().split())
            overlap = len(question_words & answer_words)
            ts = min(100, overlap * 15)
            qf = _rule_based_feedback(answer, word_count)

        tech_scores.append(ts)
        comm_scores.append(cs)
        per_question.append({'technical_score': round(ts, 1), 'communication_score': round(cs, 1), 'feedback': qf})
        ans_status = '❌ Not Answered' if not q.get('answer', '').strip() else f"Tech: {round(ts,1)}% | Comm: {round(cs,1)}%"
        feedback_parts.append(f"Q{i+1} [{ans_status}]: {qf}")

    avg_tech = round(sum(tech_scores) / len(tech_scores), 1) if tech_scores else 0
    avg_comm = round(sum(comm_scores) / len(comm_scores), 1) if comm_scores else 0
    overall = round((avg_tech * 0.6 + avg_comm * 0.4), 1)

    scores = {
        'technical': avg_tech,
        'communication': avg_comm,
        'overall': overall,
        'per_question': per_question
    }

    answered = sum(1 for q in questions if q.get('answer', '').strip())
    summary = f"✅ You answered {answered}/{len(questions)} questions."
    if avg_tech < 40:
        summary += "\n📈 Areas to Improve: Focus on explaining technical concepts with more depth and examples."
    if avg_comm < 40:
        summary += "\n📢 Communication: Try to structure your answers using the STAR method (Situation, Task, Action, Result)."

    return scores, summary + '\n\n' + '\n\n'.join(feedback_parts)


def _rule_based_feedback(answer: str, word_count: int) -> str:
    if word_count < 5:
        return "Very brief answer. Expand your response with examples and technical details."
    elif word_count < 20:
        return "Decent start, but the answer needs more depth. Try to explain 'why' and 'how'."
    elif word_count < 50:
        return "Good answer. Adding a concrete example or use case would make it stronger."
    else:
        return "Well-elaborated answer. Good structure and detail."