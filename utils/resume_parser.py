"""
resume_parser.py
Extracts text from PDF resumes and identifies skills.
"""
import re

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


# Comprehensive skills list
KNOWN_SKILLS = [
    # Languages
    'python', 'java', 'javascript', 'typescript', 'c', 'c++', 'c#', 'ruby', 'go', 'rust',
    'kotlin', 'swift', 'php', 'r', 'scala', 'dart', 'perl',
    # Web
    'html', 'css', 'react', 'angular', 'vue', 'node', 'nodejs', 'express', 'django',
    'flask', 'spring', 'spring boot', 'bootstrap', 'tailwind', 'jquery', 'sass',
    # Data
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'nosql',
    # DS/ML
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy',
    'scikit', 'keras', 'data structures', 'algorithms',
    # Cloud/DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github', 'linux', 'ci/cd',
    # Soft Skills
    'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking',
    'time management', 'presentation',
]


def extract_text_from_pdf(filepath: str) -> str:
    """Extract all text from a PDF file."""
    if not PYPDF2_AVAILABLE:
        return ""
    try:
        text = ""
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception:
        return ""


def extract_skills(text: str) -> list:
    """Extract skills from resume text by matching against known skills list."""
    if not text:
        return []

    text_lower = text.lower()
    found = []

    for skill in KNOWN_SKILLS:
        # Word boundary match to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for s in found:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    return unique