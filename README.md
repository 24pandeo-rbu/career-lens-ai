# CareerLens AI — Resume & Job Match Analyzer

CareerLens AI is a Python-based career intelligence application that compares a resume with a job description, identifies relevant skills and gaps, and generates a learning roadmap with interview practice questions.

## Features

- PDF resume text extraction
- Job-description analysis
- Skills identification using a configurable skills dictionary
- TF-IDF and cosine similarity
- Transparent, estimated resume–job matching score
- Matched and missing skills report
- Personalized learning roadmap
- Role-relevant interview practice questions
- Downloadable text report

## Technology Stack

- Python
- Streamlit
- PyMuPDF
- scikit-learn
- Pandas
- Natural language processing techniques

## Project Structure

```text
career-lens-ai/
├── app.py
├── analyzer.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation on Windows

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the application:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## How It Works

1. Extract selectable text from a PDF resume.
2. Identify known skills in the resume and job description.
3. Calculate skill coverage and TF-IDF cosine similarity.
4. Combine these signals into a transparent estimated score.
5. Display skills, gaps, learning suggestions, and interview questions.

## Limitations

- Scanned PDFs may not contain selectable text.
- The skills dictionary does not cover every skill or synonym.
- TF-IDF similarity is based on word overlap and does not fully understand meaning.
- The match score is not a hiring probability.
- Learning recommendations and interview questions in this starter version use templates rather than a generative AI model.
- The application does not make hiring decisions.

## Future Improvements

- Semantic embeddings for stronger matching
- Generative AI explanations and learning plans
- Evidence-backed skill extraction
- Automated unit and integration tests
- Secure deployment and optional report export to PDF

## Author

Om Pande
year of project- 2026
