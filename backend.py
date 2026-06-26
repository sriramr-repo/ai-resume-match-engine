from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI()   # ✅ app must be defined BEFORE endpoints

import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

@app.get("/")
def home():
    return {"message": "AI server is running ✅"}

@app.get("/test-ai")
def test_ai():
    response = model.generate_content("Say hello like a friendly assistant")
    return {"response": response.text}

@app.post("/analyze-job")
def analyze_job(job_text: str):

    with open("resume.txt", "r") as f:
        resume_text = f.read()

    prompt = f"""
You are an AI career evaluator.

Score the candidate based on:

- Each required skill = +25 points
- Missing skills reduce score proportionally

Return ONLY valid JSON:

{{
  "summary": "...",
  "skills_required": [],
  "skills_present_in_resume": [],
  "skills_missing": [],
  "fit_score": integer (0-100),
  "fit_reasoning": "Brief explanation of score",
  "improvement_suggestions": []
}}

JOB:
{job_text}

RESUME:
{resume_text}
"""

    response = model.generate_content(prompt)

    raw_text = response.text.strip()
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()

    import json
    try:
        parsed = json.loads(cleaned)
        return parsed
    except:
        return {"raw_output": raw_text}