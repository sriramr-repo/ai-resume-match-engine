# AI Resume Match Engine

This is an AI-powered application that evaluates how well a resume matches a job description.

---

## What it does

- Takes a job description as input
- Uses AI to analyze it
- Returns:
  - Summary
  - Fit score
  - Missing skills
  - Suggestions for improvement

---

## What is the UI?

UI means **User Interface** — the page where you interact with the app.

In this project, the UI is a Streamlit app.

After running the code, open this in your browser:
http://localhost:8501

That page is the UI.

---

## Project structure

- backend.py → API + AI logic
- app.py → UI (Streamlit)
- resume.txt → sample resume

---

## How to run

### Start backend
python -m uvicorn backend:app --host 127.0.0.1 --port 9000

### Start UI

python -m streamlit run app.py

---

## Tech used

- Python
- FastAPI
- Streamlit
- Google Gemini

---

## Status

✅ Working end-to-end
