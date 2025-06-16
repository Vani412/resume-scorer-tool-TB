import streamlit as st
import fitz  # PyMuPDF
from scorer import score_resume, analyze_resume_sections
from keywords import DOMAIN_KEYWORDS

# Page config
st.set_page_config(page_title="Resume Scorer", layout="centered")

# Custom CSS for light theme and readability
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #ffffff;
            color: #000000;
        }
        .title {
            font-size: 2.2em;
            color: #111111;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .section {
            background-color: #f7f7f7;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #ccc;
            color: #000000;
        }
        .heading {
            color: #111111;
            font-weight: bold;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }
        .highlight {
            color: #1a73e8;
            font-weight: bold;
        }
        .suggestion {
            color: #b00020;
        }
        ul li {
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<div class='title'>Resume Scorer</div>", unsafe_allow_html=True)

# Domain selection
domain = st.selectbox("Select Resume Domain", list(DOMAIN_KEYWORDS.keys()))

# PDF upload
uploaded_file = st.file_uploader("Upload your Resume PDF", type=["pdf"])

# Processing
if uploaded_file:
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    # Run scoring
    score, breakdown, suggestions, missing_keywords = score_resume(text, domain)
    section_feedback = analyze_resume_sections(text)

    # Total Score
    st.markdown(
        f"<div class='section'><div class='heading'>Total Score</div><div class='highlight'>{score} / 10</div></div>",
        unsafe_allow_html=True
    )

    # Score Breakdown
    st.markdown("<div class='section'><div class='heading'>Score Breakdown</div>", unsafe_allow_html=True)
    for k, v in breakdown.items():
        st.markdown(f"- **{k}**: {v}/10")
    st.markdown("</div>", unsafe_allow_html=True)

    # Missing Keywords
    if missing_keywords:
        st.markdown("<div class='section'><div class='heading'>Missing Keywords</div>", unsafe_allow_html=True)
        for kw in missing_keywords:
            st.markdown(f"<span class='highlight'>• {kw}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Section Feedback
    if section_feedback:
        st.markdown("<div class='section'><div class='heading'>Section Feedback</div>", unsafe_allow_html=True)
        for fb in section_feedback:
            st.markdown(f"- <span class='suggestion'>{fb}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Personalized Suggestions
    if suggestions:
        st.markdown("<div class='section'><div class='heading'>Personalized Suggestions</div>", unsafe_allow_html=True)
        for s in suggestions:
            st.markdown(f"- <span class='suggestion'>{s}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Bonus Tips
    st.markdown("""
    <div class='section'>
        <div class='heading'>General Resume Tips</div>
        <ul>
            <li>Use strong action verbs like <b>led</b>, <b>created</b>, <b>optimized</b>.</li>
            <li>Quantify achievements when possible (e.g., "Increased efficiency by 30%").</li>
            <li>Ensure consistent font, spacing, and formatting.</li>
            <li>Highlight certifications and skills related to your domain.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
