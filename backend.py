from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

@app.get("/")
def home():
    return {"message": "backend is working ✅"}

@app.post("/analyze-job")
def analyze_job(job_text: str):

    with open("resume.txt", "r") as f:
        resume_text = f.read()

    prompt = f"""
    Return ONLY valid JSON.

    {{
      "summary": "...",
      "skills_required": [],
      "skills_present_in_resume": [],
      "skills_missing": [],
      "fit_score": 0-100,
      "fit_reasoning": "...",
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

    try:
        parsed = json.loads(cleaned)
        return parsed
    except:
        return {"raw_output": raw_text}