import streamlit as st
import google.generativeai as genai
import json

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# Title
st.title("AI Resume Match Engine")
st.write("Analyze job fit and prepare for interviews.")

# Shared Inputs
job_text = st.text_area("Job Description")
resume_text = st.text_area("Your Resume")

st.divider()

# Tabs
tab1, tab2 = st.tabs(["Resume Match", "Interview Prep"])

# -----------------------------
# TAB 1: Resume Match
# -----------------------------
with tab1:

    st.subheader("Resume Match Analysis")

    if st.button("Analyze Resume Match", key="match"):

        if not job_text.strip() or not resume_text.strip():
            st.warning("Please fill in both fields.")
        else:
            try:
                with st.spinner("Analyzing Resume Match..."):

                    prompt = f"""
You are a hiring manager evaluating a candidate.

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_text}

Return ONLY valid JSON. No explanation.

Format EXACTLY like this:

{{
  "summary": "2-3 line summary",
  "fit_score": 0,
  "missing_skills": ["skill1", "skill2"]
}}
"""

                    response = model.generate_content(prompt)

                # ✅ Robust JSON parsing
                clean_text = response.text.strip()

                if clean_text.startswith("```"):
                    clean_text = clean_text.split("```")[1]
                    clean_text = clean_text.replace("json", "").strip()

                data = json.loads(clean_text)

                st.markdown("### Summary")
                st.write(data.get("summary", ""))

                st.markdown("### Fit Score")
                st.success(f"{data.get('fit_score', '')}%")

                st.markdown("### Missing Skills")
                for skill in data.get("missing_skills", []):
                    st.write(f"- {skill}")

            except Exception as e:
                st.error("Error during analysis")
                st.text(str(e))

# -----------------------------
# TAB 2: Interview Prep
# -----------------------------
with tab2:

    st.subheader("Interview Preparation")

    if st.button("Generate Interview Prep", key="prep"):

        if not job_text.strip() or not resume_text.strip():
            st.warning("Please fill in both fields.")
        else:
            try:
                with st.spinner("Generating Interview Prep..."):

                    prompt = f"""
You are an experienced interview coach.

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_text}

Return ONLY valid JSON. No explanation.

Format EXACTLY like this:

{{
  "questions": ["question1", "question2", "question3", "question4", "question5"],
  "answers": ["answer1", "answer2"],
  "weak_areas": ["weakness1", "weakness2"],
  "suggestions": ["suggestion1", "suggestion2"]
}}
"""

                    response = model.generate_content(prompt)

                # ✅ Robust JSON parsing
                clean_text = response.text.strip()

                if clean_text.startswith("```"):
                    clean_text = clean_text.split("```")[1]
                    clean_text = clean_text.replace("json", "").strip()

                data = json.loads(clean_text)

                st.markdown("### Interview Questions")
                for i, q in enumerate(data.get("questions", []), 1):
                    st.write(f"{i}. {q}")

                st.markdown("### Sample Answers")
                for a in data.get("answers", []):
                    st.write(f"- {a}")

                st.markdown("### Weak Areas")
                for w in data.get("weak_areas", []):
                    st.write(f"- {w}")

                st.markdown("### Suggestions")
                for s in data.get("suggestions", []):
                    st.write(f"- {s}")

            except Exception as e:
                st.error("Error generating interview prep")
                st.text(str(e))