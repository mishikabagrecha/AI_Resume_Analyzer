import streamlit as st

# ── MUST be the absolute first Streamlit call ─────────────────────────────────
st.set_page_config(page_title="ATS Resume Analyzer", page_icon="◈", layout="wide")

import os
import json
import pdfplumber
import pytesseract
from dotenv import load_dotenv
from google import genai
from pdf2image import convert_from_bytes

from ui import (
    inject_styles, render_topbar, render_hero,
    render_inputs, render_analyze_button, render_divider,
    render_results, render_footer,
)

# ─────────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

inject_styles(st)   # CSS injected safely after set_page_config

if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# ─────────────────────────────────────────────
# PDF EXTRACTION
# ─────────────────────────────────────────────
def extract_text_with_ocr(pdf_file):
    text = ""
    try:
        images = convert_from_bytes(pdf_file.read())
        for image in images:
            ocr_text = pytesseract.image_to_string(image)
            if ocr_text:
                text += ocr_text + "\n"
    except Exception as e:
        st.error(f"OCR extraction failed: {e}")
    return text


def read_resume(file):
    text = ""
    file.seek(0)
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        st.warning(f"Normal PDF extraction failed: {e}")

    if len(text.strip()) < 50:
        file.seek(0)
        text = extract_text_with_ocr(file)

    return text.strip()


# ─────────────────────────────────────────────
# AI ANALYSIS — strict scoring prompt
# ─────────────────────────────────────────────
def analyze_resume(resume_text, job_description):
    prompt = f"""
You are a STRICT ATS (Applicant Tracking System) resume evaluator. Be HARSH and REALISTIC.
Most candidates score between 40-70. Only exceptional candidates score 80+. Do NOT inflate scores.

SCORING RULES per category (0-100):

1. skills_match (weight 35%):
   - Score = (exact matched skills / total required skills) * 100, then apply context cap.
   - Fewer than 50% matched -> max score 50. Partial keyword overlaps do NOT count.
   - Skills in projects/certifications count, not just the skills section.

2. experience_relevance (weight 25%):
   - No experience / unrelated internship -> 20-35
   - One short relevant internship (< 3 months) -> 40-55
   - Solid relevant internship (3-6 months) -> 55-70
   - Full-time relevant work experience -> 70-90
   - For freshers: academic projects and virtual programs count partially.

3. projects_quality (weight 20%):
   - Toy / tutorial projects -> 25-40
   - 1-2 real projects without deployment -> 45-65
   - 2-3 solid projects with links or deployment -> 65-80
   - Complex, deployed, impressive projects -> 80-90

4. education_certifications (weight 10%):
   - Unrelated degree -> 20-40
   - Related degree (CS/IT/etc.) in progress -> 50-65
   - Completed related degree -> 65-80
   - Degree + relevant certifications (Google, IBM, etc.) -> +10 each, max 90

5. resume_presentation (weight 10%):
   - Missing contact info or messy structure -> 20-40
   - Decent but issues present -> 50-70
   - Clean, ATS-friendly, GitHub + LinkedIn present -> 75-90

CANDIDATE LEVEL DETECTION:
- Student/fresher (graduation year 2025-2027): evaluate against FRESHER standards.
- For freshers: projects and certifications are primary signals. Do NOT penalize for no professional experience.

FINAL SCORE: compute the exact weighted average. Do NOT round up generously.

Job Description:
{job_description}

Resume:
{resume_text}

Return ONLY valid JSON. No markdown. No explanation. No extra text.

Format:
{{
  "candidate_level": "fresher or experienced",
  "final_score": <weighted integer 0-100>,
  "score_breakdown": {{
    "skills_match": {{ "score": <0-100>, "matched": ["skill1", "skill2"], "missing": ["skill3"] }},
    "experience_relevance": {{ "score": <0-100>, "reason": "one line explanation" }},
    "projects_quality": {{ "score": <0-100>, "reason": "one line explanation" }},
    "education_certifications": {{ "score": <0-100>, "reason": "one line explanation" }},
    "resume_presentation": {{ "score": <0-100>, "reason": "one line explanation" }}
  }},
  "summary": "2-3 sentence overall summary",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2"],
  "missing_skills": ["skill1", "skill2"],
  "recommendations": ["action 1", "action 2", "action 3"]
}}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)

    # Recalculate server-side to prevent AI score inflation
    weights = {
        "skills_match": 0.35,
        "experience_relevance": 0.25,
        "projects_quality": 0.20,
        "education_certifications": 0.10,
        "resume_presentation": 0.10,
    }
    breakdown = data.get("score_breakdown", {})
    data["final_score"] = round(sum(
        breakdown.get(k, {}).get("score", 0) * w for k, w in weights.items()
    ))
    return data


# ─────────────────────────────────────────────
# APP LAYOUT
# ─────────────────────────────────────────────
render_topbar(st)
render_hero(st)

job_description, uploaded_file = render_inputs(st)
render_divider(st)

analyze_clicked = render_analyze_button(st)
render_divider(st)

# ─────────────────────────────────────────────
# ANALYSIS FLOW
# ─────────────────────────────────────────────
if uploaded_file and analyze_clicked:

    if not job_description.strip():
        st.warning("Please paste a job description before analyzing.")
        st.stop()

    with st.spinner("Extracting resume text..."):
        resume_text = read_resume(uploaded_file)

    if len(resume_text.strip()) < 50:
        st.error("Could not extract enough text from this PDF. Try a text-based PDF.")
        st.stop()

    resume_text = resume_text[:15000]

    with st.expander("View extracted resume text"):
        st.write(resume_text)

    with st.spinner("Running AI analysis..."):
        try:
            data = analyze_resume(resume_text, job_description)
        except Exception as e:
            st.error(f"Failed to parse AI response: {e}")
            st.stop()

    render_results(st, data)

render_footer(st)