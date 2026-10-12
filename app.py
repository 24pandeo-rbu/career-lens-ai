
# app.py
# CareerLens AI - Resume and Job Match Analyzer

import io
import re

import pandas as pd
import streamlit as st
import pymupdf

from analyzer import analyze_resume, make_learning_roadmap


st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 CareerLens AI")
st.subheader("Resume intelligence. Clearer career decisions.")
st.write(
    "Compare a resume with a job description, identify relevant "
    "skills, and create a practical plan to close skill gaps."
)

st.info(
    "Privacy: this starter version processes resume text in the "
    "running application and does not save uploaded resumes to a "
    "database. Avoid uploading sensitive personal documents to "
    "public or shared deployments."
)


def extract_pdf_text(pdf_bytes):
    """Extract selectable text from a PDF held in memory."""
    text_parts = []

    with pymupdf.open(
        stream=io.BytesIO(pdf_bytes),
        filetype="pdf",
    ) as document:
        for page in document:
            text_parts.append(page.get_text())

    return "\n".join(text_parts).strip()


def make_interview_questions(job_skills, missing_skills):
    """Create starter questions from identified job skills."""
    questions = []

    for skill in job_skills[:5]:
        questions.append(
            f"Explain {skill} and describe a practical example "
            f"of how you would use it in this role."
        )

    for skill in missing_skills[:3]:
        questions.append(
            f"What do you currently know about {skill}, and how "
            f"would you build practical experience in it?"
        )

    questions.append(
        "Describe a project where you solved a difficult problem. "
        "What was your approach and what did you learn?"
    )

    return questions


with st.sidebar:
    st.header("How to use CareerLens AI")
    st.markdown(
        """
        1. Upload a text-based PDF resume.
        2. Paste the target job description.
        3. Click **Analyze my profile**.
        4. Review matches and missing skills.
        5. Follow the learning roadmap.
        """
    )
    st.caption("Version 1.0 — CareerLens AI")


left, right = st.columns([1, 1])

with left:
    st.subheader("1. Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        help="Start with a text-based PDF, not a scanned image.",
    )

with right:
    st.subheader("2. Target Job")
    job_title = st.text_input(
        "Job title",
        placeholder="e.g. Cloud Engineer",
    )
    company = st.text_input(
        "Company (optional)",
        placeholder="e.g. Example company",
    )

job_description = st.text_area(
    "Paste the complete job description",
    height=240,
    placeholder=(
        "Paste the responsibilities, required skills, "
        "qualifications, and experience here..."
    ),
)

analyze_clicked = st.button(
    "Analyze my profile",
    type="primary",
    use_container_width=True,
)

if analyze_clicked:
    if uploaded_file is None:
        st.error("Please upload a PDF resume first.")

    elif len(job_description.strip()) < 50:
        st.error(
            "Please paste a more complete job description "
            "(at least 50 characters)."
        )

    else:
        try:
            with st.spinner("Analyzing resume and job requirements..."):
                pdf_bytes = uploaded_file.getvalue()
                resume_text = extract_pdf_text(pdf_bytes)

                if len(resume_text) < 30:
                    st.error(
                        "Very little text was extracted. This may "
                        "be a scanned PDF. Try a text-based PDF "
                        "exported from Word or Google Docs."
                    )
                else:
                    result = analyze_resume(
                        resume_text,
                        job_description,
                    )

                    st.session_state["analysis"] = result
                    st.session_state["job_title"] = (
                        job_title.strip() or "Target role"
                    )
                    st.session_state["company"] = company.strip()

        except Exception as error:
            st.error(
                "The PDF could not be analyzed. Try another "
                f"text-based PDF. Technical details: {error}"
            )


result = st.session_state.get("analysis")

if result:
    st.divider()
    st.header("Your Career Match Report")

    st.caption(
        f"Role: {st.session_state.get('job_title', 'Target role')}"
        + (
            f" | Company: {st.session_state['company']}"
            if st.session_state.get("company")
            else ""
        )
    )

    st.warning(
        "The match score is an estimate based on skill coverage "
        "and text similarity. It is not the probability of getting "
        "an interview or a job offer."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Estimated match score",
        f"{result['overall_score']}%",
    )
    c2.metric(
        "Skill coverage",
        f"{result['skill_coverage']}%",
    )
    c3.metric(
        "Text similarity",
        f"{result['text_similarity']}%",
    )

    st.progress(
        min(max(result["overall_score"] / 100, 0.0), 1.0)
    )

    st.subheader("3. Skills Analysis")

    matched, missing = st.columns(2)

    with matched:
        st.markdown("#### ✅ Matched skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                st.write(f"✓ {skill}")
        else:
            st.write("No recognized matching skills found.")

    with missing:
        st.markdown("#### 🎯 Skills to develop")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.write(f"• {skill}")
        else:
            st.write(
                "No gaps found in the current skills dictionary. "
                "This does not mean every job requirement is met."
            )

    with st.expander("View all skills detected"):
        st.markdown("**Skills in resume**")
        st.write(
            ", ".join(result["resume_skills"])
            if result["resume_skills"]
            else "No known skills detected."
        )
        st.markdown("**Skills in job description**")
        st.write(
            ", ".join(result["job_skills"])
            if result["job_skills"]
            else "No known skills detected."
        )

    st.subheader("4. Personalized Learning Roadmap")

    roadmap = make_learning_roadmap(result["missing_skills"])

    if roadmap:
        st.dataframe(
            pd.DataFrame(roadmap),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success(
            "No gaps were detected in the current skill library. "
            "Review the job description manually for other "
            "qualifications and experience requirements."
        )

    st.subheader("5. Interview Practice")

    questions = make_interview_questions(
        result["job_skills"],
        result["missing_skills"],
    )

    for number, question in enumerate(questions, start=1):
        st.markdown(f"**Q{number}.** {question}")

    st.subheader("6. Download Your Report")

    report_lines = [
        "CAREERLENS AI — RESUME MATCH REPORT",
        f"Target role: {st.session_state.get('job_title', 'Target role')}",
        f"Company: {st.session_state.get('company', 'Not specified')}",
        f"Estimated match score: {result['overall_score']}%",
        f"Skill coverage: {result['skill_coverage']}%",
        f"Text similarity: {result['text_similarity']}%",
        "",
        "MATCHED SKILLS",
        *[f"- {s}" for s in result["matched_skills"]],
        "",
        "SKILLS TO DEVELOP",
        *[f"- {s}" for s in result["missing_skills"]],
        "",
        "INTERVIEW QUESTIONS",
        *[f"{i}. {q}" for i, q in enumerate(questions, start=1)],
        "",
        "Note: Scores are estimates, not hiring probabilities.",
    ]

    st.download_button(
        "Download analysis as TXT",
        data="\n".join(report_lines),
        file_name="career_lens_report.txt",
        mime="text/plain",
    )

st.divider()
st.caption(
    "CareerLens AI | Python • NLP • Resume Analysis • "
    "Skill Matching • Career Planning"
)
