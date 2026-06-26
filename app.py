import streamlit as st
import requests

st.title("AI Resume Match Engine")
st.caption("Using a sample resume stored locally (resume.txt)")

st.write("Paste a job description and see how well your resume matches.")

job_text = st.text_area("Job Description", height=200)

if st.button("Analyze"):

    if not job_text.strip():
        st.warning("Please enter a job description")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze-job",
                params={"job_text": job_text}
            )

            data = response.json()

            st.subheader("Results")

            st.write("### Summary")
            st.write(data.get("summary", ""))

            st.write("### Fit Score")
            st.success(data.get("fit_score", ""))

            st.write("### Fit Reasoning")
            st.write(data.get("fit_reasoning", ""))

            st.write("### Skills Missing")
            st.warning(", ".join(data.get("skills_missing", [])))

            st.write("### Suggestions")
            st.write(data.get("improvement_suggestions", []))

        except:
            st.error("Something went wrong. Make sure your backend is running.")