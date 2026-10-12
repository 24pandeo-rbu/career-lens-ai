
# analyzer.py
# CareerLens AI: resume and job-description analysis

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# A starter skills library. You can expand it as the project grows.
SKILLS = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Excel": ["excel", "microsoft excel", "spreadsheets"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Java": ["java"],
    "C++": ["c++"],
    "JavaScript": ["javascript"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "HTML": ["html"],
    "CSS": ["css"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Machine Learning": ["machine learning", "ml models"],
    "Deep Learning": ["deep learning"],
    "Natural Language Processing": [
        "natural language processing", "nlp"
    ],
    "Generative AI": ["generative ai", "gen ai", "llm", "llms"],
    "Prompt Engineering": ["prompt engineering"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["microsoft azure", "azure"],
    "Google Cloud": ["google cloud", "gcp"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous delivery"],
    "Linux": ["linux"],
    "Git": ["git", "github", "version control"],
    "Networking": ["networking", "tcp/ip", "dns"],
    "REST APIs": ["rest api", "rest apis", "restful api"],
    "MongoDB": ["mongodb"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "Data Structures and Algorithms": [
        "data structures", "algorithms", "dsa"
    ],
    "Communication": ["communication skills", "verbal communication"],
    "Problem Solving": ["problem solving", "analytical thinking"],
    "Agile": ["agile", "scrum"],
    "Testing": ["unit testing", "software testing", "pytest"],
}


def normalize_text(text):
    """Clean whitespace without removing useful technical symbols."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    """
    Find known skills using phrase matching.
    Returns canonical skill names found in the text.
    """
    normalized = normalize_text(text)
    found = []

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            # Avoid matches inside larger words.
            pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"

            if re.search(pattern, normalized):
                found.append(skill)
                break

    return sorted(found)


def calculate_similarity(resume_text, job_text):
    """
    Estimate text similarity using TF-IDF and cosine similarity.
    This is a baseline similarity score, not a hiring probability.
    """
    if not resume_text.strip() or not job_text.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )
        vectors = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(vectors[0], vectors[1])[0][0]

        return round(float(score) * 100, 1)

    except ValueError:
        # For example, both documents contain no usable terms.
        return 0.0


def analyze_resume(resume_text, job_text):
    """Produce the complete analysis result."""
    if not resume_text.strip():
        raise ValueError("The resume contains no readable text.")

    if not job_text.strip():
        raise ValueError("Please provide a job description.")

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))

    if job_skills:
        skill_coverage = round(
            100 * len(matched) / len(job_skills), 1
        )
    else:
        skill_coverage = 0.0

    similarity = calculate_similarity(resume_text, job_text)

    # A transparent composite score, not a prediction of hiring.
    overall_score = round(
        0.7 * skill_coverage + 0.3 * similarity, 1
    )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_coverage": skill_coverage,
        "text_similarity": similarity,
        "overall_score": overall_score,
    }


def make_learning_roadmap(missing_skills):
    """Create starter recommendations from identified skill gaps."""
    roadmap = []

    for skill in missing_skills:
        roadmap.append({
            "Skill": skill,
            "Action": f"Learn the fundamentals of {skill}",
            "Practice": f"Complete a small practical project using {skill}",
        })

    return roadmap
