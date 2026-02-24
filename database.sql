-- PostgreSQL Schema for SmartHire AI

-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS resources CASCADE;
DROP TABLE IF EXISTS answers CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS interview_sessions CASCADE;
DROP TABLE IF EXISTS resumes CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'Student', -- 'Student' or 'Admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Resumes Table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    extracted_skills TEXT, -- Stored as comma-separated or JSON string
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Interview Sessions Table
CREATE TABLE interview_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    interview_type VARCHAR(50) NOT NULL, -- 'Technical' or 'Management'
    total_score NUMERIC(5, 2) DEFAULT 0.00,
    overall_feedback TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Questions Table (Pool of generated/stored questions)
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    difficulty VARCHAR(20), -- 'Easy', 'Medium', 'Hard'
    topic VARCHAR(100)
);

-- 5. Answers & Scores Table
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions(id) ON DELETE CASCADE,
    user_answer TEXT NOT NULL,
    score INTEGER CHECK (score >= 0 AND score <= 10),
    feedback TEXT,
    improvement_topic VARCHAR(100),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Resources Table (Recommendations based on weak topics)
CREATE TABLE resources (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    type VARCHAR(50) -- 'Video', 'Documentation', 'Practice'
);

-- Insert dummy resources for fallback
INSERT INTO resources (topic, title, url, type) VALUES
('Python', 'Python Official Docs', 'https://docs.python.org/3/', 'Documentation'),
('DSA', 'Data Structures & Algorithms', 'https://leetcode.com/', 'Practice'),
('Communication', 'Effective Communication Skills', 'https://www.youtube.com/', 'Video');