# ui.py — all UI rendering functions
# NOTE: No module-level streamlit import — st is always passed in or imported
#       inside functions to avoid side-effects before set_page_config().

GOOGLE_FONT = (
    "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght"
    "@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,300"
    "&family=DM+Mono:wght@300;400;500"
    "&family=DM+Sans:wght@300;400;500&display=swap"
)


# ─────────────────────────────────────────────
# SCORE HELPERS  (pure functions, no st needed)
# ─────────────────────────────────────────────
def score_color(score):
    if score >= 80:   return "#00c896"
    elif score >= 65: return "#e8b84b"
    elif score >= 45: return "#e87c3e"
    else:             return "#e84b6a"

def score_label(score):
    if score >= 85:   return "Excellent Match"
    elif score >= 70: return "Strong Match"
    elif score >= 55: return "Moderate Match"
    elif score >= 40: return "Weak Match"
    else:             return "Poor Match"


# ─────────────────────────────────────────────
# STYLES  — reads styles.css from disk
# ─────────────────────────────────────────────
def inject_styles(st, css_path="styles.css"):
    import os
    with open(os.path.join(os.path.dirname(__file__), css_path), "r") as f:
        css = f.read()
    st.markdown(
        f'<link href="{GOOGLE_FONT}" rel="stylesheet">'
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# LAYOUT SECTIONS
# ─────────────────────────────────────────────
def render_topbar(st):
    st.markdown("""
    <div class="topbar">
        <div class="topbar-logo">◈ ATS <span>Analyzer</span></div>
        <div class="topbar-tag">Resume Intelligence Engine</div>
        <div class="topbar-badge">Gemini 2.5 Flash · v2.0</div>
    </div>""", unsafe_allow_html=True)


def render_hero(st):
    st.markdown("""
    <div class="hero-wrap">
        <div>
            <div class="hero-eyebrow">◈ AI-Powered ATS Evaluation</div>
            <div class="hero-title">Know where<br>you <em>stand.</em></div>
            <div class="hero-desc">Upload your resume and a job description. Get a precision match score, skill gap analysis, and clear recommendations — in seconds.</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">5</div>
            <div class="hero-stat-label">Weighted scoring<br>dimensions</div>
        </div>
    </div>""", unsafe_allow_html=True)


def render_inputs(st):
    st.markdown('<div style="padding: 2.5rem 3rem 0;">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            '<div class="input-num">01 — Job Description</div>'
            '<div class="input-title">Target Role</div>',
            unsafe_allow_html=True,
        )
        job_description = st.text_area(
            "job_description", height=200,
            placeholder="Paste the full job description here...\n\nInclude required skills, responsibilities, and qualifications for the most accurate analysis.",
            label_visibility="collapsed",
        )

    with col_right:
        st.markdown(
            '<div class="input-num">02 — Resume Upload</div>'
            '<div class="input-title">Your Resume</div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader("resume_upload", type=["pdf"], label_visibility="collapsed")
        st.markdown("""
        <div class="weights-strip">
            <span class="w-chip">Skills 35%</span>
            <span class="w-chip">Experience 25%</span>
            <span class="w-chip">Projects 20%</span>
            <span class="w-chip">Education 10%</span>
            <span class="w-chip">Presentation 10%</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return job_description, uploaded_file


def render_analyze_button(st):
    st.markdown('<div style="padding: 1.75rem 3rem 2.5rem;">', unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        clicked = st.button("◈ Analyze Resume", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked


def render_divider(st):
    st.markdown('<div class="ats-divider"></div>', unsafe_allow_html=True)


def render_results(st, data):
    final_score = data.get("final_score", 0)
    breakdown   = data.get("score_breakdown", {})
    color       = score_color(final_score)
    verdict     = score_label(final_score)
    level       = data.get("candidate_level", "fresher").capitalize()

    # Results header
    st.markdown("""
    <div class="results-header">
        <div class="results-eyebrow">◈ Analysis Complete</div>
        <div class="results-line"></div>
    </div>""", unsafe_allow_html=True)

    # Score + Breakdown rows
    categories = [
        ("Skills Match",         "skills_match",            "35%"),
        ("Experience Relevance", "experience_relevance",    "25%"),
        ("Projects Quality",     "projects_quality",        "20%"),
        ("Education & Certs",    "education_certifications","10%"),
        ("Presentation",         "resume_presentation",     "10%"),
    ]
    rows = []
    for label, key, weight in categories:
        cat = breakdown.get(key, {})
        s   = cat.get("score", 0)
        c   = score_color(s)
        rows.append(
            '<div class="bc-row">'
            f'<div class="bc-name">{label}</div>'
            f'<div class="bc-weight">{weight}</div>'
            '<div class="bc-bar-bg">'
            f'<div class="bc-bar-fill" style="width:{s}%;background:{c}"></div>'
            '</div>'
            f'<div class="bc-score" style="color:{c}">{s}</div>'
            '</div>'
        )

    st.markdown(
        '<div class="score-area">'
        '<div class="score-card">'
        '<div class="sc-label">ATS Match Score</div>'
        f'<div class="sc-number" style="color:{color}">{final_score}'
        f'<span class="sc-denom">/100</span></div>'
        f'<div class="sc-verdict" style="color:{color}">{verdict}</div>'
        f'<div class="sc-level">{level}</div>'
        '</div>'
        '<div class="breakdown-card">'
        '<div class="bc-title">Score Breakdown — Weighted Categories</div>'
        + "\n".join(rows) +
        '</div></div>',
        unsafe_allow_html=True,
    )

    # Skills pills
    skills_data = breakdown.get("skills_match", {})
    matched     = skills_data.get("matched", [])
    missing_sk  = skills_data.get("missing", [])

    if matched or missing_sk:
        st.markdown('<div class="section-grid">', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="large")
        with c1:
            pills = "".join(f'<span class="pill pill-green">{s}</span>' for s in matched)
            st.markdown(
                '<div class="content-card"><div class="cc-head">'
                '<div class="cc-icon" style="background:#f0faf6">✓</div>'
                '<div class="cc-title">Matched Skills</div></div>'
                '<div class="pill-grid">'
                + (pills or '<span style="font-size:0.8rem;color:#ccc">None detected</span>') +
                '</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            pills = "".join(f'<span class="pill pill-red">{s}</span>' for s in missing_sk)
            st.markdown(
                '<div class="content-card"><div class="cc-head">'
                '<div class="cc-icon" style="background:#fef3f5">✗</div>'
                '<div class="cc-title">Missing Skills</div></div>'
                '<div class="pill-grid">'
                + (pills or '<span style="font-size:0.8rem;color:#ccc">None detected</span>') +
                '</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Summary
    st.markdown(
        '<div class="section-full">'
        '<div style="font-family:\'DM Mono\',monospace;font-size:0.6rem;letter-spacing:0.18em;'
        'color:#bbb;text-transform:uppercase;margin-bottom:0.85rem">Summary</div>'
        f'<div class="summary-card">{data.get("summary","")}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Strengths & Weaknesses
    c3, c4 = st.columns(2, gap="large")
    st.markdown('<div style="padding: 0 3rem;">', unsafe_allow_html=True)
    with c3:
        items = "".join(
            f'<div class="li-item"><div class="li-dot" style="background:#00a97a"></div><div>{s}</div></div>'
            for s in data.get("strengths", [])
        )
        st.markdown(
            '<div class="content-card" style="margin:0 0 1.5rem 0;"><div class="cc-head">'
            '<div class="cc-icon" style="background:#f0faf6;font-size:0.75rem">↑</div>'
            '<div class="cc-title">Strengths</div></div>' + items + '</div>',
            unsafe_allow_html=True,
        )
    with c4:
        items = "".join(
            f'<div class="li-item"><div class="li-dot" style="background:#c73b55"></div><div>{w}</div></div>'
            for w in data.get("weaknesses", [])
        )
        st.markdown(
            '<div class="content-card" style="margin:0 0 1.5rem 0;"><div class="cc-head">'
            '<div class="cc-icon" style="background:#fef3f5;font-size:0.75rem">↓</div>'
            '<div class="cc-title">Weaknesses</div></div>' + items + '</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Recommendations
    recs = data.get("recommendations", [])
    if recs:
        rec_items = "".join(
            f'<div class="rec-row"><div class="rec-num">0{i}</div><div class="rec-text">{r}</div></div>'
            for i, r in enumerate(recs, 1)
        )
        st.markdown(
            '<div class="section-full">'
            '<div style="font-family:\'DM Mono\',monospace;font-size:0.6rem;letter-spacing:0.18em;'
            'color:#bbb;text-transform:uppercase;margin-bottom:0.85rem">Recommendations</div>'
            '<div class="content-card"><div class="cc-head">'
            '<div class="cc-icon" style="background:#fdfaf0">→</div>'
            '<div class="cc-title">Action Items to Improve Your Score</div></div>'
            + rec_items + '</div></div>',
            unsafe_allow_html=True,
        )


def render_footer(st):
    st.markdown("""
    <div class="ats-footer">
        <div class="footer-text">Powered by Gemini 2.5 Flash</div>
        <div class="footer-text">◈ ATS Analyzer · v2.0</div>
    </div>""", unsafe_allow_html=True)