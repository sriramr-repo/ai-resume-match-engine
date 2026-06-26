import streamlit as st
import google.generativeai as genai

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# Title
st.title("AI Resume Match Engine")

st.write("Analyze job fit and prepare for interviews.")

# ✅ Shared Inputs (IMPORTANT)
job_text = st.text_area("Job Description")
resume_text = st.text_area("Your Resume")
st.divider()

# ✅ Tabs
tab1, tab2 = st.tabs(["Resume Match", "Interview Prep"])

# -----------------------------
# ✅ TAB 1: Resume Match
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

                # st.markdown(response.text)
              import json

data = json.loads(response.text)

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
# ✅ TAB 2: Interview Prep
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
You are an experienced interview coach and mentor to high quality candidates.

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_text}

Return output in VALID markdown format.

### Interview Questions
Provide 5 questions.

### Sample Answers
Provide 2–3 strong answers tailored to resume.

### Weak Areas
Provide 2–3 bullet points.

### Suggestions
Provide 2–3 actionable suggestions as bullet points.
                    """

                    response = model.generate_content(prompt)

                st.markdown(response.text)

            except Exception as e:
                st.error("Error generating interview prep")
                st.text(str(e))