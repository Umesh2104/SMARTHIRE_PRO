import os
import uuid
import json
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify, Response
)
from config import Config

# Import utility modules
from utils.resume_parser import extract_text_from_pdf, extract_skills
from utils.question_generator import generate_questions
from utils.evaluator import evaluate_answers

app = Flask(__name__)
app.config.from_object(Config)

# Optional mail (won't crash if not configured)
try:
    from flask_mail import Mail, Message
    mail = Mail(app)
    MAIL_AVAILABLE = True
except Exception:
    MAIL_AVAILABLE = False

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -------------------------------------------------------------------
# JSON Data Manager
# -------------------------------------------------------------------
DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {'users': {}, 'candidates': {}}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {'users': {}, 'candidates': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# -------------------------------------------------------------------
# Auth Helpers
# -------------------------------------------------------------------
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if role:
                data = load_data()
                user = data['users'].get(session['user_id'])
                if not user or user['role'] != role:
                    flash('Unauthorized access.', 'danger')
                    return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        role = request.form.get('role', 'candidate')

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        data = load_data()
        for uid, u in data['users'].items():
            if u['email'] == email:
                flash('Email already registered.', 'danger')
                return redirect(url_for('register'))

        user_id = str(uuid.uuid4())
        data['users'][user_id] = {
            'id': user_id,
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,
            'created_at': datetime.datetime.now().isoformat()
        }
        if role == 'candidate':
            data['candidates'][user_id] = {
                'user_id': user_id,
                'resume_text': '',
                'skills': [],
                'interviews': [],
                'asked_questions': []   # ← Track all asked questions to avoid repeats
            }
        save_data(data)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        data = load_data()
        user = None
        for uid, u in data['users'].items():
            if u['email'] == email:
                user = u
                break
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            flash(f"Welcome back, {user['name']}!", 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required()
def dashboard():
    data = load_data()
    user_id = session['user_id']
    user = data['users'].get(user_id)
    if not user:
        session.clear()
        return redirect(url_for('login'))

    role = user['role']
    if role == 'admin':
        candidates = data['candidates']
        total_candidates = len(candidates)
        total_interviews = sum(len(c.get('interviews', [])) for c in candidates.values())
        all_scores = [
            iv['scores']['overall']
            for c in candidates.values()
            for iv in c.get('interviews', [])
        ]
        avg_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
        stats = {'total_candidates': total_candidates, 'total_interviews': total_interviews, 'avg_score': avg_score}
        return render_template('dashboard.html', role=role, stats=stats)
    else:
        candidate = data['candidates'].get(user_id, {'interviews': [], 'skills': []})
        interviews = candidate.get('interviews', [])
        total_interviews = len(interviews)
        avg_score = 0
        if interviews:
            avg_score = round(sum(iv['scores']['overall'] for iv in interviews) / total_interviews, 1)
        stats = {'total_interviews': total_interviews, 'avg_score': avg_score}
        return render_template('dashboard.html', role=role, stats=stats, candidate=candidate)

@app.route('/upload_resume', methods=['POST'])
@login_required(role='candidate')
def upload_resume():
    if 'resume' not in request.files:
        flash('No file selected.', 'danger')
        return redirect(url_for('dashboard'))
    file = request.files['resume']
    if not file or file.filename == '':
        flash('No file selected.', 'danger')
        return redirect(url_for('dashboard'))

    if file.filename.lower().endswith('.pdf'):
        filename = secure_filename(f"{session['user_id']}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        skills = extract_skills(text)

        data = load_data()
        candidate = data['candidates'].get(session['user_id'])
        if candidate is None:
            # Create candidate record if missing
            data['candidates'][session['user_id']] = {
                'user_id': session['user_id'],
                'resume_text': '',
                'skills': [],
                'interviews': [],
                'asked_questions': []
            }
            candidate = data['candidates'][session['user_id']]

        candidate['resume_text'] = text
        candidate['skills'] = skills
        save_data(data)
        flash(f'Resume uploaded! Found {len(skills)} skills: {", ".join(skills[:6])}{"..." if len(skills) > 6 else ""}', 'success')
    else:
        flash('Please upload a PDF file only.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/start_interview', methods=['POST'])
@login_required(role='candidate')
def start_interview():
    interview_type = request.form.get('interview_type', 'technical')
    # User-selected question count (5, 10, or 15), default 10
    try:
        question_count = int(request.form.get('question_count', 10))
        question_count = max(5, min(15, question_count))  # clamp 5-15
    except (ValueError, TypeError):
        question_count = 10

    data = load_data()
    candidate = data['candidates'].get(session['user_id'])

    if not candidate or not candidate.get('skills'):
        flash('Please upload your resume first.', 'warning')
        return redirect(url_for('dashboard'))

    # Get all previously asked questions to avoid repeats
    asked = candidate.get('asked_questions', [])
    questions = generate_questions(
        candidate['skills'],
        interview_type,
        used_questions=asked,
        count=question_count
    )

    if not questions:
        flash('Could not generate questions. Please try again.', 'danger')
        return redirect(url_for('dashboard'))

    # Record these questions as asked
    candidate.setdefault('asked_questions', []).extend(questions)

    interview_id = str(uuid.uuid4())
    interview = {
        'id': interview_id,
        'date': datetime.datetime.now().isoformat(),
        'type': interview_type,
        'questions': [{'question': q, 'answer': '', 'score': 0} for q in questions],
        'scores': {'technical': 0, 'communication': 0, 'overall': 0},
        'result': 'pending',
        'feedback': '',
        'duration_seconds': 0
    }
    candidate['interviews'].append(interview)
    save_data(data)

    session['current_interview_id'] = interview_id
    session['interview_start_time'] = datetime.datetime.now().isoformat()
    return redirect(url_for('interview'))

@app.route('/interview')
@login_required(role='candidate')
def interview():
    interview_id = session.get('current_interview_id')
    if not interview_id:
        flash('No active interview.', 'warning')
        return redirect(url_for('dashboard'))

    data = load_data()
    candidate = data['candidates'].get(session['user_id'])
    if not candidate:
        flash('Candidate profile not found.', 'danger')
        return redirect(url_for('dashboard'))

    iv = next((x for x in candidate['interviews'] if x['id'] == interview_id), None)
    if not iv:
        flash('Interview not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Time per question: 3 minutes = 180 seconds
    time_per_question = 180
    total_time = time_per_question * len(iv['questions'])

    interview_json = json.dumps(iv)
    return render_template(
        'interview.html',
        interview=iv,
        interview_json=interview_json,
        total_time=total_time,
        time_per_question=time_per_question
    )

@app.route('/save_answer', methods=['POST'])
@login_required(role='candidate')
def save_answer():
    data = load_data()
    candidate = data['candidates'].get(session['user_id'])
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404

    interview_id = session.get('current_interview_id')
    iv = next((x for x in candidate['interviews'] if x['id'] == interview_id), None)
    if not iv:
        return jsonify({'error': 'Interview not found'}), 404

    q_index = int(request.form.get('q_index', 0))
    answer = request.form.get('answer', '').strip()

    if 0 <= q_index < len(iv['questions']):
        iv['questions'][q_index]['answer'] = answer
        save_data(data)
    return jsonify({'status': 'ok'})

@app.route('/submit_interview', methods=['POST'])
@login_required(role='candidate')
def submit_interview():
    data = load_data()
    candidate = data['candidates'].get(session['user_id'])
    if not candidate:
        flash('Candidate not found.', 'danger')
        return redirect(url_for('dashboard'))

    interview_id = session.get('current_interview_id')
    iv = next((x for x in candidate['interviews'] if x['id'] == interview_id), None)
    if not iv:
        flash('Interview not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Calculate duration
    start_time_str = session.get('interview_start_time')
    if start_time_str:
        start_time = datetime.datetime.fromisoformat(start_time_str)
        duration = int((datetime.datetime.now() - start_time).total_seconds())
        iv['duration_seconds'] = duration

    # Evaluate answers
    scores, feedback = evaluate_answers(iv['questions'])
    iv['scores'] = scores
    iv['feedback'] = feedback

    # FIX: Correct threshold — scores are 0-100
    iv['result'] = 'selected' if scores['overall'] >= 60 else 'rejected'

    save_data(data)
    session.pop('current_interview_id', None)
    session.pop('interview_start_time', None)
    return redirect(url_for('results', interview_id=interview_id))

@app.route('/results/<interview_id>')
@login_required()
def results(interview_id):
    data = load_data()
    user_id = session['user_id']
    user = data['users'].get(user_id)
    if not user:
        return redirect(url_for('login'))

    iv = None
    candidate_name = None

    if user['role'] == 'admin':
        for cid, cand in data['candidates'].items():
            for x in cand.get('interviews', []):
                if x['id'] == interview_id:
                    iv = x
                    candidate_name = data['users'].get(cid, {}).get('name', 'Candidate')
                    break
            if iv:
                break
    else:
        candidate = data['candidates'].get(user_id)
        if candidate:
            iv = next((x for x in candidate.get('interviews', []) if x['id'] == interview_id), None)
        candidate_name = user['name']

    if not iv:
        flash('Interview not found.', 'danger')
        return redirect(url_for('dashboard'))

    first_name = candidate_name.split()[0] if candidate_name else 'Candidate'
    return render_template('results.html', interview=iv, candidate_name=candidate_name, first_name=first_name)

@app.route('/send_result_email/<interview_id>', methods=['POST'])
@login_required(role='admin')
def send_result_email(interview_id):
    if not MAIL_AVAILABLE:
        flash('Email service not configured.', 'danger')
        return redirect(url_for('admin_panel'))

    data = load_data()
    iv = None
    candidate_email = None
    candidate_name = None

    for cid, cand in data['candidates'].items():
        for x in cand.get('interviews', []):
            if x['id'] == interview_id:
                iv = x
                candidate_email = data['users'].get(cid, {}).get('email')
                candidate_name = data['users'].get(cid, {}).get('name', 'Candidate')
                break
        if iv:
            break

    if not iv:
        flash('Interview not found.', 'danger')
        return redirect(url_for('admin_panel'))

    subject = f"SmartHire AI: Your Interview Result - {iv['result'].title()}"
    body = f"""Dear {candidate_name},

Thank you for participating in the SmartHire AI mock interview.

Your Overall Score: {iv['scores']['overall']}%
Result: {iv['result'].title()}

Feedback:
{iv['feedback']}

Best regards,
SmartHire AI Team
"""
    try:
        msg = Message(subject, recipients=[candidate_email], body=body)
        mail.send(msg)
        flash('Email sent successfully.', 'success')
    except Exception as e:
        flash(f'Failed to send email: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))

@app.route('/admin')
@login_required(role='admin')
def admin_panel():
    data = load_data()
    candidates_list = []
    for uid, user in data['users'].items():
        if user['role'] == 'candidate':
            cand = data['candidates'].get(uid, {})
            interviews = cand.get('interviews', [])
            last_interview = interviews[-1] if interviews else None
            candidates_list.append({
                'id': uid,
                'name': user['name'],
                'email': user['email'],
                'skills': cand.get('skills', []),
                'total_interviews': len(interviews),
                'last_score': last_interview['scores']['overall'] if last_interview else 'N/A',
                'result': last_interview['result'] if last_interview else 'N/A',
                'interview_id': last_interview['id'] if last_interview else None
            })
    return render_template('admin.html', candidates=candidates_list)

@app.route('/delete_candidate/<user_id>', methods=['POST'])
@login_required(role='admin')
def delete_candidate(user_id):
    data = load_data()
    if user_id in data['users'] and data['users'][user_id]['role'] == 'candidate':
        del data['users'][user_id]
        data['candidates'].pop(user_id, None)
        save_data(data)
        flash('Candidate deleted successfully.', 'success')
    else:
        flash('Candidate not found.', 'danger')
    return redirect(url_for('admin_panel'))

@app.route('/export_results')
@login_required(role='admin')
def export_results():
    import csv
    import io

    data = load_data()
    output = []
    for uid, user in data['users'].items():
        if user['role'] == 'candidate':
            cand = data['candidates'].get(uid, {})
            for iv in cand.get('interviews', []):
                duration_min = round(iv.get('duration_seconds', 0) / 60, 1)
                output.append({
                    'Name': user['name'],
                    'Email': user['email'],
                    'Interview Date': iv['date'][:10],
                    'Type': iv['type'].title(),
                    'Technical Score': iv['scores']['technical'],
                    'Communication Score': iv['scores']['communication'],
                    'Overall Score': iv['scores']['overall'],
                    'Result': iv['result'].title(),
                    'Duration (min)': duration_min
                })

    if not output:
        flash('No data to export.', 'warning')
        return redirect(url_for('admin_panel'))

    si = io.StringIO()
    cw = csv.DictWriter(si, fieldnames=output[0].keys())
    cw.writeheader()
    cw.writerows(output)
    return Response(
        si.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=smarthire_results.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True)