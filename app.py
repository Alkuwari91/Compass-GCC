import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_engine import (
    build_unis_context,
    chat_rushd,
    generate_dashboard_report,
    explain_matches,
    analyze_gaps,
)

st.set_page_config(page_title="بوصلة", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════
# DESIGN SYSTEM — Luxury Dark × Electric Indigo × Gold
# ══════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
<style>
/* ── Variables ── */
:root {
  --bg-deep:    #07080F;
  --bg-surface: #0D0E1A;
  --bg-card:    rgba(255,255,255,0.03);
  --bg-card-h:  rgba(255,255,255,0.06);
  --indigo:     #6366F1;
  --indigo-dim: rgba(99,102,241,0.15);
  --violet:     #8B5CF6;
  --gold:       #F59E0B;
  --gold-dim:   rgba(245,158,11,0.12);
  --cyan:       #06B6D4;
  --text-1:     #F1F5F9;
  --text-2:     #94A3B8;
  --text-3:     #475569;
  --border:     rgba(255,255,255,0.07);
  --border-h:   rgba(99,102,241,0.4);
  --glow-i:     0 0 40px rgba(99,102,241,0.15);
  --glow-g:     0 0 40px rgba(245,158,11,0.1);
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
  font-family: 'Cairo', sans-serif !important;
  background: var(--bg-deep) !important;
  color: var(--text-1) !important;
}
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
button[kind="header"],
section[data-testid="stSidebar"] { display: none !important; }

/* Mesh background */
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,102,241,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 110%, rgba(139,92,246,0.08) 0%, transparent 60%),
    var(--bg-deep) !important;
}
[data-testid="stMain"] {
  background: transparent !important;
}

/* ── RTL ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  direction: rtl !important;
  text-align: right !important;
}
input, textarea, [role="textbox"] { direction: rtl !important; text-align: right !important; }
div[data-baseweb="select"] * { direction: rtl !important; text-align: right !important; }
label { direction: rtl !important; text-align: right !important; }

/* ── Header ── */
.baw-header {
  text-align: center;
  padding: 70px 20px 50px;
  position: relative;
}
.baw-logo {
  font-family: 'Playfair Display', serif;
  font-size: 5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #fff 0%, var(--indigo) 50%, var(--gold) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 12px;
  letter-spacing: -2px;
}
.baw-sub {
  font-size: 1.05rem;
  color: var(--text-2);
  font-weight: 400;
  letter-spacing: 0.5px;
}
.baw-line {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, var(--indigo), var(--gold));
  margin: 20px auto;
  border-radius: 2px;
}

/* ── Stats Strip ── */
.stats-strip {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin: 0 auto 32px;
  max-width: 700px;
}
.stat-pill {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 10px 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}
.stat-pill:hover {
  border-color: var(--border-h);
  background: var(--indigo-dim);
  box-shadow: var(--glow-i);
}
.stat-pill b {
  font-size: 1.2rem;
  font-weight: 900;
  color: var(--indigo);
}
.stat-pill span {
  font-size: 0.85rem;
  color: var(--text-2);
}

/* ── Navigation ── */
.stButton > button {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-2) !important;
  border-radius: 100px !important;
  font-weight: 600 !important;
  font-family: 'Cairo', sans-serif !important;
  font-size: 0.88rem !important;
  padding: 8px 18px !important;
  transition: all 0.25s ease !important;
  backdrop-filter: blur(8px) !important;
}
.stButton > button:hover {
  background: var(--indigo-dim) !important;
  border-color: var(--indigo) !important;
  color: var(--text-1) !important;
  box-shadow: var(--glow-i) !important;
  transform: translateY(-1px) !important;
}

/* ── Glass Cards ── */
.glass-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px 32px;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  transition: all 0.3s ease;
  margin-bottom: 16px;
}
.glass-card:hover {
  border-color: var(--border-h);
  background: var(--bg-card-h);
  box-shadow: var(--glow-i);
  transform: translateY(-2px);
}
.glass-card h3 {
  margin: 0 0 8px;
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-1);
}
.glass-card .meta {
  color: var(--text-2);
  font-size: 0.88rem;
  margin-bottom: 12px;
}
.glass-card .tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

/* ── Tags ── */
.tag {
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.3px;
}
.tag-gov  { background: rgba(99,102,241,0.15); color: #A5B4FC; border: 1px solid rgba(99,102,241,0.3); }
.tag-priv { background: rgba(139,92,246,0.15); color: #C4B5FD; border: 1px solid rgba(139,92,246,0.3); }
.tag-sch  { background: var(--gold-dim);        color: #FCD34D; border: 1px solid rgba(245,158,11,0.3); }
.tag-lang { background: rgba(6,182,212,0.12);   color: #67E8F9; border: 1px solid rgba(6,182,212,0.25); }

/* ── Accent Link ── */
.card-link {
  color: var(--indigo);
  font-size: 0.83rem;
  text-decoration: none;
  font-weight: 600;
  margin-left: 14px;
  transition: color 0.2s;
}
.card-link:hover { color: var(--gold); }

/* ── Section heading ── */
.section-title {
  font-size: 1.6rem;
  font-weight: 900;
  color: var(--text-1);
  text-align: center;
  margin: 10px 0 24px;
}
.section-title span {
  background: linear-gradient(135deg, var(--indigo), var(--violet));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── AI Report Box ── */
.ai-box {
  background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.08));
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: 20px;
  padding: 28px 32px;
  line-height: 2;
  color: var(--text-1);
  backdrop-filter: blur(12px);
}
.ai-box-label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--indigo);
  text-transform: uppercase;
  margin-bottom: 12px;
  display: block;
}

/* ── Gap Box ── */
.gap-box {
  background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(6,182,212,0.06));
  border: 1px solid rgba(245,158,11,0.2);
  border-radius: 20px;
  padding: 28px 32px;
  line-height: 2.1;
  color: var(--text-1);
}

/* ── Home Cards ── */
.home-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 32px 28px;
  backdrop-filter: blur(16px);
  transition: all 0.3s ease;
  height: 100%;
}
.home-card:hover {
  border-color: var(--border-h);
  box-shadow: var(--glow-i);
  transform: translateY(-3px);
}
.home-card-icon {
  font-size: 2.2rem;
  margin-bottom: 16px;
  display: block;
}
.home-card-title {
  font-size: 1.15rem;
  font-weight: 900;
  color: var(--text-1);
  margin-bottom: 10px;
}
.home-card-text {
  font-size: 0.92rem;
  color: var(--text-2);
  line-height: 1.9;
}

/* ── Divider ── */
.fancy-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 32px 0;
  border: none;
}

/* ── Expander override ── */
div[data-testid="stExpander"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(12px) !important;
  overflow: hidden !important;
  margin-bottom: 12px !important;
  box-shadow: none !important;
}
div[data-testid="stExpander"] details > summary p {
  font-size: 1rem !important;
  font-weight: 800 !important;
  color: var(--text-1) !important;
}
div[data-testid="stExpander"] details > summary:hover {
  background: var(--indigo-dim) !important;
}
div[data-testid="stExpander"] details > div {
  color: var(--text-2) !important;
  line-height: 2 !important;
}

/* ── Selectbox & Input ── */
div[data-baseweb="select"] > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text-1) !important;
}
div[data-baseweb="select"] > div:hover {
  border-color: var(--indigo) !important;
}
.stTextInput > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text-1) !important;
}
.stTextInput > div > div:focus-within {
  border-color: var(--indigo) !important;
  box-shadow: 0 0 0 2px var(--indigo-dim) !important;
}
input { color: var(--text-1) !important; }

/* ── Chat ── */
[data-testid="stChatMessage"] {
  direction: rtl !important;
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(12px) !important;
}
.stChatInputContainer {
  background: var(--bg-surface) !important;
  border-top: 1px solid var(--border) !important;
}
.stChatInputContainer textarea {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text-1) !important;
}

/* ── Number input ── */
.stNumberInput > div > div {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text-1) !important;
}

/* ── Page title ── */
.page-title {
  text-align: center;
  font-weight: 900;
  font-size: 1.9rem;
  margin: 0 0 28px;
  color: var(--text-1);
}

/* ── Counter chip ── */
.count-chip {
  display: inline-block;
  background: var(--indigo-dim);
  border: 1px solid rgba(99,102,241,0.3);
  color: var(--indigo);
  border-radius: 100px;
  padding: 4px 14px;
  font-size: 0.83rem;
  font-weight: 700;
  margin-bottom: 20px;
}

/* ── Comparison cards ── */
.comp-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 24px;
  backdrop-filter: blur(12px);
  height: 100%;
}
.comp-card-title {
  font-size: 1rem;
  font-weight: 900;
  color: var(--text-1);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}
.comp-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  font-size: 0.88rem;
}
.comp-row .label { color: var(--text-3); font-weight: 600; }
.comp-row .value { color: var(--text-1); font-weight: 700; }

/* ── Link button ── */
.stLinkButton a {
  background: var(--indigo-dim) !important;
  border: 1px solid rgba(99,102,241,0.3) !important;
  color: #A5B4FC !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
  transition: all 0.2s !important;
}
.stLinkButton a:hover {
  background: var(--indigo) !important;
  color: white !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-h); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data helpers
# ─────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent
UNIS_PATH  = ROOT / "universities.csv"
PROGS_PATH = ROOT / "programs.csv"


@st.cache_data(show_spinner=False)
def load_unis_csv(path):
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip().lower()
    kw = dict(encoding="utf-8", engine="python", on_bad_lines="skip")
    return pd.read_csv(path, **kw) if first.startswith("uni_id") else pd.read_csv(path, header=None, **kw)


@st.cache_data(show_spinner=False)
def load_csv(path):
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="skip")
        if all(isinstance(c, int) for c in df.columns):
            df = pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="skip", header=None)
        return df
    except Exception:
        return pd.DataFrame()


def normalize_unis(df):
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    cols_15 = ["uni_id","name_ar","name_en","country","city","type",
               "website","admissions_url","programs_url",
               "ranking_source","extra_1","extra_2",
               "scholarship","sch_notes","sch_url"]
    if list(df.columns) == list(range(len(df.columns))):
        df.columns = cols_15[:len(df.columns)]
    if "uni_id" in df.columns and str(df.iloc[0]["uni_id"]).strip().lower() == "uni_id":
        df = df.iloc[1:].copy()
    for c in ["ranking_value","accreditation_notes","scholarship","sch_notes","sch_url"]:
        if c not in df.columns:
            df[c] = ""
    df["scholarship"] = df["scholarship"].fillna("Unknown").astype(str).str.strip().replace({"":"Unknown","nan":"Unknown"})
    needed = ["uni_id","name_ar","name_en","country","city","type",
              "scholarship","sch_notes","sch_url","website","admissions_url","programs_url",
              "ranking_source","ranking_value","accreditation_notes"]
    for c in needed:
        if c not in df.columns:
            df[c] = ""
    return df[needed]


def normalize_progs(df):
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    needed = ["program_id","uni_id","level","degree_type","major_field",
              "program_name_en","program_name_ar","city","language",
              "duration_years","tuition_notes","admissions_requirements","url",
              "english_test","english_score","math_test","math_score",
              "admission_tests","admission_notes"]
    for c in needed:
        if c not in df.columns:
            df[c] = ""
    return df[needed]


def uni_has_sch(s):
    return str(s).strip() not in ["", "No", "Unknown", "nan"]


# Load data
unis_raw  = normalize_unis(load_unis_csv(UNIS_PATH))
progs_raw = normalize_progs(load_csv(PROGS_PATH))
n_unis      = len(unis_raw)
n_progs     = len(progs_raw)
n_countries = unis_raw["country"].nunique() if not unis_raw.empty else 0

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="baw-header">
  <div class="baw-logo">بوصلة</div>
  <div class="baw-line"></div>
  <div class="baw-sub">من الحيرة إلى القرار — دليلك الذكي للتعليم العالي الخليجي</div>
</div>
<div class="stats-strip">
  <div class="stat-pill"><b>{n_unis}+</b><span>جامعة</span></div>
  <div class="stat-pill"><b>{n_countries}</b><span>دول</span></div>
  <div class="stat-pill"><b>{n_progs}+</b><span>برنامج</span></div>
  <div class="stat-pill"><b>GPT‑4</b><span>مدعوم بـ AI</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Navigation
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

PAGES = ["من نحن", "تحليل البيانات", "رُشد", "المقارنة", "بحث الجامعات", "الرئيسية"]
nav_cols = st.columns(len(PAGES))
for i, name in enumerate(PAGES):
    col = nav_cols[-(i + 1)]
    if col.button(name, use_container_width=True, key=f"nav_{name}"):
        st.session_state.page = name
        st.rerun()

st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: الرئيسية
# ══════════════════════════════════════════════
if st.session_state.page == "الرئيسية":
    _, center, _ = st.columns([0.5, 3, 0.5])
    with center:
        st.markdown('<p class="section-title">اكتشف <span>مستقبلك الأكاديمي</span></p>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
<div class="home-card">
  <span class="home-card-icon">💬</span>
  <div class="home-card-title">رُشد — مستشارك الذكي</div>
  <div class="home-card-text">تحدّث بالعربية بشكل طبيعي وسيرشّح لك رُشد أفضل الجامعات المناسبة لملفك الأكاديمي.</div>
</div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""
<div class="home-card">
  <span class="home-card-icon">📊</span>
  <div class="home-card-title">تحليل البيانات</div>
  <div class="home-card-text">لوحة تفاعلية تحوّل بيانات التعليم الخليجي إلى رؤى إحصائية وتقارير ذكية فورية.</div>
</div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""
<div class="home-card">
  <span class="home-card-icon">⚖️</span>
  <div class="home-card-title">مقارنة الجامعات</div>
  <div class="home-card-text">قارن بين أي جامعتين إلى أربع جامعات جنباً إلى جنب لاتخاذ قرارك بثقة.</div>
</div>""", unsafe_allow_html=True)

        st.write("")
        with st.expander("رؤيتنا", expanded=True):
            st.markdown("نسعى في بوصلة إلى إعادة تعريف تجربة اختيار التعليم في الخليج، عبر منصة ذكية توجّه الشباب نحو تخصصاتهم وجامعاتهم المناسبة، وتحوّل القرار التعليمي من حيرة فردية إلى مسار واضح مدروس.")
        with st.expander("رسالتنا"):
            st.markdown("تلتزم بوصلة بتمكين الطلبة وأولياء الأمور من اتخاذ قرارات تعليمية دقيقة من خلال منصة ذكية تعتمد على الذكاء الاصطناعي والبيانات الموثوقة.")
        with st.expander("قيمنا"):
            st.markdown("**الوضوح** · **العدالة** · **التمكين** · **الابتكار** · **الموثوقية**")

        st.write("")
        b1, b2, b3 = st.columns(3)
        if b1.button("💬 تحدث مع رُشد", use_container_width=True):
            st.session_state.page = "رُشد"; st.rerun()
        if b2.button("📊 تحليل البيانات", use_container_width=True):
            st.session_state.page = "تحليل البيانات"; st.rerun()
        if b3.button("🔍 بحث الجامعات", use_container_width=True):
            st.session_state.page = "بحث الجامعات"; st.rerun()


# ══════════════════════════════════════════════
# PAGE: بحث الجامعات
# ══════════════════════════════════════════════
elif st.session_state.page == "بحث الجامعات":
    st.markdown('<p class="page-title">🔍 بحث الجامعات</p>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty:
        st.error("ملف universities.csv غير موجود."); st.stop()

    c4, c3, c2, c1 = st.columns([1.2, 1, 1, 1.2])
    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c4.selectbox("🌍 الدولة",        ["الكل"] + countries)
    types_    = sorted([x for x in unis["type"].unique() if str(x).strip()])
    uni_type  = c3.selectbox("🏛️ النوع",         ["الكل"] + types_)
    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c2.selectbox("🎓 المرحلة",        ["الكل"] + levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c1.selectbox("📚 التخصص",         ["الكل"] + majors_)

    rs, ls = st.columns([3, 1.2])
    q  = rs.text_input("", placeholder="🔎  ابحث عن جامعة أو مدينة...", value="").strip().lower()
    yn = ls.selectbox("💰 المنح", ["الكل", "متاحة", "غير متاحة"])

    f = unis.copy()
    if country  != "الكل": f = f[f["country"] == country]
    if uni_type != "الكل": f = f[f["type"]    == uni_type]
    if yn == "متاحة":       f = f[f["scholarship"].apply(uni_has_sch)]
    if yn == "غير متاحة":   f = f[~f["scholarship"].apply(uni_has_sch)]
    if q:
        mask = (f["name_en"].str.lower().str.contains(q, na=False) |
                f["name_ar"].str.lower().str.contains(q, na=False) |
                f["city"].str.lower().str.contains(q, na=False))
        f = f[mask]
    if (major != "الكل" or level != "الكل") and not progs.empty:
        pm = progs.copy()
        if major != "الكل": pm = pm[pm["major_field"] == major]
        if level != "الكل": pm = pm[pm["level"]       == level]
        f = f[f["uni_id"].isin(pm["uni_id"].unique())]

    st.markdown(f'<div class="count-chip">{len(f)} نتيجة</div>', unsafe_allow_html=True)

    if f.empty:
        st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
    else:
        for _, row in f.head(30).iterrows():
            is_pub   = str(row["type"]).strip().lower() in ["public", "حكومية"]
            type_tag = '<span class="tag tag-gov">حكومية</span>' if is_pub else '<span class="tag tag-priv">خاصة</span>'
            sch_tag  = '<span class="tag tag-sch">💰 منحة</span>' if uni_has_sch(str(row["scholarship"])) else ""
            lang_tags= ""
            if not progs.empty:
                for lg in progs[progs["uni_id"] == str(row["uni_id"])]["language"].dropna().unique()[:3]:
                    lang_tags += f'<span class="tag tag-lang">{lg}</span>'
            links = ""
            if str(row.get("website","")).strip():
                links += f'<a href="{row["website"]}" target="_blank" class="card-link">🌐 الموقع</a>'
            if str(row.get("admissions_url","")).strip():
                links += f'<a href="{row["admissions_url"]}" target="_blank" class="card-link">📋 القبول</a>'

            st.markdown(f"""
<div class="glass-card">
  <h3>{row["name_ar"]} — {row["name_en"]}</h3>
  <div class="meta">📍 {row["city"]}, {row["country"]}</div>
  <div class="tags">{type_tag}{sch_tag}{lang_tags}</div>
  <div style="margin-top:12px;">{links}</div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: المقارنة
# ══════════════════════════════════════════════
elif st.session_state.page == "المقارنة":
    st.markdown('<p class="page-title">⚖️ المقارنة بين الجامعات</p>', unsafe_allow_html=True)

    unis = unis_raw.copy()
    if unis.empty:
        st.error("ملف universities.csv غير موجود."); st.stop()

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + ", " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country","city","name_en"], na_position="last")

    selected = st.multiselect(
        "اختر ٢ إلى ٤ جامعات",
        options=unis["uni_id"].tolist(),
        format_func=lambda x: label_map.get(str(x), str(x)),
        max_selections=4
    )
    if len(selected) < 2:
        st.info("يرجى اختيار جامعتين على الأقل."); st.stop()

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_comp = st.columns(len(selected))
    for i, uid in enumerate(selected):
        row = comp[comp["uni_id"] == uid].iloc[0]
        with cols_comp[i]:
            sch = str(row.get("scholarship","")).strip()
            rank = f"{str(row.get('ranking_source','')).strip()} {str(row.get('ranking_value','')).strip()}".strip()
            st.markdown(f"""
<div class="comp-card">
  <div class="comp-card-title">{row['name_ar']}</div>
  <div class="comp-row"><span class="label">📍 الموقع</span><span class="value">{row['city']}, {row['country']}</span></div>
  <div class="comp-row"><span class="label">🏛️ النوع</span><span class="value">{row['type']}</span></div>
  <div class="comp-row"><span class="label">💰 المنح</span><span class="value">{sch or '—'}</span></div>
  <div class="comp-row"><span class="label">🏆 الترتيب</span><span class="value">{rank or '—'}</span></div>
</div>""", unsafe_allow_html=True)
            st.write("")
            if str(row.get("website","")).strip():
                st.link_button("🌐 Website",    row["website"],        use_container_width=True)
            if str(row.get("admissions_url","")).strip():
                st.link_button("📋 Admissions", row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url","")).strip():
                st.link_button("📚 Programs",   row["programs_url"],   use_container_width=True)


# ══════════════════════════════════════════════
# PAGE: رُشد
# ══════════════════════════════════════════════
elif st.session_state.page == "رُشد":
    st.markdown("""
<div style="text-align:center;margin-bottom:28px;">
  <div style="font-size:3rem;margin-bottom:8px;">🧭</div>
  <h2 style="margin:0;font-size:1.8rem;font-weight:900;color:#F1F5F9;">رُشد</h2>
  <p style="color:#94A3B8;font-size:0.95rem;margin-top:6px;">مستشارك الأكاديمي الذكي — تحدّث بالعربية بشكل طبيعي</p>
</div>
""", unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty:
        st.error("ملف universities.csv غير موجود."); st.stop()

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{
            "role": "assistant",
            "content": (
                "مرحباً! أنا رُشد 🎓\n\n"
                "أخبرني عن نفسك وسأرشّح لك أفضل الجامعات:\n"
                "- ما التخصص الذي تريده؟\n"
                "- أي دولة تفضل؟\n"
                "- ما معدلك وهل عندك IELTS؟"
            )
        }]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"], avatar="🧭" if msg["role"]=="assistant" else "🎓"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":user_input})
        with st.chat_message("user", avatar="🎓"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner("رُشد يفكر..."):
                history = [m for m in st.session_state.rushd_messages
                           if not (m["role"]=="assistant" and "مرحباً" in m["content"])]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role":"assistant","content":reply})

    if len(st.session_state.rushd_messages) > 1:
        if st.button("🔄 محادثة جديدة"):
            st.session_state.rushd_messages = []; st.rerun()


# ══════════════════════════════════════════════
# PAGE: تحليل البيانات
# ══════════════════════════════════════════════
elif st.session_state.page == "تحليل البيانات":
    st.markdown('<p class="page-title">📊 لوحة تحليل البيانات</p>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty:
        st.error("لا تتوفر بيانات."); st.stop()

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    PLOTLY_THEME = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Cairo", color="#94A3B8"),
        margin=dict(l=10,r=10,t=40,b=10),
        height=300,
    )

    # Row 1
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        fig = px.bar(x=list(by_country.values()), y=list(by_country.keys()),
                     orientation="h", title="الجامعات حسب الدولة",
                     color=list(by_country.values()),
                     color_continuous_scale=[[0,"#4338CA"],[1,"#6366F1"]])
        fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False, showlegend=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        fig = px.pie(values=list(by_type.values()), names=list(by_type.keys()),
                     title="حكومية / خاصة", hole=0.55,
                     color_discrete_sequence=["#6366F1","#F59E0B","#06B6D4"])
        fig.update_layout(**PLOTLY_THEME)
        fig.update_traces(textfont_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with ch3:
        if top_fields:
            fig = px.bar(x=list(top_fields.keys()), y=list(top_fields.values()),
                         title="أبرز التخصصات",
                         color=list(top_fields.values()),
                         color_continuous_scale=[[0,"#F59E0B"],[1,"#FCD34D"]])
            fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                              showlegend=False, xaxis_tickangle=-30)
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    # Row 2
    ch4, ch5 = st.columns(2)
    with ch4:
        pct = round(with_sch / max(len(unis),1) * 100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct,
            title={"text":"نسبة الجامعات التي تقدم منحاً %","font":{"family":"Cairo","color":"#94A3B8","size":13}},
            number={"font":{"color":"#F59E0B","family":"Cairo"}},
            gauge={"axis":{"range":[0,100],"tickcolor":"#475569"},
                   "bar":{"color":"#F59E0B"},
                   "bgcolor":"rgba(0,0,0,0)",
                   "bordercolor":"rgba(255,255,255,0.05)",
                   "steps":[{"range":[0,40],"color":"rgba(99,102,241,0.08)"},
                             {"range":[40,70],"color":"rgba(99,102,241,0.12)"},
                             {"range":[70,100],"color":"rgba(99,102,241,0.18)"}]}
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Cairo",color="#94A3B8"),
                          height=280, margin=dict(l=20,r=20,t=40,b=10))
        st.plotly_chart(fig, use_container_width=True)

    with ch5:
        if by_lang:
            fig = px.bar(x=list(by_lang.keys()), y=list(by_lang.values()),
                         title="لغات الدراسة",
                         color=list(by_lang.values()),
                         color_continuous_scale=[[0,"#06B6D4"],[1,"#67E8F9"]])
            fig.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                              showlegend=False, height=280)
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)

    col_rep, col_gap = st.columns(2)
    with col_rep:
        st.markdown("### 🤖 تقرير ذكي تلقائي")
        st.caption("الذكاء الاصطناعي يحلل الإحصاءات ويولّد تقريراً شاملاً")
        if st.button("📝 اطلب التقرير", use_container_width=True):
            stats = {"total_unis":len(unis),"by_country":by_country,"by_type":by_type,
                     "top_fields":top_fields,"by_language":by_lang,
                     "with_scholarships":with_sch,"total_progs":len(progs)}
            with st.spinner("يكتب التقرير..."):
                report = generate_dashboard_report(stats)
            st.markdown(f'<div class="ai-box"><span class="ai-box-label">التقرير التحليلي</span>{report}</div>',
                        unsafe_allow_html=True)

    with col_gap:
        st.markdown("### 🔍 تحليل الفجوات")
        st.caption("الذكاء الاصطناعي يكشف الفجوات في التعليم الخليجي")
        if st.button("🔎 اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div class="gap-box">{gaps}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PAGE: من نحن
# ══════════════════════════════════════════════
elif st.session_state.page == "من نحن":
    st.markdown('<p class="page-title">من نحن</p>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 2.8, 1])
    with center:
        st.markdown("""
<div style="direction:rtl;text-align:center;line-height:2;color:#94A3B8;font-size:1rem;">
  <p style="color:#F1F5F9;font-size:1.1rem;font-weight:700;margin-bottom:16px;">
    بوصلة — منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة
  </p>
  <p>جاءت فكرة بوصلة استجابةً لتحدٍ واقعي يواجه الكثير من الطلبة، وهو <b style="color:#A5B4FC;">تشتّت المعلومات</b> وصعوبة المقارنة بين الجامعات والبرامج.</p>
  <p>نعمل على جمع البيانات وتنظيمها وتقديمها بطريقة مبسطة مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على فهم الخيارات واتخاذ القرار بثقة.</p>
</div>
""", unsafe_allow_html=True)

        st.write("")
        c1, c2, c3, c4 = st.columns(4)
        for col, icon, label in [
            (c1, "🌍", "سياق خليجي"),
            (c2, "💬", "AI عربي"),
            (c3, "📊", "بيانات حقيقية"),
            (c4, "🛡️", "استخدام مسؤول"),
        ]:
            col.markdown(f"""
<div style="text-align:center;padding:20px 10px;background:rgba(255,255,255,0.03);
border:1px solid rgba(255,255,255,0.07);border-radius:16px;">
  <div style="font-size:1.8rem;margin-bottom:8px;">{icon}</div>
  <div style="font-size:0.85rem;color:#94A3B8;font-weight:600;">{label}</div>
</div>""", unsafe_allow_html=True)

        st.write("")
        st.markdown('<hr class="fancy-divider">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;color:#F1F5F9;'>تواصل معنا</h3>", unsafe_allow_html=True)
        ca, cb = st.columns(2)
        with ca:
            st.text_input("الاسم", placeholder="اكتب اسمك")
            st.text_input("البريد الإلكتروني", placeholder="example@email.com")
        with cb:
            st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=120)
        if st.button("إرسال", use_container_width=True):
            st.success("✅ تم الاستلام. شكراً لتواصلك!")
        st.caption("للتعاون والشراكات: يسعدنا التواصل مع الجهات التعليمية.")
