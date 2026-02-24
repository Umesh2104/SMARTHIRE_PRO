SmartHire AI - Final Year BCA Project 🎓

1. Abstract

The conventional interview preparation process lacks dynamic, personalized feedback, leaving students unprepared for real-world unpredictability. SmartHire AI is a production-ready, AI-driven SaaS platform designed to bridge this gap. Utilizing Natural Language Processing (NLP) and the Gemini AI LLM, the system autonomously parses resumes, generates context-aware technical and management questions, and evaluates human answers. The application provides quantifiable scores, pinpointed feedback, and curated learning resources, creating a comprehensive and realistic mock interview environment.

2. Problem Statement

Students and job seekers struggle to self-evaluate their interview skills. Existing platforms offer static, pre-defined question banks that do not adapt to a user's specific resume skills or provide genuine, contextual analysis of subjective answers.

3. Objectives

To implement an intelligent Resume Parser (PDF/DOCX) using Python.

To dynamically generate randomized, difficulty-scaled questions based on extracted skills.

To evaluate user answers using semantic AI analysis (Gemini 2.5) rather than basic keyword matching.

To provide an intuitive Analytics Dashboard tracking progress over time.

To ensure high security using JWT authentication, Bcrypt password hashing, and parameterized PostgreSQL queries.

4. System Architecture Diagram (Textual Representation)

[ Client Browser (HTML/CSS/JS) ] 
       <-- HTTPS / JSON --> 
[ Flask REST API (app.py) ]
       |        |        |
       v        v        v
[ PyPDF2 ]  [ Gemini AI ] [ PostgreSQL DB ]
 (Parser)    (Evaluation)   (Data Store)


Explanation: The architecture follows a modern decoupled pattern. The Frontend (Client) sends REST API requests to the Python Flask backend. The backend manages local processes (like PyPDF2 for parsing) and database connections (PostgreSQL). For heavy AI logic (question generation and answer evaluation), the backend acts as a secure proxy, securely sending prompts to the Gemini AI API and formatting the responses back to the client.

5. ER Diagram Explanation

Users Table: The central hub linking to all other records (1:N relationship with Resumes and Sessions).

Resumes Table: Stores file metadata and extracted JSON skill arrays.

Interview_Sessions: Groups a set of questions and holds the overall score.

Questions & Answers: A 1:1 relationship per session. Questions store the AI prompt text, and Answers store the user's input along with the AI's grading (0-10) and feedback.

Resources: Independent lookup table mapped to candidate weakness topics.

6. How to Run Locally (Setup Instructions)

Prerequisites: Install Python 3.10+ and PostgreSQL.

Database Setup: * Open PGAdmin or psql shell.

Create a database: CREATE DATABASE smarthire;

Run the provided database.sql script to create tables.

Environment Setup:

Create a virtual environment: python -m venv venv

Activate: source venv/bin/activate (Mac/Linux) or venv\Scripts\activate (Windows)

Install dependencies: pip install -r requirements.txt

Environment Variables (.env):

Create a .env file in the root directory.

Add:
DATABASE_URL=postgresql://your_db_user:password@localhost/smarthire
GEMINI_API_KEY=your_google_gemini_api_key
SECRET_KEY=some_random_secure_string

Run the App:

Execute python app.py

Open your browser and go to http://localhost:5000

7. Future Enhancements

Speech-to-Text: Allow users to answer questions verbally using the Web Speech API.

Video Analysis: Integrate OpenCV to track eye movement and confidence levels via webcam.

Real Corporate Integration: Allow companies to define custom prompt parameters for specific job roles.

8. Conclusion

SmartHire AI successfully demonstrates the integration of modern web technologies (Flask, Bootstrap 5) with advanced Generative AI. It fulfills the requirements of a major university project by providing a scalable, secure, and highly interactive solution to a real-world educational problem.