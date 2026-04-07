import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_engine import build_unis_context, chat_rushd, generate_dashboard_report, analyze_gaps, compare_unis_ai, quick_match

st.set_page_config(page_title="بوصلة", layout="wide", initial_sidebar_state="collapsed")

# ─── DESIGN TOKENS ───────────────────────────────────────────────
NAV_BG   = "#0f2922"   # dark teal nav/hero
SEC_BG   = "#1e3d38"   # slightly lighter section bg
SAGE     = "#d3e8d0"   # light sage green
CREAM    = "#f7f4ef"   # warm off-white page bg
WHITE    = "#ffffff"
INK      = "#1a2e2b"   # main text
MUTED    = "#4a6b65"   # secondary text
TEAL     = "#2EC4B6"   # brand accent
BORDER   = "rgba(15,41,34,.12)"

# ─── BASE CSS (injected once) ─────────────────────────────────────
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ overflow-x: hidden !important; }}
html, body, [class*="css"] {{
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  direction: rtl !important;
  background: {CREAM} !important;
  color: {INK} !important;
}}

/* ── Hide Streamlit chrome ── */
[data-testid="stSidebar"], [data-testid="stSidebarNav"],
button[kind="header"], [data-testid="collapsedControl"],
[data-testid="stDecoration"], footer, #MainMenu {{ display: none !important; }}

/* ── App & page containers ── */
[data-testid="stApp"], [data-testid="stAppViewContainer"] {{
  background: {CREAM} !important; overflow-x: hidden !important;
}}
[data-testid="stMain"] {{
  background: {CREAM} !important; padding: 0 !important; overflow-x: hidden !important;
}}
[data-testid="stMainBlockContainer"] {{
  padding: 0 80px !important;
  max-width: 1240px !important;
  margin: 0 auto !important;
  background: {CREAM} !important;
  overflow-x: hidden !important;
}}
[data-testid="block-container"] {{ padding: 0 !important; max-width: 100% !important; }}

/* ── RTL enforcement ── */
p, span, div, h1, h2, h3, h4, label, button, li {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; }}
input, textarea, [role="textbox"] {{ direction: rtl !important; text-align: right !important; }}
div[data-baseweb="select"] * {{ direction: rtl !important; }}

/* ── NAV ROW: break out of 80px padding + full-width dark bg ── */
[data-testid="stHorizontalBlock"]:first-of-type {{
  background: {NAV_BG} !important;
  margin-left:  -80px !important;
  margin-right: -80px !important;
  padding: 0 80px !important;
  min-height: 60px !important;
  gap: 0 !important;
  align-items: center !important;
  flex-wrap: nowrap !important;
  overflow: visible !important;
}}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] {{
  display: flex !important; align-items: center !important; padding: 0 !important; overflow: visible !important;
}}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child {{
  justify-content: flex-end !important; min-width: 120px !important;
}}
[data-testid="stHorizontalBlock"]:first-of-type button {{
  background: transparent !important; border: none !important; box-shadow: none !important;
  color: rgba(211,232,208,.55) !important;
  font-size: 13.5px !important; font-weight: 400 !important;
  padding: 0 14px !important; border-radius: 0 !important;
  white-space: nowrap !important; height: 60px !important; min-height: 60px !important;
  border-bottom: 2px solid transparent !important;
  transition: all .18s !important; width: 100% !important; letter-spacing: .2px !important;
}}
[data-testid="stHorizontalBlock"]:first-of-type button:hover {{
  color: #fff !important; background: rgba(255,255,255,.05) !important;
}}

/* ── INPUTS ── */
label {{ color: {MUTED} !important; font-size: 13px !important; font-weight: 500 !important; }}
.stTextInput > div > div {{
  background: {WHITE} !important; border: 1px solid {BORDER} !important; border-radius: 3px !important;
}}
.stTextInput > div > div:focus-within {{ border-color: {TEAL} !important; box-shadow: 0 0 0 2px rgba(46,196,182,.15) !important; }}
.stTextInput > div > div > input {{ color: {INK} !important; font-size: 14px !important; }}
input::placeholder, textarea::placeholder {{ color: #a0b5b0 !important; opacity: 1 !important; }}
.stTextArea > div > div {{
  background: {WHITE} !important; border: 1px solid {BORDER} !important; border-radius: 3px !important;
}}
div[data-baseweb="select"] > div {{
  background: {WHITE} !important; border: 1px solid {BORDER} !important; border-radius: 3px !important; color: {INK} !important;
}}
div[data-baseweb="select"] * {{ color: {INK} !important; }}
div[data-baseweb="popover"] li {{ background: {WHITE} !important; color: {INK} !important; }}
div[data-baseweb="popover"] li:hover {{ background: {SAGE} !important; }}

/* ── BUTTONS (non-nav) ── */
.stButton > button {{
  background: transparent !important; border: 1.5px solid {BORDER} !important;
  color: {INK} !important; border-radius: 2px !important;
  font-size: 14px !important; font-weight: 600 !important;
  padding: 10px 22px !important; letter-spacing: .2px !important;
  transition: all .18s !important;
}}
.stButton > button:hover {{
  background: {INK} !important; border-color: {INK} !important; color: {CREAM} !important;
}}
.stLinkButton a {{
  border: 1.5px solid {BORDER} !important; border-radius: 2px !important;
  color: {MUTED} !important; font-size: 13px !important; font-weight: 600 !important;
  padding: 8px 16px !important; background: transparent !important;
}}
.stLinkButton a:hover {{
  background: {INK} !important; color: {CREAM} !important; border-color: {INK} !important;
}}
[data-testid="stChatMessage"] {{
  background: {WHITE} !important; border: 1px solid {BORDER} !important;
  border-radius: 3px !important; direction: rtl !important; margin-bottom: 10px !important;
}}
div[data-testid="stExpander"] {{
  background: {WHITE} !important; border: 1px solid {BORDER} !important;
  border-radius: 3px !important; margin-bottom: 8px !important;
}}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-thumb {{ background: rgba(15,41,34,.2); border-radius: 0; }}

/* ── Plotly charts ── */
.js-plotly-plot .plotly {{ direction: ltr !important; }}
</style>""", unsafe_allow_html=True)

# ─── DATA ───────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent
UNIS_PATH  = ROOT / "universities.csv"
PROGS_PATH = ROOT / "programs.csv"

@st.cache_data(show_spinner=False)
def load_unis_csv(path):
    if not path.exists() or path.stat().st_size == 0: return pd.DataFrame()
    kw = dict(encoding="utf-8", engine="python", on_bad_lines="skip")
    try:
        first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].lower()
        return pd.read_csv(path, **kw) if "uni_id" in first else pd.read_csv(path, header=None, **kw)
    except: return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_csv(path):
    if not path.exists() or path.stat().st_size == 0: return pd.DataFrame()
    try: return pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="skip")
    except: return pd.DataFrame()

def normalize_unis(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    cols = ["uni_id","name_ar","name_en","country","city","type","website","admissions_url",
            "programs_url","ranking_source","extra_1","extra_2","scholarship","sch_notes","sch_url"]
    if list(df.columns) == list(range(len(df.columns))): df.columns = cols[:len(df.columns)]
    if "uni_id" in df.columns and str(df.iloc[0].get("uni_id","")).lower().strip() == "uni_id":
        df = df.iloc[1:].copy()
    for c in ["ranking_value","accreditation_notes","scholarship","sch_notes","sch_url",
              "website","admissions_url","programs_url","ranking_source"]:
        if c not in df.columns: df[c] = ""
    df["scholarship"] = df["scholarship"].fillna("").astype(str).str.strip().replace({"nan":""})
    needed = ["uni_id","name_ar","name_en","country","city","type","scholarship","sch_notes",
              "sch_url","website","admissions_url","programs_url","ranking_source",
              "ranking_value","accreditation_notes"]
    for c in needed:
        if c not in df.columns: df[c] = ""
    return df[needed].dropna(subset=["uni_id"])

def normalize_progs(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    needed = ["program_id","uni_id","level","degree_type","major_field","program_name_en",
              "program_name_ar","city","language","duration_years","tuition_notes",
              "admissions_requirements","url"]
    for c in needed:
        if c not in df.columns: df[c] = ""
    return df[needed]

def uni_has_sch(s): return str(s).strip() not in ["","No","Unknown","nan","none","None"]

unis_raw  = normalize_unis(load_unis_csv(UNIS_PATH))
progs_raw = normalize_progs(load_csv(PROGS_PATH))
N_UNIS  = len(unis_raw)
N_PROGS = len(progs_raw)
N_CTRY  = unis_raw["country"].nunique() if not unis_raw.empty else 0
N_SCH   = int(unis_raw["scholarship"].apply(uni_has_sch).sum()) if not unis_raw.empty else 0

# ─── SESSION STATE ───────────────────────────────────────────────
if "page" not in st.session_state: st.session_state.page = "الرئيسية"
PAGES = ["الرئيسية","بحث الجامعات","المقارنة","رُشد","البيانات","من نحن"]
active_idx = PAGES.index(st.session_state.page)

# ═══════════════════════════════════════════════════════════════
# NAV BAR
# ═══════════════════════════════════════════════════════════════
_nc = st.columns([1.6] + [1]*len(PAGES))
with _nc[0]:
    st.markdown(
        f'<span style="font-family:Syne,sans-serif;font-size:21px;font-weight:800;'
        f'color:#fff;letter-spacing:-.5px;white-space:nowrap;">'
        f'بو<span style="color:{TEAL};">صلة</span></span>',
        unsafe_allow_html=True)
for _i, _p in enumerate(PAGES):
    with _nc[_i + 1]:
        if st.button(_p, key=f"nav_{_p}", use_container_width=True):
            st.session_state.page = _p; st.rerun()

# Active underline via CSS
st.markdown(f"""<style>
[data-testid="stHorizontalBlock"]:first-of-type
  [data-testid="column"]:nth-child({active_idx + 2}) button {{
  color: #fff !important; font-weight: 600 !important;
  border-bottom-color: {TEAL} !important;
}}
</style>""", unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────
def v_space(px=40):
    st.markdown(f'<div style="height:{px}px;"></div>', unsafe_allow_html=True)

def section_tag(t, color=TEAL):
    st.markdown(
        f'<p style="font-size:11px;font-weight:700;letter-spacing:2.5px;'
        f'text-transform:uppercase;color:{color};margin-bottom:10px;text-align:right;">{t}</p>',
        unsafe_allow_html=True)

def section_h(t, color=INK):
    st.markdown(
        f'<h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;'
        f'color:{color};margin-bottom:24px;text-align:right;line-height:1.3;'
        f'letter-spacing:-.5px;">{t}</h2>',
        unsafe_allow_html=True)

def section_h_sm(t, color=INK):
    st.markdown(
        f'<h3 style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;'
        f'color:{color};margin-bottom:16px;text-align:right;letter-spacing:-.3px;">{t}</h3>',
        unsafe_allow_html=True)

def hr():
    st.markdown(f'<div style="height:1px;background:{BORDER};margin:44px 0;"></div>',
                unsafe_allow_html=True)

def page_header(tag, title, subtitle=""):
    # Full-width dark header band using negative-margin breakout
    sub_html = f'<p style="font-size:15px;color:rgba(211,232,208,.7);margin-top:10px;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
<div style="background:{NAV_BG};margin:0 -80px;padding:64px 80px 56px;direction:rtl;overflow:hidden;">
  <p style="font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
     color:{TEAL};margin-bottom:12px;">{tag}</p>
  <h1 style="font-family:Syne,sans-serif;font-size:38px;font-weight:800;
     color:#fff;margin:0;line-height:1.15;letter-spacing:-1px;">{title}</h1>
  {sub_html}
</div>""", unsafe_allow_html=True)

def back_btn():
    v_space(28)
    if st.button("← الرئيسية", key="back_btn"):
        st.session_state.page = "الرئيسية"; st.rerun()
    v_space(8)

# Card HTML helper
def card_html(title, body, accent=NAV_BG):
    return f"""
<div style="background:{WHITE};border:1px solid {BORDER};border-top:3px solid {accent};
     padding:28px 24px;direction:rtl;height:100%;min-height:160px;">
  <h3 style="font-family:Syne,sans-serif;font-size:17px;font-weight:800;
     color:{INK};margin-bottom:12px;text-align:right;">{title}</h3>
  <p style="font-size:13.5px;color:{MUTED};line-height:1.85;text-align:right;margin:0;">{body}</p>
</div>"""

P = st.session_state.page

# ═══════════════════════════════════════════════════════════════
# الرئيسية
# ═══════════════════════════════════════════════════════════════
if P == "الرئيسية":

    # ── HERO (full-width band via negative-margin) ──
    st.markdown(f"""
<div style="background:{NAV_BG};margin:0 -80px;padding:100px 80px 80px;direction:rtl;overflow:hidden;">
  <div style="max-width:700px;margin:0 auto;text-align:center;">
    <p style="font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
       color:{TEAL};margin-bottom:20px;">الدليل الذكي للتعليم الخليجي</p>
    <h1 style="font-family:Syne,sans-serif;font-size:72px;font-weight:800;
       color:#fff;line-height:.95;letter-spacing:-3.5px;margin-bottom:18px;">
      بو<span style="color:{TEAL};">صلة</span>
    </h1>
    <div style="width:44px;height:3px;background:{TEAL};margin:0 auto 22px;"></div>
    <p style="font-size:16px;color:rgba(211,232,208,.75);line-height:1.9;
       margin:0 auto 52px;max-width:480px;">
      اكتشف الجامعات، قارن التخصصات، واتخذ قرارك التعليمي بثقة مع مستشار ذكي يتحدث العربية
    </p>
    <div style="display:inline-flex;border:1px solid rgba(211,232,208,.2);">
      <div style="padding:22px 36px;text-align:center;border-left:1px solid rgba(211,232,208,.2);">
        <div style="font-family:Syne,sans-serif;font-size:30px;font-weight:800;color:#fff;">{N_UNIS}+</div>
        <div style="font-size:12px;color:rgba(211,232,208,.55);margin-top:5px;letter-spacing:.5px;">جامعة</div>
      </div>
      <div style="padding:22px 36px;text-align:center;border-left:1px solid rgba(211,232,208,.2);">
        <div style="font-family:Syne,sans-serif;font-size:30px;font-weight:800;color:#fff;">{N_CTRY}</div>
        <div style="font-size:12px;color:rgba(211,232,208,.55);margin-top:5px;letter-spacing:.5px;">دولة خليجية</div>
      </div>
      <div style="padding:22px 36px;text-align:center;border-left:1px solid rgba(211,232,208,.2);">
        <div style="font-family:Syne,sans-serif;font-size:30px;font-weight:800;color:#fff;">{N_PROGS}+</div>
        <div style="font-size:12px;color:rgba(211,232,208,.55);margin-top:5px;letter-spacing:.5px;">برنامج</div>
      </div>
      <div style="padding:22px 36px;text-align:center;">
        <div style="font-family:Syne,sans-serif;font-size:30px;font-weight:800;color:#fff;">{N_SCH}</div>
        <div style="font-size:12px;color:rgba(211,232,208,.55);margin-top:5px;letter-spacing:.5px;">منحة متاحة</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── SERVICES ──
    v_space(60)
    section_tag("خدماتنا")
    section_h("اختر ما يناسبك")

    svc_data = [
        ("بحث الجامعات",         "ابحث في قاعدة بيانات الجامعات الخليجية وصفّ النتائج حسب الدولة والتخصص والمنح.",       "بحث الجامعات"),
        ("مقارنة الجامعات",       "قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — المنح، الترتيب، والروابط الرسمية.",            "المقارنة"),
        ("رُشد — المستشار الذكي","تحدّث بالعربية مع مستشار AI يرشّح الجامعات المناسبة ويشرح كل توصية.",                  "رُشد"),
        ("لوحة البيانات",         "مخططات تفاعلية وتقارير إحصائية شاملة عن التعليم العالي في دول الخليج.",               "البيانات"),
        ("من نحن",                "تعرّف على منصة بوصلة ورؤيتها ورسالتها وقيمها.",                                         "من نحن"),
    ]

    # Row 1: 3 cards
    r1 = st.columns(3, gap="medium")
    for col, (title, body, dest) in zip(r1, svc_data[:3]):
        with col:
            st.markdown(card_html(title, body), unsafe_allow_html=True)
            if st.button("انتقل ←", key=f"svc_{dest}", use_container_width=True):
                st.session_state.page = dest; st.rerun()

    v_space(16)

    # Row 2: 2 cards
    r2 = st.columns([1, 1, 1], gap="medium")
    for col, (title, body, dest) in zip(r2[:2], svc_data[3:]):
        with col:
            st.markdown(card_html(title, body), unsafe_allow_html=True)
            if st.button("انتقل ←", key=f"svc2_{dest}", use_container_width=True):
                st.session_state.page = dest; st.rerun()

    # ── VISION / MISSION / VALUES (display-only → can use colored bg band) ──
    v_space(60)
    st.markdown(f"""
<div style="background:{SAGE};margin:0 -80px;padding:72px 80px 64px;direction:rtl;overflow:hidden;">
  <p style="font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
     color:{MUTED};margin-bottom:12px;text-align:right;">هويتنا</p>
  <h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;
     color:{NAV_BG};margin-bottom:40px;text-align:right;letter-spacing:-.5px;">
    رؤيتنا ورسالتنا وقيمنا</h2>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;">
    <div style="background:{WHITE};padding:28px 22px;border-top:3px solid {NAV_BG};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;
         color:{NAV_BG};margin-bottom:12px;text-align:right;">رؤيتنا</div>
      <div style="font-size:13.5px;color:{MUTED};line-height:1.85;text-align:right;">
        إعادة تعريف تجربة اختيار التعليم في الخليج — منصة ذكية توجّه الشباب نحو مستقبلهم بثقة.</div>
    </div>
    <div style="background:{WHITE};padding:28px 22px;border-top:3px solid {NAV_BG};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;
         color:{NAV_BG};margin-bottom:12px;text-align:right;">رسالتنا</div>
      <div style="font-size:13.5px;color:{MUTED};line-height:1.85;text-align:right;">
        تمكين الطلبة من اتخاذ قرارات تعليمية دقيقة باستخدام الذكاء الاصطناعي والبيانات الموثوقة.</div>
    </div>
    <div style="background:{WHITE};padding:28px 22px;border-top:3px solid {TEAL};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;
         color:{NAV_BG};margin-bottom:12px;text-align:right;">قيمنا</div>
      <div style="font-size:13.5px;color:{MUTED};line-height:1.85;text-align:right;">
        الوضوح · العدالة · التمكين · الابتكار · الموثوقية</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
    v_space(56)


# ═══════════════════════════════════════════════════════════════
# بحث الجامعات
# ═══════════════════════════════════════════════════════════════
elif P == "بحث الجامعات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    page_header("الاستكشاف", "بحث الجامعات")
    back_btn()

    # Search + filters
    q = st.text_input("", placeholder="ابحث عن جامعة، مدينة، أو دولة...", label_visibility="collapsed").strip().lower()
    v_space(12)

    c1, c2, c3, c4, c5 = st.columns([1.2, 1, 1, 1.2, 1], gap="small")
    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c1.selectbox("الدولة",   ["الكل"] + countries)
    types_    = sorted([x for x in unis["type"].unique() if str(x).strip()])
    uni_type  = c2.selectbox("النوع",    ["الكل"] + types_)
    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c3.selectbox("المرحلة", ["الكل"] + levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c4.selectbox("التخصص",  ["الكل"] + majors_)
    yn        = c5.selectbox("المنح",   ["الكل", "متاحة", "غير متاحة"])

    has_searched = bool(q) or any(x != "الكل" for x in [country, uni_type, level, major, yn])

    if not has_searched:
        v_space(60)
        st.markdown(f"""
<div style="text-align:center;direction:rtl;">
  <p style="font-size:40px;margin-bottom:16px;">🔍</p>
  <p style="font-size:16px;font-weight:600;color:{MUTED};margin-bottom:6px;">ابحث للبدء</p>
  <p style="font-size:13.5px;color:#a0b5b0;">اكتب اسم جامعة أو دولة، أو استخدم الفلاتر أعلاه</p>
</div>""", unsafe_allow_html=True)
        v_space(60)
    else:
        f = unis.copy()
        if country  != "الكل": f = f[f["country"] == country]
        if uni_type != "الكل": f = f[f["type"] == uni_type]
        if yn == "متاحة":      f = f[f["scholarship"].apply(uni_has_sch)]
        if yn == "غير متاحة":  f = f[~f["scholarship"].apply(uni_has_sch)]
        if q:
            mask = (f["name_en"].str.lower().str.contains(q, na=False) |
                    f["name_ar"].str.lower().str.contains(q, na=False) |
                    f["city"].str.lower().str.contains(q, na=False))
            f = f[mask]
        if (major != "الكل" or level != "الكل") and not progs.empty:
            pm = progs.copy()
            if major != "الكل": pm = pm[pm["major_field"] == major]
            if level != "الكل": pm = pm[pm["level"] == level]
            f = f[f["uni_id"].isin(pm["uni_id"].unique())]

        v_space(20)
        st.markdown(f'<p style="font-size:13px;font-weight:600;color:{MUTED};">{len(f)} نتيجة</p>',
                    unsafe_allow_html=True)
        v_space(8)

        if f.empty:
            st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
        else:
            for _, row in f.head(30).iterrows():
                is_pub = str(row["type"]).strip().lower() in ["public","حكومية"]
                t_style = f"background:rgba(15,41,34,.08);color:{MUTED};" if is_pub else f"background:rgba(15,41,34,.05);color:{INK};"
                t_label = "حكومية" if is_pub else "خاصة"
                sch = f'<span style="padding:2px 10px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;margin-right:6px;">منحة دراسية</span>' if uni_has_sch(str(row["scholarship"])) else ""
                langs = ""
                if not progs.empty:
                    for lg in progs[progs["uni_id"]==str(row["uni_id"])]["language"].dropna().unique()[:2]:
                        langs += f'<span style="padding:2px 10px;font-size:11px;font-weight:600;background:rgba(46,196,182,.1);color:{MUTED};margin-right:6px;">{lg}</span>'
                links = ""
                if str(row.get("website","")).strip():
                    links += f'<a href="{row["website"]}" target="_blank" style="font-size:12.5px;font-weight:600;color:{TEAL};text-decoration:none;padding:5px 14px;border:1px solid rgba(46,196,182,.3);white-space:nowrap;margin-right:8px;">الموقع الرسمي</a>'
                if str(row.get("admissions_url","")).strip():
                    links += f'<a href="{row["admissions_url"]}" target="_blank" style="font-size:12.5px;font-weight:600;color:{MUTED};text-decoration:none;padding:5px 14px;border:1px solid {BORDER};white-space:nowrap;">القبول</a>'
                st.markdown(f"""
<div style="background:{WHITE};border-bottom:1px solid {BORDER};padding:18px 0;
     display:flex;justify-content:space-between;align-items:center;gap:16px;direction:rtl;">
  <div style="flex:1;min-width:0;">
    <div style="font-size:14.5px;font-weight:700;color:{INK};margin-bottom:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
      {row["name_ar"]}
      <span style="font-weight:400;color:#a0b5b0;font-size:12.5px;"> — {row["name_en"]}</span>
    </div>
    <div style="font-size:12.5px;color:#a0b5b0;margin-bottom:10px;">{row["city"]}, {row["country"]}</div>
    <div><span style="padding:2px 10px;font-size:11px;font-weight:600;{t_style}margin-left:6px;">{t_label}</span>{sch}{langs}</div>
  </div>
  <div style="display:flex;align-items:center;gap:0;flex-shrink:0;">{links}</div>
</div>""", unsafe_allow_html=True)
    v_space(56)


# ═══════════════════════════════════════════════════════════════
# المقارنة
# ═══════════════════════════════════════════════════════════════
elif P == "المقارنة":
    unis = unis_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    page_header("التقييم المقارن", "مقارنة الجامعات")
    back_btn()

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + ", " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country","city","name_en"], na_position="last")

    selected = st.multiselect("اختر من ٢ إلى ٤ جامعات",
                              options=unis["uni_id"].tolist(),
                              format_func=lambda x: label_map.get(str(x), str(x)),
                              max_selections=4)
    if len(selected) < 2:
        v_space(20)
        st.info("يرجى اختيار جامعتين على الأقل للمقارنة.")
        v_space(56); st.stop()

    comp = unis[unis["uni_id"].isin(selected)].copy()
    v_space(28)
    cols_c = st.columns(len(selected), gap="medium")
    for i, uid in enumerate(selected):
        row = comp[comp["uni_id"] == uid].iloc[0]
        with cols_c[i]:
            sch  = str(row.get("scholarship","")).strip() or "—"
            rank = (str(row.get("ranking_source","")).strip() + " " + str(row.get("ranking_value","")).strip()).strip() or "—"
            st.markdown(f"""
<div style="background:{WHITE};border:1px solid {BORDER};border-top:3px solid {NAV_BG};padding:22px 20px;direction:rtl;">
  <div style="font-family:Syne,sans-serif;font-size:15px;font-weight:800;
     color:{INK};margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid {BORDER};
     text-align:right;">{row['name_ar']}</div>
  <div style="font-size:13px;color:#a0b5b0;margin-bottom:4px;text-align:right;">{row['city']}, {row['country']}</div>
  <div style="height:1px;background:{BORDER};margin:12px 0;"></div>
  <div style="display:flex;justify-content:space-between;padding:7px 0;"><span style="font-size:12px;color:{MUTED};">النوع</span><span style="font-size:13px;font-weight:600;">{row['type']}</span></div>
  <div style="display:flex;justify-content:space-between;padding:7px 0;border-top:1px solid {BORDER};"><span style="font-size:12px;color:{MUTED};">المنح</span><span style="font-size:13px;font-weight:600;max-width:55%;text-align:left;overflow:hidden;text-overflow:ellipsis;">{sch}</span></div>
  <div style="display:flex;justify-content:space-between;padding:7px 0;border-top:1px solid {BORDER};"><span style="font-size:12px;color:{MUTED};">الترتيب</span><span style="font-size:13px;font-weight:600;">{rank}</span></div>
</div>""", unsafe_allow_html=True)
            v_space(8)
            if str(row.get("website","")).strip():        st.link_button("الموقع الرسمي",      row["website"],        use_container_width=True)
            if str(row.get("admissions_url","")).strip(): st.link_button("القبول والتسجيل",    row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url","")).strip():   st.link_button("البرامج الأكاديمية", row["programs_url"],   use_container_width=True)

    progs = progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        hr()
        section_h_sm("البرامج المتاحة")
        comp_progs = progs[progs["uni_id"].isin(selected)].copy()
        if comp_progs.empty:
            st.info("لا تتوفر بيانات برامج للجامعات المختارة.")
        else:
            show_cols = [c for c in ["uni_id","program_name_ar","program_name_en","level","major_field","language","duration_years"] if c in comp_progs.columns]
            rename_map = {"uni_id":"الجامعة","program_name_ar":"البرنامج","program_name_en":"Program",
                          "level":"المرحلة","major_field":"التخصص","language":"اللغة","duration_years":"المدة"}
            display_df = comp_progs[show_cols].rename(columns=rename_map)
            if "الجامعة" in display_df.columns:
                id_to_ar = dict(zip(unis["uni_id"], unis["name_ar"]))
                display_df["الجامعة"] = display_df["الجامعة"].map(id_to_ar).fillna(display_df["الجامعة"])
            st.dataframe(display_df, use_container_width=True, hide_index=True)

    hr()
    section_h_sm("المقارنة الذكية")
    profile_txt = st.text_input("", placeholder="ملفك الأكاديمي (اختياري) — مثال: طالب هندسة، IELTS 6.5",
                                 key="comp_profile", label_visibility="collapsed")
    if st.button("اطلب مقارنة ذكية", use_container_width=True, key="btn_compare_ai"):
        unis_data = [comp[comp["uni_id"]==uid].iloc[0].to_dict() for uid in selected if uid in comp["uni_id"].values]
        with st.spinner("جاري تحليل الجامعات..."):
            ai_result = compare_unis_ai(unis_data, profile_txt)
        st.markdown(f"""
<div style="background:{SAGE};border-top:2px solid {TEAL};padding:22px 24px;
     margin-top:16px;line-height:2;color:{INK};direction:rtl;">
  <span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
     color:{TEAL};display:block;margin-bottom:10px;">المقارنة الذكية</span>{ai_result}</div>""",
            unsafe_allow_html=True)
    v_space(56)


# ═══════════════════════════════════════════════════════════════
# رُشد
# ═══════════════════════════════════════════════════════════════
elif P == "رُشد":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    page_header("المستشار الأكاديمي الذكي", "رُشد",
                "تحدّث بالعربية — رُشد يفهم ملفك ويرشّح الجامعات المناسبة")
    back_btn()

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    section_h_sm("التحليل السريع")
    qm_c1, qm_c2, qm_c3 = st.columns(3, gap="medium")
    countries_list = sorted([x for x in unis["country"].unique() if str(x).strip()])
    qm_country = qm_c1.selectbox("الدولة المفضلة", ["الكل"] + countries_list, key="qm_country")
    qm_major   = qm_c2.text_input("التخصص المطلوب", placeholder="مثال: هندسة الحاسب", key="qm_major")
    qm_ielts   = qm_c3.text_input("درجة IELTS",     placeholder="مثال: 6.5",          key="qm_ielts")
    v_space(4)
    if st.button("حلّل بسرعة", use_container_width=True, key="btn_qm"):
        if not qm_major.strip(): st.warning("يرجى إدخال التخصص.")
        else:
            with st.spinner("جاري التحليل..."):
                res = quick_match({"country":qm_country,"major":qm_major,"ielts":qm_ielts or "غير محدد"},
                                  st.session_state.unis_context)
            top3 = res.get("top_3",[]); advice = res.get("advice",""); missing = res.get("missing",[])
            if top3:
                qr = st.columns(len(top3[:3]), gap="medium")
                for i, item in enumerate(top3[:3]):
                    uid = item.get("uni_id",""); nm = item.get("name_ar", uid)
                    rsn = item.get("reason",""); fit = item.get("fit","مناسب")
                    ur = unis[unis["uni_id"]==uid]
                    cc = ""; st_tag = ""
                    if not ur.empty:
                        r = ur.iloc[0]; cc = f"{r.get('city','')}, {r.get('country','')}"
                        if uni_has_sch(str(r.get("scholarship",""))): st_tag = f'<span style="padding:2px 10px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;">منحة</span> '
                    with qr[i]:
                        st.markdown(f"""
<div style="background:{WHITE};border:1px solid {BORDER};border-top:3px solid {NAV_BG};padding:20px;direction:rtl;">
  <div style="font-size:14.5px;font-weight:700;color:{INK};margin-bottom:4px;">{nm}</div>
  <div style="font-size:12px;color:#a0b5b0;margin-bottom:10px;">{cc}</div>
  <div style="font-size:13px;color:{MUTED};line-height:1.75;margin-bottom:12px;">{rsn}</div>
  <div>{st_tag}<span style="padding:2px 10px;font-size:11px;font-weight:600;background:rgba(15,41,34,.07);color:{MUTED};">{fit}</span></div>
</div>""", unsafe_allow_html=True)
            if advice:
                st.markdown(f'<div style="background:{SAGE};border-top:2px solid {TEAL};padding:20px 22px;margin-top:14px;line-height:2;color:{INK};direction:rtl;"><span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{TEAL};display:block;margin-bottom:8px;">نصيحة رُشد</span>{advice}</div>', unsafe_allow_html=True)
            if missing:
                mh = "".join([f'<span style="padding:2px 10px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;margin:3px;">{m}</span>' for m in missing])
                st.markdown(f'<div style="margin-top:10px;direction:rtl;"><span style="color:#a0b5b0;font-size:13px;margin-left:8px;">قد تحتاج إلى:</span>{mh}</div>', unsafe_allow_html=True)

    hr()
    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{"role":"assistant","content":"مرحباً، أنا رُشد.\n\nأخبرني عن نفسك:\n- التخصص الذي تريده\n- الدولة المفضلة\n- معدلك التقريبي\n- هل عندك IELTS وكم درجتك؟\n\nوسأرشّح لك الجامعات المناسبة."}]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"], avatar="🧭" if msg["role"]=="assistant" else "🎓"):
            st.markdown(msg["content"])

    if ui := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":ui})
        with st.chat_message("user", avatar="🎓"): st.markdown(ui)
        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner(""):
                hist = [m for m in st.session_state.rushd_messages if not (m["role"]=="assistant" and "مرحباً" in m["content"])]
                rep = chat_rushd(hist, st.session_state.unis_context)
            st.markdown(rep)
            st.session_state.rushd_messages.append({"role":"assistant","content":rep})

    if len(st.session_state.rushd_messages) > 1:
        v_space(8)
        if st.button("محادثة جديدة"): st.session_state.rushd_messages=[]; st.rerun()
    v_space(56)


# ═══════════════════════════════════════════════════════════════
# البيانات
# ═══════════════════════════════════════════════════════════════
elif P == "البيانات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("لا تتوفر بيانات."); st.stop()

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    page_header("الإحصاء والتحليل", "لوحة البيانات")

    # Stats band (sage, full-width)
    st.markdown(f"""
<div style="background:{SAGE};margin:0 -80px;padding:0 80px;direction:rtl;overflow:hidden;">
  <div style="display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid rgba(15,41,34,.08);">
    <div style="padding:32px 0;text-align:center;border-left:1px solid rgba(15,41,34,.08);">
      <div style="font-family:Syne,sans-serif;font-size:34px;font-weight:800;color:{NAV_BG};line-height:1;">{N_UNIS}</div>
      <div style="font-size:12.5px;color:{MUTED};margin-top:6px;letter-spacing:.3px;">إجمالي الجامعات</div>
    </div>
    <div style="padding:32px 0;text-align:center;border-left:1px solid rgba(15,41,34,.08);">
      <div style="font-family:Syne,sans-serif;font-size:34px;font-weight:800;color:{NAV_BG};line-height:1;">{N_PROGS}</div>
      <div style="font-size:12.5px;color:{MUTED};margin-top:6px;letter-spacing:.3px;">إجمالي البرامج</div>
    </div>
    <div style="padding:32px 0;text-align:center;border-left:1px solid rgba(15,41,34,.08);">
      <div style="font-family:Syne,sans-serif;font-size:34px;font-weight:800;color:{NAV_BG};line-height:1;">{with_sch}</div>
      <div style="font-size:12.5px;color:{MUTED};margin-top:6px;letter-spacing:.3px;">تقدم منحاً</div>
    </div>
    <div style="padding:32px 0;text-align:center;">
      <div style="font-family:Syne,sans-serif;font-size:34px;font-weight:800;color:{NAV_BG};line-height:1;">{N_CTRY}</div>
      <div style="font-size:12.5px;color:{MUTED};margin-top:6px;letter-spacing:.3px;">دولة خليجية</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    back_btn()

    T    = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Sans Arabic", color=MUTED),
                margin=dict(l=8, r=8, t=36, b=8), height=280)
    T_sm = {**T, "height": 260}

    ch1, ch2, ch3 = st.columns(3, gap="medium")
    with ch1:
        fig = px.bar(x=list(by_country.values()), y=list(by_country.keys()),
                     orientation="h", title="الجامعات حسب الدولة",
                     color_discrete_sequence=[NAV_BG])
        fig.update_layout(**T); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        fig = px.pie(values=list(by_type.values()), names=list(by_type.keys()),
                     title="حكومية / خاصة", hole=0.55,
                     color_discrete_sequence=[TEAL, NAV_BG, SEC_BG])
        fig.update_layout(**T); fig.update_traces(textfont_color="white")
        st.plotly_chart(fig, use_container_width=True)
    with ch3:
        if top_fields:
            fig = px.bar(x=list(top_fields.keys()), y=list(top_fields.values()),
                         title="أبرز التخصصات", color_discrete_sequence=[SEC_BG])
            fig.update_layout(**T, xaxis_tickangle=-30); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    ch4, ch5 = st.columns(2, gap="medium")
    with ch4:
        pct = round(with_sch / max(len(unis),1) * 100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=pct,
            title={"text":"% نسبة الجامعات التي تقدم منحاً",
                   "font":{"family":"IBM Plex Sans Arabic","color":MUTED,"size":12}},
            number={"font":{"color":NAV_BG,"family":"IBM Plex Sans Arabic"}},
            gauge={"axis":{"range":[0,100],"tickcolor":SAGE},"bar":{"color":NAV_BG},
                   "bgcolor":"rgba(0,0,0,0)","bordercolor":SAGE,
                   "steps":[{"range":[0,100],"color":SAGE}]}))
        fig.update_layout(**T_sm)
        st.plotly_chart(fig, use_container_width=True)
    with ch5:
        if by_lang:
            fig = px.bar(x=list(by_lang.keys()), y=list(by_lang.values()),
                         title="لغات الدراسة", color_discrete_sequence=[SEC_BG])
            fig.update_layout(**T_sm); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    hr()
    section_h_sm("توزيع المنح حسب الدولة")
    if not unis.empty and "scholarship" in unis.columns:
        sch_data = []
        for _, row in unis.iterrows():
            ctry = str(row.get("country","")).strip(); sch = str(row.get("scholarship","")).strip()
            if not ctry or ctry=="nan": continue
            for cat in ["Local","GCC","International"]:
                sch_data.append({"الدولة":ctry,"نوع المنحة":cat,"عدد":1 if cat in sch else 0})
        sch_df = pd.DataFrame(sch_data).groupby(["الدولة","نوع المنحة"],as_index=False)["عدد"].sum()
        sch_df = sch_df[sch_df["عدد"]>0]
        if not sch_df.empty:
            fig_sch = px.bar(sch_df, x="عدد", y="الدولة", color="نوع المنحة",
                             orientation="h", barmode="stack",
                             color_discrete_map={"Local":TEAL,"GCC":NAV_BG,"International":SEC_BG})
            fig_sch.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(family="IBM Plex Sans Arabic",color=MUTED),
                                  margin=dict(l=8,r=8,t=36,b=8), height=300,
                                  legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color=MUTED)))
            fig_sch.update_traces(marker_line_width=0)
            st.plotly_chart(fig_sch, use_container_width=True)

    hr()
    col_r, col_g = st.columns(2, gap="medium")
    with col_r:
        section_h_sm("التقرير التحليلي الذكي")
        st.markdown(f'<p style="font-size:13.5px;color:{MUTED};margin-bottom:16px;text-align:right;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير", use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                rep = generate_dashboard_report({"total_unis":len(unis),"by_country":by_country,"by_type":by_type,"top_fields":top_fields,"by_language":by_lang,"with_scholarships":with_sch,"total_progs":len(progs)})
            st.markdown(f'<div style="background:{SAGE};border-top:2px solid {TEAL};padding:20px 22px;margin-top:14px;line-height:2;color:{INK};direction:rtl;"><span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{TEAL};display:block;margin-bottom:8px;">التقرير</span>{rep}</div>', unsafe_allow_html=True)
    with col_g:
        section_h_sm("تحليل الفجوات التعليمية")
        st.markdown(f'<p style="font-size:13.5px;color:{MUTED};margin-bottom:16px;text-align:right;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div style="background:#FFFBEB;border-top:2px solid #FDE68A;padding:20px 22px;margin-top:14px;line-height:2;color:{INK};direction:rtl;">{gaps}</div>', unsafe_allow_html=True)
    v_space(56)


# ═══════════════════════════════════════════════════════════════
# من نحن
# ═══════════════════════════════════════════════════════════════
elif P == "من نحن":
    page_header("هويتنا", "من نحن")

    # About text (sage band)
    st.markdown(f"""
<div style="background:{SAGE};margin:0 -80px;padding:72px 80px 64px;direction:rtl;overflow:hidden;">
  <p style="font-size:19px;font-weight:700;color:{NAV_BG};margin-bottom:20px;
     text-align:right;line-height:1.55;max-width:680px;margin-right:auto;">
    منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.
  </p>
  <p style="font-size:15.5px;color:{MUTED};line-height:1.95;text-align:right;max-width:680px;margin-right:auto;">
    جاءت فكرة بوصلة استجابةً لتحدٍ واقعي — تشتّت المعلومات وصعوبة المقارنة بين الجامعات وتعدد المصادر غير الموثوقة.
  </p>
  <p style="font-size:15.5px;color:{MUTED};line-height:1.95;text-align:right;margin-top:16px;max-width:680px;margin-right:auto;">
    نجمع البيانات التعليمية الخليجية ونقدّمها بطريقة مبسّطة، مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على اتخاذ قراره بثقة.
  </p>
</div>
""", unsafe_allow_html=True)

    # Values (dark band)
    st.markdown(f"""
<div style="background:{NAV_BG};margin:0 -80px;padding:72px 80px 64px;direction:rtl;overflow:hidden;">
  <p style="font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
     color:{TEAL};margin-bottom:12px;text-align:right;">قيمنا</p>
  <h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;
     color:#fff;margin-bottom:40px;text-align:right;letter-spacing:-.5px;">ما يحركنا</h2>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
    <div style="background:rgba(255,255,255,.05);padding:24px 18px;border-top:2px solid {TEAL};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#fff;margin-bottom:8px;text-align:right;">الوضوح</div>
      <div style="font-size:13px;color:rgba(211,232,208,.65);text-align:right;">تبسيط القرار التعليمي</div>
    </div>
    <div style="background:rgba(255,255,255,.05);padding:24px 18px;border-top:2px solid {TEAL};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#fff;margin-bottom:8px;text-align:right;">العدالة</div>
      <div style="font-size:13px;color:rgba(211,232,208,.65);text-align:right;">عرض الخيارات دون تحيّز</div>
    </div>
    <div style="background:rgba(255,255,255,.05);padding:24px 18px;border-top:2px solid {TEAL};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#fff;margin-bottom:8px;text-align:right;">التمكين</div>
      <div style="font-size:13px;color:rgba(211,232,208,.65);text-align:right;">فهم الذات قبل التخصص</div>
    </div>
    <div style="background:rgba(255,255,255,.05);padding:24px 18px;border-top:2px solid {TEAL};direction:rtl;">
      <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#fff;margin-bottom:8px;text-align:right;">الابتكار</div>
      <div style="font-size:13px;color:rgba(211,232,208,.65);text-align:right;">AI في خدمة التعليم</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Contact
    back_btn()
    section_tag("تواصل")
    section_h("تواصل معنا")
    ca, cb = st.columns(2, gap="medium")
    with ca:
        st.text_input("الاسم",             placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني", placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=114)
    v_space(4)
    if st.button("إرسال", use_container_width=True):
        st.success("تم الاستلام. شكراً لتواصلك.")
    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
    v_space(56)
