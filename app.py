import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_engine import build_unis_context, chat_rushd, generate_dashboard_report, analyze_gaps, compare_unis_ai, quick_match

st.set_page_config(page_title="بوصلة", layout="wide", initial_sidebar_state="collapsed")

# ─── Base CSS ───
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

:root{--teal:#2EC4B6;--dark:#17252A;--mid:#2B7A77;--pale:#EEF8F8;--border:rgba(23,37,42,.10);--muted:#3B7A77;--white:#FEFFFF;--r:12px;}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'IBM Plex Sans Arabic',sans-serif!important;direction:rtl!important;color:#17252A!important;}

/* Hide chrome */
[data-testid="stSidebar"],[data-testid="stSidebarNav"],
button[kind="header"],[data-testid="collapsedControl"],
[data-testid="stDecoration"],footer,#MainMenu{display:none!important;}

/* Grey outer bg */
[data-testid="stApp"],[data-testid="stAppViewContainer"]{background:#E8EDED!important;}
[data-testid="stMain"]{background:#E8EDED!important;padding:20px!important;}

/* White centered card — NO overflow:hidden so scroll works */
[data-testid="stMainBlockContainer"]{
  max-width:1100px!important;width:100%!important;
  margin:0 auto!important;padding:0!important;
  background:#FEFFFF!important;
  border:1.5px solid #C8E6E4!important;
  border-radius:18px!important;
  box-shadow:0 2px 20px rgba(46,196,182,.09)!important;
}
[data-testid="block-container"]{padding:0!important;max-width:100%!important;}

/* Force RTL + font everywhere */
p,span,div,h1,h2,h3,label,button{font-family:'IBM Plex Sans Arabic',sans-serif!important;}
input,textarea,[role="textbox"]{direction:rtl!important;text-align:right!important;}
div[data-baseweb="select"] *{direction:rtl!important;}
label{color:var(--muted)!important;font-size:13px!important;font-weight:500!important;}

/* ── Inputs ── */
.stTextInput>div>div{background:#fff!important;border:1.5px solid var(--border)!important;border-radius:10px!important;}
.stTextInput>div>div:focus-within{border-color:var(--teal)!important;box-shadow:0 0 0 3px rgba(46,196,182,.12)!important;}
.stTextInput>div>div>input{color:#17252A!important;background:transparent!important;}
input::placeholder,textarea::placeholder{color:#9AACAC!important;opacity:1!important;}
.stTextArea>div>div{background:#fff!important;border:1.5px solid var(--border)!important;border-radius:10px!important;}
div[data-baseweb="select"]>div{background:#fff!important;border:1.5px solid var(--border)!important;border-radius:10px!important;}
div[data-baseweb="select"] *{color:#17252A!important;}
div[data-baseweb="popover"] li{background:#fff!important;color:#17252A!important;}
div[data-baseweb="popover"] li:hover{background:var(--pale)!important;color:var(--teal)!important;}

/* ── Buttons ── */
.stButton>button{
  background:#fff!important;border:1.5px solid var(--border)!important;
  color:#17252A!important;border-radius:10px!important;font-weight:600!important;
  font-family:'IBM Plex Sans Arabic',sans-serif!important;font-size:13px!important;
  padding:10px 18px!important;transition:all .18s!important;
}
.stButton>button:hover{background:var(--pale)!important;border-color:var(--teal)!important;color:var(--teal)!important;}
.stLinkButton a{background:rgba(46,196,182,.07)!important;border:1.5px solid rgba(46,196,182,.25)!important;color:var(--mid)!important;border-radius:9px!important;font-weight:600!important;font-size:12px!important;}
.stLinkButton a:hover{background:var(--teal)!important;color:var(--dark)!important;}
[data-testid="stChatMessage"]{background:#fff!important;border:1.5px solid var(--border)!important;border-radius:var(--r)!important;direction:rtl!important;margin-bottom:8px!important;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(46,196,182,.3);border-radius:4px;}
</style>""", unsafe_allow_html=True)

# ─── Data ───
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
    cols = ["uni_id","name_ar","name_en","country","city","type","website","admissions_url","programs_url","ranking_source","extra_1","extra_2","scholarship","sch_notes","sch_url"]
    if list(df.columns) == list(range(len(df.columns))): df.columns = cols[:len(df.columns)]
    if "uni_id" in df.columns and str(df.iloc[0].get("uni_id","")).lower().strip() == "uni_id": df = df.iloc[1:].copy()
    for c in ["ranking_value","accreditation_notes","scholarship","sch_notes","sch_url","website","admissions_url","programs_url","ranking_source"]:
        if c not in df.columns: df[c] = ""
    df["scholarship"] = df["scholarship"].fillna("").astype(str).str.strip().replace({"nan":""})
    needed = ["uni_id","name_ar","name_en","country","city","type","scholarship","sch_notes","sch_url","website","admissions_url","programs_url","ranking_source","ranking_value","accreditation_notes"]
    for c in needed:
        if c not in df.columns: df[c] = ""
    return df[needed].dropna(subset=["uni_id"])

def normalize_progs(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    needed = ["program_id","uni_id","level","degree_type","major_field","program_name_en","program_name_ar","city","language","duration_years","tuition_notes","admissions_requirements","url"]
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

# ── Session state ──
if "page" not in st.session_state: st.session_state.page = "الرئيسية"
PAGES = ["الرئيسية","بحث الجامعات","المقارنة","رُشد","البيانات","من نحن"]
active_idx = PAGES.index(st.session_state.page)

# ── Nav: logo col + nav button cols ──
_nc = st.columns([1.6, 1, 1, 1, 1, 1, 1])
with _nc[0]:
    st.markdown('<p style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#FEFFFF;margin:0;line-height:60px;white-space:nowrap;padding-right:4px;">بو<span style="color:#2EC4B6;">صلة</span></p>', unsafe_allow_html=True)
for _i, _name in enumerate(PAGES):
    with _nc[_i + 1]:
        if st.button(_name, key=f"nav_{_name}", use_container_width=True):
            st.session_state.page = _name; st.rerun()

# Style the nav row (first stHorizontalBlock in the page)
st.markdown(f"""<style>
[data-testid="stHorizontalBlock"]:first-of-type{{
  background:#17252A!important;
  padding:8px 24px!important;
  gap:2px!important;
  align-items:center!important;
  min-height:60px!important;
  border-radius:16px 16px 0 0!important;
  flex-wrap:nowrap!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type button{{
  background:transparent!important;border:none!important;box-shadow:none!important;
  color:rgba(255,255,255,.5)!important;font-size:13px!important;font-weight:500!important;
  font-family:'IBM Plex Sans Arabic',sans-serif!important;
  padding:7px 8px!important;border-radius:8px!important;
  white-space:nowrap!important;height:36px!important;min-height:36px!important;
  transition:all .15s!important;width:100%!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type button:hover{{
  background:rgba(255,255,255,.1)!important;color:#fff!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:nth-child({active_idx+2}) button{{
  background:#2EC4B6!important;color:#17252A!important;font-weight:700!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child p{{
  font-family:'Syne',sans-serif!important;font-size:20px!important;font-weight:800!important;
  color:#FEFFFF!important;
}}
</style>""", unsafe_allow_html=True)

st.markdown('<div style="height:1px;background:#DEF2F1;margin:0;"></div>', unsafe_allow_html=True)

# ── Helpers ──
P = st.session_state.page

def section_tag(t):   st.markdown(f'<p style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2EC4B6;margin-bottom:6px;text-align:right;">{t}</p>', unsafe_allow_html=True)
def section_h(t):     st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:#17252A;letter-spacing:-.5px;margin-bottom:22px;text-align:right;">{t}</h2>', unsafe_allow_html=True)
def section_h_sm(t):  st.markdown(f'<h3 style="font-family:Syne,sans-serif;font-size:18px;font-weight:800;color:#17252A;letter-spacing:-.3px;margin-bottom:14px;text-align:right;">{t}</h3>', unsafe_allow_html=True)
def divider():        st.markdown('<hr style="height:1px;background:rgba(23,37,42,.08);border:none;margin:36px 0;">', unsafe_allow_html=True)
def page_start():     st.markdown('<div style="padding:36px 44px 52px;direction:rtl;">', unsafe_allow_html=True)
def page_end():       st.markdown('</div>', unsafe_allow_html=True)
def back_btn():
    if st.button("← الرئيسية", key="back_btn"):
        st.session_state.page = "الرئيسية"; st.rerun()
    st.markdown('<div style="margin-bottom:24px;"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# الرئيسية
# ══════════════════════════════════════════════
if P == "الرئيسية":
    page_start()

    # Hero
    st.markdown(f"""
<div style="text-align:center;padding:48px 0 40px;direction:rtl;">
  <div style="display:inline-flex;align-items:center;gap:7px;background:rgba(46,196,182,.1);border:1px solid rgba(46,196,182,.25);border-radius:100px;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#2B7A77;margin-bottom:24px;">
    <span style="width:5px;height:5px;border-radius:50%;background:#2EC4B6;display:inline-block;animation:pulse 2s infinite;"></span>
    الدليل الذكي للتعليم الخليجي
  </div>
  <div style="font-family:Syne,sans-serif;font-size:82px;font-weight:800;color:#17252A;line-height:.95;letter-spacing:-4px;margin-bottom:20px;">
    بو<span style="color:#2EC4B6;">صلة</span>
  </div>
  <div style="width:52px;height:3px;background:#2EC4B6;border-radius:2px;margin:0 auto 20px;"></div>
  <div style="font-size:16px;color:#3B7A77;line-height:1.85;max-width:500px;margin:0 auto 36px;">
    اكتشف الجامعات، قارن التخصصات، واتخذ قرارك التعليمي بثقة<br>مع مستشار ذكي يتحدث العربية
  </div>
  <div style="display:flex;justify-content:center;">
    <div style="display:flex;border:1.5px solid #DEF2F1;border-radius:14px;overflow:hidden;">
      <div style="padding:16px 28px;text-align:center;border-left:1.5px solid #DEF2F1;">
        <div style="font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#17252A;">{N_UNIS}+</div>
        <div style="font-size:11px;color:#9AACAC;margin-top:3px;">جامعة</div>
      </div>
      <div style="padding:16px 28px;text-align:center;border-left:1.5px solid #DEF2F1;">
        <div style="font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#17252A;">{N_CTRY}</div>
        <div style="font-size:11px;color:#9AACAC;margin-top:3px;">دولة خليجية</div>
      </div>
      <div style="padding:16px 28px;text-align:center;border-left:1.5px solid #DEF2F1;">
        <div style="font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#17252A;">{N_PROGS}+</div>
        <div style="font-size:11px;color:#9AACAC;margin-top:3px;">برنامج</div>
      </div>
      <div style="padding:16px 28px;text-align:center;">
        <div style="font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#17252A;">{N_SCH}</div>
        <div style="font-size:11px;color:#9AACAC;margin-top:3px;">منحة متاحة</div>
      </div>
    </div>
  </div>
</div>
<style>@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}</style>
""", unsafe_allow_html=True)

    divider()

    # Section title centered
    st.markdown('<p style="text-align:center;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2EC4B6;margin-bottom:10px;">خدماتنا</p>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:Syne,sans-serif;font-size:24px;font-weight:800;color:#17252A;text-align:center;margin-bottom:28px;letter-spacing:-.5px;">اختر ما يناسبك</h2>', unsafe_allow_html=True)

    # 3 nav cards
    c1, c2, c3 = st.columns(3)
    cards = [
        ("بحث الجامعات", "🔍", "ابحث في قاعدة بيانات الجامعات الخليجية وصفّ النتائج حسب الدولة والتخصص والمنح.", "بحث الجامعات"),
        ("مقارنة الجامعات", "⚖️", "قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — المنح، الترتيب، والروابط الرسمية.", "المقارنة"),
        ("رُشد — المستشار الذكي", "🧭", "تحدّث بالعربية مع مستشار AI يرشّح لك الجامعات ويشرح أسباب كل توصية.", "رُشد"),
    ]
    for col, (title, icon, body, dest) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
<div style="border:1.5px solid #DEF2F1;border-radius:16px;padding:28px 22px;background:#fff;min-height:200px;text-align:right;direction:rtl;">
  <div style="font-size:28px;margin-bottom:14px;">{icon}</div>
  <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#17252A;margin-bottom:10px;">{title}</div>
  <div style="font-size:13px;color:#3B7A77;line-height:1.75;">{body}</div>
</div>
""", unsafe_allow_html=True)
            if st.button(f"انتقل ←", key=f"card_{dest}", use_container_width=True):
                st.session_state.page = dest; st.rerun()

    divider()

    # Additional nav row
    c4, c5 = st.columns(2)
    with c4:
        st.markdown("""
<div style="border:1.5px solid #DEF2F1;border-radius:16px;padding:28px 22px;background:#fff;text-align:right;direction:rtl;">
  <div style="font-size:28px;margin-bottom:14px;">📊</div>
  <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#17252A;margin-bottom:10px;">لوحة البيانات</div>
  <div style="font-size:13px;color:#3B7A77;line-height:1.75;">مخططات تفاعلية وتقارير إحصائية عن التعليم العالي في دول الخليج.</div>
</div>
""", unsafe_allow_html=True)
        if st.button("انتقل إلى البيانات ←", key="card_data", use_container_width=True):
            st.session_state.page = "البيانات"; st.rerun()
    with c5:
        st.markdown("""
<div style="border:1.5px solid #DEF2F1;border-radius:16px;padding:28px 22px;background:#fff;text-align:right;direction:rtl;">
  <div style="font-size:28px;margin-bottom:14px;">🏛️</div>
  <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#17252A;margin-bottom:10px;">من نحن</div>
  <div style="font-size:13px;color:#3B7A77;line-height:1.75;">تعرّف على منصة بوصلة ورؤيتها ورسالتها وقيمها.</div>
</div>
""", unsafe_allow_html=True)
        if st.button("انتقل إلى من نحن ←", key="card_about", use_container_width=True):
            st.session_state.page = "من نحن"; st.rerun()

    divider()

    # Vision / Mission / Values
    section_tag("هويتنا")
    section_h("رؤيتنا ورسالتنا وقيمنا")
    st.markdown("""
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:32px;direction:rtl;">
  <div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.15);border-radius:14px;padding:22px 18px;">
    <div style="font-family:Syne,sans-serif;font-size:15px;font-weight:800;color:#17252A;margin-bottom:10px;text-align:right;">رؤيتنا</div>
    <div style="font-size:13px;color:#3B7A77;line-height:1.7;text-align:right;">إعادة تعريف تجربة اختيار التعليم في الخليج — منصة ذكية توجّه الشباب نحو مستقبلهم بثقة.</div>
  </div>
  <div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.15);border-radius:14px;padding:22px 18px;">
    <div style="font-family:Syne,sans-serif;font-size:15px;font-weight:800;color:#17252A;margin-bottom:10px;text-align:right;">رسالتنا</div>
    <div style="font-size:13px;color:#3B7A77;line-height:1.7;text-align:right;">تمكين الطلبة من اتخاذ قرارات تعليمية دقيقة باستخدام الذكاء الاصطناعي والبيانات الموثوقة.</div>
  </div>
  <div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.15);border-radius:14px;padding:22px 18px;">
    <div style="font-family:Syne,sans-serif;font-size:15px;font-weight:800;color:#17252A;margin-bottom:10px;text-align:right;">قيمنا</div>
    <div style="font-size:13px;color:#3B7A77;line-height:1.7;text-align:right;">الوضوح · العدالة · التمكين · الابتكار · الموثوقية</div>
  </div>
</div>
""", unsafe_allow_html=True)

    page_end()


# ══════════════════════════════════════════════
# بحث الجامعات
# ══════════════════════════════════════════════
elif P == "بحث الجامعات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    page_start()
    back_btn()
    section_tag("الاستكشاف")
    section_h("بحث الجامعات")

    q = st.text_input("", placeholder="ابحث عن جامعة، مدينة، أو دولة...").strip().lower()

    c1, c2, c3, c4, c5 = st.columns([1.2, 1, 1, 1.2, 1])
    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c1.selectbox("الدولة",   ["الكل"] + countries)
    types_    = sorted([x for x in unis["type"].unique() if str(x).strip()])
    uni_type  = c2.selectbox("النوع",    ["الكل"] + types_)
    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c3.selectbox("المرحلة", ["الكل"] + levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c4.selectbox("التخصص",  ["الكل"] + majors_)
    yn        = c5.selectbox("المنح",   ["الكل", "متاحة", "غير متاحة"])

    has_searched = bool(q) or country != "الكل" or uni_type != "الكل" or level != "الكل" or major != "الكل" or yn != "الكل"

    if not has_searched:
        st.markdown("""
<div style="text-align:center;padding:64px 0;color:#9AACAC;direction:rtl;">
  <div style="font-size:44px;margin-bottom:16px;">🔍</div>
  <div style="font-size:15px;font-weight:600;color:#2B7A77;margin-bottom:8px;">ابحث للبدء</div>
  <div style="font-size:13px;">اكتب اسم جامعة أو دولة، أو استخدم الفلاتر أعلاه</div>
</div>
""", unsafe_allow_html=True)
    else:
        f = unis.copy()
        if country  != "الكل": f = f[f["country"] == country]
        if uni_type != "الكل": f = f[f["type"] == uni_type]
        if yn == "متاحة":      f = f[f["scholarship"].apply(uni_has_sch)]
        if yn == "غير متاحة":  f = f[~f["scholarship"].apply(uni_has_sch)]
        if q:
            m = (f["name_en"].str.lower().str.contains(q, na=False) |
                 f["name_ar"].str.lower().str.contains(q, na=False) |
                 f["city"].str.lower().str.contains(q, na=False))
            f = f[m]
        if (major != "الكل" or level != "الكل") and not progs.empty:
            pm = progs.copy()
            if major != "الكل": pm = pm[pm["major_field"] == major]
            if level != "الكل": pm = pm[pm["level"] == level]
            f = f[f["uni_id"].isin(pm["uni_id"].unique())]

        st.markdown(f'<div style="display:inline-flex;align-items:center;gap:6px;background:rgba(46,196,182,.08);border:1.5px solid rgba(46,196,182,.25);border-radius:100px;padding:5px 14px;font-size:12px;font-weight:700;color:#2B7A77;margin-bottom:20px;">{len(f)} نتيجة</div>', unsafe_allow_html=True)

        if f.empty:
            st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
        else:
            for _, row in f.head(30).iterrows():
                is_pub   = str(row["type"]).strip().lower() in ["public", "حكومية"]
                type_tag = '<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:rgba(46,196,182,.1);color:#2B7A77;border:1px solid rgba(46,196,182,.25);">حكومية</span>' if is_pub else '<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:rgba(23,37,42,.06);color:#17252A;border:1px solid rgba(23,37,42,.1);">خاصة</span>'
                sch_tag  = '<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;">منحة دراسية</span>' if uni_has_sch(str(row["scholarship"])) else ""
                lang_tags = ""
                if not progs.empty:
                    for lg in progs[progs["uni_id"] == str(row["uni_id"])]["language"].dropna().unique()[:2]:
                        lang_tags += f'<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:#F0F9FF;color:#0369A1;border:1px solid #BAE6FD;">{lg}</span>'
                links = ""
                if str(row.get("website", "")).strip():        links += f'<a href="{row["website"]}" target="_blank" style="font-size:12px;font-weight:600;color:#2EC4B6;text-decoration:none;padding:5px 12px;border:1.5px solid rgba(46,196,182,.3);border-radius:7px;background:rgba(46,196,182,.05);white-space:nowrap;">الموقع الرسمي</a>'
                if str(row.get("admissions_url", "")).strip(): links += f'<a href="{row["admissions_url"]}" target="_blank" style="font-size:12px;font-weight:600;color:#2EC4B6;text-decoration:none;padding:5px 12px;border:1.5px solid rgba(46,196,182,.3);border-radius:7px;background:rgba(46,196,182,.05);white-space:nowrap;margin-right:6px;">القبول</a>'
                st.markdown(f"""
<div style="background:#fff;border:1.5px solid rgba(23,37,42,.1);border-radius:12px;padding:16px 20px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;gap:16px;direction:rtl;">
  <div>
    <div style="font-size:14px;font-weight:700;color:#17252A;margin-bottom:3px;">{row["name_ar"]} <span style="font-weight:400;color:#9AACAC;font-size:12px;">— {row["name_en"]}</span></div>
    <div style="font-size:12px;color:#9AACAC;margin-bottom:8px;">{row["city"]}, {row["country"]}</div>
    <div style="display:flex;flex-wrap:wrap;gap:5px;">{type_tag}{sch_tag}{lang_tags}</div>
  </div>
  <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">{links}</div>
</div>""", unsafe_allow_html=True)

    page_end()


# ══════════════════════════════════════════════
# المقارنة
# ══════════════════════════════════════════════
elif P == "المقارنة":
    unis = unis_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    page_start()
    back_btn()
    section_tag("التقييم المقارن")
    section_h("مقارنة الجامعات")

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + ", " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country", "city", "name_en"], na_position="last")

    selected = st.multiselect("اختر من ٢ إلى ٤ جامعات", options=unis["uni_id"].tolist(),
                              format_func=lambda x: label_map.get(str(x), str(x)), max_selections=4)
    if len(selected) < 2:
        st.info("يرجى اختيار جامعتين على الأقل.")
        page_end(); st.stop()

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_c = st.columns(len(selected))
    for i, uid in enumerate(selected):
        row = comp[comp["uni_id"] == uid].iloc[0]
        with cols_c[i]:
            sch  = str(row.get("scholarship", "")).strip() or "—"
            rank = (str(row.get("ranking_source", "")).strip() + " " + str(row.get("ranking_value", "")).strip()).strip() or "—"
            st.markdown(f"""
<div style="background:#fff;border:1.5px solid rgba(23,37,42,.1);border-radius:16px;padding:20px;direction:rtl;">
  <div style="font-family:Syne,sans-serif;font-size:15px;font-weight:800;color:#17252A;margin-bottom:14px;padding-bottom:12px;border-bottom:1.5px solid rgba(23,37,42,.1);">{row['name_ar']}</div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(23,37,42,.04);"><span style="font-size:12px;color:#9AACAC;">الموقع</span><span style="font-size:13px;font-weight:600;">{row['city']}, {row['country']}</span></div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(23,37,42,.04);"><span style="font-size:12px;color:#9AACAC;">النوع</span><span style="font-size:13px;font-weight:600;">{row['type']}</span></div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(23,37,42,.04);"><span style="font-size:12px;color:#9AACAC;">المنح</span><span style="font-size:13px;font-weight:600;">{sch}</span></div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;"><span style="font-size:12px;color:#9AACAC;">الترتيب</span><span style="font-size:13px;font-weight:600;">{rank}</span></div>
</div>""", unsafe_allow_html=True)
            st.write("")
            if str(row.get("website", "")).strip():        st.link_button("الموقع الرسمي",      row["website"],        use_container_width=True)
            if str(row.get("admissions_url", "")).strip(): st.link_button("القبول والتسجيل",    row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url", "")).strip():   st.link_button("البرامج الأكاديمية", row["programs_url"],   use_container_width=True)

    progs = progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        divider()
        section_tag("البرامج الأكاديمية")
        section_h_sm("البرامج المتاحة للجامعات المختارة")
        comp_progs = progs[progs["uni_id"].isin(selected)].copy()
        if comp_progs.empty:
            st.info("لا تتوفر بيانات برامج للجامعات المختارة.")
        else:
            show_cols = [c for c in ["uni_id","program_name_ar","program_name_en","level","major_field","language","duration_years"] if c in comp_progs.columns]
            rename_map = {"uni_id":"الجامعة","program_name_ar":"البرنامج","program_name_en":"Program","level":"المرحلة","major_field":"التخصص","language":"اللغة","duration_years":"المدة (سنوات)"}
            display_df = comp_progs[show_cols].rename(columns=rename_map)
            if "الجامعة" in display_df.columns:
                id_to_ar = dict(zip(unis["uni_id"], unis["name_ar"]))
                display_df["الجامعة"] = display_df["الجامعة"].map(id_to_ar).fillna(display_df["الجامعة"])
            st.dataframe(display_df, use_container_width=True, hide_index=True)

    divider()
    section_tag("الذكاء الاصطناعي")
    section_h_sm("المقارنة الذكية")
    profile_txt = st.text_input("", placeholder="ملفك الأكاديمي (اختياري) — مثال: طالب هندسة، IELTS 6.5", key="comp_profile", label_visibility="collapsed")
    if st.button("اطلب مقارنة ذكية", use_container_width=True, key="btn_compare_ai"):
        unis_data = [comp[comp["uni_id"] == uid].iloc[0].to_dict() for uid in selected if uid in comp["uni_id"].values]
        with st.spinner("جاري تحليل الجامعات..."):
            ai_result = compare_unis_ai(unis_data, profile_txt)
        st.markdown(f'<div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.2);border-radius:14px;padding:22px 26px;margin-top:14px;line-height:2;color:#17252A;direction:rtl;"><span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2EC4B6;margin-bottom:10px;display:block;">المقارنة الذكية</span>{ai_result}</div>', unsafe_allow_html=True)
    page_end()


# ══════════════════════════════════════════════
# رُشد
# ══════════════════════════════════════════════
elif P == "رُشد":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    page_start()
    back_btn()
    section_tag("المستشار الأكاديمي الذكي")
    section_h("رُشد")
    st.markdown('<p style="color:#9AACAC;font-size:14px;margin-bottom:28px;margin-top:-14px;text-align:right;">تحدّث بالعربية — رُشد يفهم ملفك ويرشّح الجامعات المناسبة</p>', unsafe_allow_html=True)

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    section_tag("التحليل الفوري")
    section_h_sm("التحليل السريع")
    qm_c1, qm_c2, qm_c3 = st.columns(3)
    countries_list = sorted([x for x in unis["country"].unique() if str(x).strip()])
    qm_country = qm_c1.selectbox("الدولة المفضلة", ["الكل"] + countries_list, key="qm_country")
    qm_major   = qm_c2.text_input("التخصص المطلوب", placeholder="مثال: هندسة الحاسب", key="qm_major")
    qm_ielts   = qm_c3.text_input("درجة IELTS",     placeholder="مثال: 6.5",          key="qm_ielts")

    if st.button("حلّل بسرعة", use_container_width=True, key="btn_quick_match"):
        if not qm_major.strip():
            st.warning("يرجى إدخال التخصص المطلوب.")
        else:
            profile_data = {"country": qm_country, "major": qm_major, "ielts": qm_ielts or "غير محدد"}
            with st.spinner("جاري التحليل..."):
                qm_result = quick_match(profile_data, st.session_state.unis_context)
            top3   = qm_result.get("top_3", [])
            advice = qm_result.get("advice", "")
            missing = qm_result.get("missing", [])
            if top3:
                qr_cols = st.columns(len(top3))
                for i, item in enumerate(top3[:3]):
                    uid = item.get("uni_id", ""); name_ar = item.get("name_ar", uid)
                    reason = item.get("reason", ""); fit = item.get("fit", "مناسب")
                    uni_row = unis[unis["uni_id"] == uid]
                    city_country = ""; sch_tag = ""
                    if not uni_row.empty:
                        r = uni_row.iloc[0]; city_country = f"{r.get('city','')}, {r.get('country','')}"
                        if uni_has_sch(str(r.get("scholarship", ""))): sch_tag = '<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;">منحة دراسية</span>'
                    with qr_cols[i]:
                        st.markdown(f"""<div style="background:#fff;border:1.5px solid rgba(23,37,42,.1);border-top:3px solid #2EC4B6;border-radius:12px;padding:18px;direction:rtl;">
<div style="font-size:14px;font-weight:700;color:#17252A;">{name_ar}</div>
<div style="font-size:12px;color:#9AACAC;margin:3px 0 8px;">{city_country}</div>
<div style="color:#9AACAC;font-size:13px;margin-bottom:10px;line-height:1.7;">{reason}</div>
<div style="display:flex;flex-wrap:wrap;gap:5px;">{sch_tag}<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:rgba(46,196,182,.1);color:#2B7A77;border:1px solid rgba(46,196,182,.25);">{fit}</span></div>
</div>""", unsafe_allow_html=True)
            if advice:
                st.markdown(f'<div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.2);border-radius:14px;padding:22px 26px;margin-top:14px;line-height:2;color:#17252A;direction:rtl;"><span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2EC4B6;display:block;margin-bottom:8px;">نصيحة رُشد</span>{advice}</div>', unsafe_allow_html=True)
            if missing:
                missing_html = "".join([f'<span style="padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;margin:3px;">{m}</span>' for m in missing])
                st.markdown(f'<div style="margin-top:10px;direction:rtl;"><span style="color:#9AACAC;font-size:13px;margin-left:8px;">قد تحتاج إلى:</span>{missing_html}</div>', unsafe_allow_html=True)

    divider()

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{"role":"assistant","content":"مرحباً، أنا رُشد.\n\nأخبرني عن نفسك:\n- التخصص الذي تريده\n- الدولة المفضلة\n- معدلك التقريبي\n- هل عندك IELTS وكم درجتك؟\n\nوسأرشّح لك الجامعات المناسبة."}]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"], avatar="🧭" if msg["role"] == "assistant" else "🎓"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":user_input})
        with st.chat_message("user", avatar="🎓"): st.markdown(user_input)
        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner(""):
                history = [m for m in st.session_state.rushd_messages if not (m["role"] == "assistant" and "مرحباً" in m["content"])]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role":"assistant","content":reply})

    if len(st.session_state.rushd_messages) > 1:
        if st.button("محادثة جديدة"): st.session_state.rushd_messages = []; st.rerun()
    page_end()


# ══════════════════════════════════════════════
# البيانات
# ══════════════════════════════════════════════
elif P == "البيانات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("لا تتوفر بيانات."); st.stop()

    page_start()
    back_btn()
    section_tag("الإحصاء والتحليل")
    section_h("لوحة البيانات")

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    # Stats row
    stats = [("إجمالي الجامعات", N_UNIS), ("إجمالي البرامج", N_PROGS), ("تقدم منحاً", with_sch), ("دولة خليجية", N_CTRY)]
    cols_s = st.columns(4)
    for col, (label, val) in zip(cols_s, stats):
        col.markdown(f"""<div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.2);border-radius:12px;padding:20px;text-align:center;">
<div style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:#2EC4B6;">{val}</div>
<div style="font-size:12px;color:#3B7A77;margin-top:4px;">{label}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

    T = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             font=dict(family="IBM Plex Sans Arabic", color="#9AACAC"),
             margin=dict(l=10, r=10, t=38, b=10), height=290)
    T_sm = {**T, "height": 260}

    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        fig = px.bar(x=list(by_country.values()), y=list(by_country.keys()), orientation="h",
                     title="الجامعات حسب الدولة", color_discrete_sequence=["#2EC4B6"])
        fig.update_layout(**T); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        fig = px.pie(values=list(by_type.values()), names=list(by_type.keys()),
                     title="حكومية / خاصة", hole=0.55,
                     color_discrete_sequence=["#2EC4B6","#17252A","#3AAFA9"])
        fig.update_layout(**T); fig.update_traces(textfont_color="white")
        st.plotly_chart(fig, use_container_width=True)
    with ch3:
        if top_fields:
            fig = px.bar(x=list(top_fields.keys()), y=list(top_fields.values()),
                         title="أبرز التخصصات", color_discrete_sequence=["#3AAFA9"])
            fig.update_layout(**T, xaxis_tickangle=-30); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    ch4, ch5 = st.columns(2)
    with ch4:
        pct = round(with_sch / max(len(unis), 1) * 100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=pct,
            title={"text":"% نسبة الجامعات التي تقدم منحاً","font":{"family":"IBM Plex Sans Arabic","color":"#9AACAC","size":13}},
            number={"font":{"color":"#2EC4B6","family":"IBM Plex Sans Arabic"}},
            gauge={"axis":{"range":[0,100],"tickcolor":"#DEF2F1"},"bar":{"color":"#2EC4B6"},
                   "bgcolor":"rgba(0,0,0,0)","bordercolor":"rgba(46,196,182,.1)",
                   "steps":[{"range":[0,100],"color":"rgba(46,196,182,.05)"}]}))
        fig.update_layout(**T_sm)
        st.plotly_chart(fig, use_container_width=True)
    with ch5:
        if by_lang:
            fig = px.bar(x=list(by_lang.keys()), y=list(by_lang.values()),
                         title="لغات الدراسة", color_discrete_sequence=["#17252A"])
            fig.update_layout(**T_sm); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    divider()
    section_tag("المنح الدراسية")
    section_h_sm("توزيع المنح حسب الدولة")
    if not unis.empty and "scholarship" in unis.columns:
        sch_data = []
        for _, row in unis.iterrows():
            ctry = str(row.get("country","")).strip(); sch = str(row.get("scholarship","")).strip()
            if not ctry or ctry == "nan": continue
            for cat in ["Local","GCC","International"]:
                sch_data.append({"الدولة":ctry,"نوع المنحة":cat,"عدد":1 if cat in sch else 0})
        sch_df = pd.DataFrame(sch_data).groupby(["الدولة","نوع المنحة"], as_index=False)["عدد"].sum()
        sch_df = sch_df[sch_df["عدد"] > 0]
        if not sch_df.empty:
            fig_sch = px.bar(sch_df, x="عدد", y="الدولة", color="نوع المنحة", orientation="h", barmode="stack",
                             title="عدد الجامعات التي تقدم منحاً لكل فئة حسب الدولة",
                             color_discrete_map={"Local":"#2EC4B6","GCC":"#17252A","International":"#3AAFA9"})
            fig_sch.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(family="IBM Plex Sans Arabic",color="#9AACAC"),
                                  margin=dict(l=10,r=10,t=38,b=10), height=320,
                                  legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#9AACAC")))
            fig_sch.update_traces(marker_line_width=0)
            st.plotly_chart(fig_sch, use_container_width=True)

    divider()
    col_r, col_g = st.columns(2)
    with col_r:
        section_h_sm("التقرير التحليلي الذكي")
        st.markdown('<p style="font-size:13px;color:#9AACAC;margin-bottom:14px;text-align:right;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير", use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                report = generate_dashboard_report({"total_unis":len(unis),"by_country":by_country,"by_type":by_type,"top_fields":top_fields,"by_language":by_lang,"with_scholarships":with_sch,"total_progs":len(progs)})
            st.markdown(f'<div style="background:#EEF8F8;border:1.5px solid rgba(46,196,182,.2);border-radius:14px;padding:22px 26px;margin-top:14px;line-height:2;color:#17252A;direction:rtl;"><span style="font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#2EC4B6;display:block;margin-bottom:8px;">التقرير التحليلي</span>{report}</div>', unsafe_allow_html=True)
    with col_g:
        section_h_sm("تحليل الفجوات التعليمية")
        st.markdown('<p style="font-size:13px;color:#9AACAC;margin-bottom:14px;text-align:right;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div style="background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:14px;padding:22px 26px;margin-top:14px;line-height:2;color:#17252A;direction:rtl;">{gaps}</div>', unsafe_allow_html=True)
    page_end()


# ══════════════════════════════════════════════
# من نحن
# ══════════════════════════════════════════════
elif P == "من نحن":
    page_start()
    back_btn()
    section_tag("هويتنا")
    section_h("من نحن")
    st.markdown("""
<div style="font-size:15px;color:#2B7A77;line-height:2;margin-bottom:32px;max-width:720px;direction:rtl;text-align:right;">
  <p style="color:#17252A;font-size:17px;font-weight:600;margin-bottom:14px;">منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.</p>
  <p>جاءت فكرة بوصلة استجابةً لتحدٍ واقعي — تشتّت المعلومات وصعوبة المقارنة بين الجامعات وتعدد المصادر غير الموثوقة.</p>
  <p style="margin-top:12px;">نجمع البيانات التعليمية الخليجية ونقدّمها بطريقة مبسّطة، مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على اتخاذ قراره بثقة.</p>
</div>
""", unsafe_allow_html=True)

    divider()
    section_tag("قيمنا")
    section_h_sm("ما يحركنا")
    st.markdown("""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;direction:rtl;margin-bottom:32px;">
  <div style="background:#EEF8F8;border-radius:12px;padding:18px 14px;text-align:center;border:1.5px solid rgba(46,196,182,.15);">
    <div style="font-family:Syne,sans-serif;font-size:14px;font-weight:800;color:#17252A;margin-bottom:5px;">الوضوح</div>
    <div style="font-size:12px;color:#3B7A77;">تبسيط القرار التعليمي</div>
  </div>
  <div style="background:#EEF8F8;border-radius:12px;padding:18px 14px;text-align:center;border:1.5px solid rgba(46,196,182,.15);">
    <div style="font-family:Syne,sans-serif;font-size:14px;font-weight:800;color:#17252A;margin-bottom:5px;">العدالة</div>
    <div style="font-size:12px;color:#3B7A77;">عرض الخيارات دون تحيّز</div>
  </div>
  <div style="background:#EEF8F8;border-radius:12px;padding:18px 14px;text-align:center;border:1.5px solid rgba(46,196,182,.15);">
    <div style="font-family:Syne,sans-serif;font-size:14px;font-weight:800;color:#17252A;margin-bottom:5px;">التمكين</div>
    <div style="font-size:12px;color:#3B7A77;">فهم الذات قبل التخصص</div>
  </div>
  <div style="background:#EEF8F8;border-radius:12px;padding:18px 14px;text-align:center;border:1.5px solid rgba(46,196,182,.15);">
    <div style="font-family:Syne,sans-serif;font-size:14px;font-weight:800;color:#17252A;margin-bottom:5px;">الابتكار</div>
    <div style="font-size:12px;color:#3B7A77;">AI في خدمة التعليم</div>
  </div>
</div>
""", unsafe_allow_html=True)

    divider()
    section_tag("تواصل")
    section_h_sm("تواصل معنا")
    ca, cb = st.columns(2)
    with ca:
        st.text_input("الاسم",             placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني", placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=120)
    if st.button("إرسال", use_container_width=True):
        st.success("تم الاستلام. شكراً لتواصلك.")
    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
    page_end()
