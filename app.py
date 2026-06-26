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

# ✅ Tabs
tab1, tab2 = st.tabs(["Resume Match", "Interview Prep"])

# -----------------------------
# ✅ TAB 1: Resume Match
# -----------------------------
with tab1:

    st.subheader("Resume Match Analysis")

    if st.button("Analyze Resume Match"):

        if not job_text.strip() or not resume_text.strip():
            st.warning("Please fill in both fields.")
        else:
            try:
                with st.spinner("Analyzing Resume Match..."):

                    prompt = f"""
                    Analyze the match between this job and resume.

                    JOB:
                    {job_text}

                    RESUME:
                    {resume_text}

                    Output:
                    - Summary (short)
                    - Fit score (0-100)
                    - Missing skills (bullet points)
                    """

                    response = model.generate_content(prompt)

                st.write(response.text)

            except Exception as e:
                st.error("Error during analysis")
                st.text(str(e))

# -----------------------------
# ✅ TAB 2: Interview Prep
# -----------------------------
with tab2:

    st.subheader("Interview Preparation")

    if st.button("Generate Interview Prep"):

        if not job_text.strip() or not resume_text.strip():
            st.warning("Please fill in both fields.")
        else:
            try:
                with st.spinner("Generating Interview Prep..."):

                    prompt = f"""
                    You are an interview coach.

                    JOB:
                    {job_text}

                    RESUME:
                    {resume_text}

                    Output:
                    1. 5 Interview Questions
                    2. Sample Answers tailored to resume
                    3. Weak Areas
                    4. Suggestions to improve
                    """

                    response = model.generate_content(prompt)

                st.write(response.text)

            except Exception as e:
                st.error("Error generating interview prep")
                st.text(str(e))