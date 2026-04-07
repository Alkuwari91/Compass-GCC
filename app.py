import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_engine import build_unis_context, chat_rushd, generate_dashboard_report, analyze_gaps, compare_unis_ai, quick_match

st.set_page_config(page_title="بوصلة", layout="wide", initial_sidebar_state="collapsed")

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');
:root{--teal:#2EC4B6;--dark:#17252A;--mid:#2B7A77;--light:#DEF2F1;--white:#FEFFFF;--ink:#17252A;--muted:#3B7A77;--pale:#EEF8F8;--border:rgba(23,37,42,.10);--r:12px;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{font-family:'IBM Plex Sans Arabic',sans-serif!important;background:#F4F6F7!important;color:var(--ink)!important;direction:rtl!important;}
[data-testid="stSidebar"],[data-testid="stSidebarNav"],button[kind="header"],[data-testid="collapsedControl"],[data-testid="stDecoration"],footer,#MainMenu{display:none!important;}
[data-testid="stAppViewContainer"]{background:#F4F6F7!important;}
[data-testid="stMain"]{background:transparent!important;display:flex;justify-content:center;}
[data-testid="stMainBlockContainer"]{
  padding:0!important;
  max-width:1160px!important;
  width:100%!important;
  margin:24px auto!important;
  background:#FEFFFF!important;
  border:1.5px solid #DEF2F1!important;
  border-radius:20px!important;
  box-shadow:0 4px 32px rgba(46,196,182,.07)!important;
  overflow:hidden!important;
}
[data-testid="block-container"]{padding:0!important;max-width:100%!important;}
input,textarea,[role="textbox"]{direction:rtl!important;text-align:right!important;}
div[data-baseweb="select"] *{direction:rtl!important;}
label{direction:rtl!important;text-align:right!important;color:var(--muted)!important;font-size:13px!important;font-weight:500!important;}

/* ── Nav ── */
.baw-nav{background:var(--dark);display:flex;align-items:center;justify-content:space-between;padding:0 32px;height:58px;border-radius:18px 18px 0 0;}
.baw-logo{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#fff;letter-spacing:-0.5px;white-space:nowrap;}
.baw-logo span{color:var(--teal);}
.baw-links{display:flex;gap:4px;}
.baw-link{font-size:13px;font-weight:600;color:#6B7280;padding:6px 13px;border-radius:8px;border:none;background:none;cursor:pointer;transition:all .15s;white-space:nowrap;font-family:'IBM Plex Sans Arabic',sans-serif;}
.baw-link:hover{background:rgba(255,255,255,.08);color:#fff;}
.baw-link.on{background:var(--teal);color:var(--dark);font-weight:700;}

/* ── Page inner padding ── */
.page-body{padding:40px 48px 56px;direction:rtl;}

/* ── Hero ── */
.hero-tag{display:inline-flex;align-items:center;gap:7px;background:rgba(46,196,182,.1);border:1px solid rgba(46,196,182,.25);border-radius:100px;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#2B7A77;}
.hero-tag-dot{width:5px;height:5px;border-radius:50%;background:#2EC4B6;display:inline-block;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.hero-big{font-family:'Syne',sans-serif;font-size:80px;font-weight:800;color:#17252A;line-height:0.95;letter-spacing:-4px;margin:24px 0 0;text-align:center;}
.hero-big em{color:#2EC4B6;font-style:normal;}
.hero-rule{width:56px;height:3px;background:#2EC4B6;border-radius:2px;margin:24px auto;}
.hero-sub{font-size:16px;color:#3B7A77;line-height:1.8;max-width:540px;margin:0 auto 32px;text-align:center;}
.hero-stats{display:flex;justify-content:center;align-items:center;gap:0;border:1px solid #DEF2F1;border-radius:16px;overflow:hidden;max-width:480px;margin:0 auto 48px;}
.hero-stat-item{flex:1;padding:16px;text-align:center;border-left:1px solid #DEF2F1;}
.hero-stat-item:last-child{border-left:none;}
.hero-stat-n{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#17252A;line-height:1;}
.hero-stat-l{font-size:11px;color:#9AACAC;font-weight:500;margin-top:3px;}

/* ── Feature cards ── */
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:0;}
.feat-card{border:1.5px solid var(--border);border-radius:16px;padding:28px 22px;background:var(--white);position:relative;overflow:hidden;display:flex;flex-direction:column;min-height:220px;cursor:pointer;transition:all .2s;}
.feat-card::before{content:'';position:absolute;top:0;right:0;width:56px;height:56px;background:var(--teal);opacity:.06;border-radius:0 16px 0 56px;transition:all .3s;}
.feat-card:hover{border-color:var(--teal);transform:translateY(-2px);box-shadow:0 10px 28px rgba(46,196,182,.1);}
.feat-card:hover::before{opacity:.12;width:72px;height:72px;}
.feat-num{font-size:11px;font-weight:800;letter-spacing:2px;color:var(--teal);margin-bottom:16px;}
.feat-title{font-family:'Syne',sans-serif;font-size:17px;font-weight:800;color:var(--ink);margin-bottom:8px;}
.feat-body{font-size:13px;color:var(--muted);line-height:1.75;flex:1;}
.feat-arrow{margin-top:16px;font-size:12px;font-weight:700;color:var(--teal);}

/* ── Values compact ── */
.vision-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:32px;}
.vision-card{background:var(--pale);border:1.5px solid rgba(46,196,182,.15);border-radius:14px;padding:20px 18px;}
.vision-title{font-family:'Syne',sans-serif;font-size:14px;font-weight:800;color:var(--dark);margin-bottom:8px;}
.vision-body{font-size:13px;color:var(--muted);line-height:1.7;}
.values-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.val-card{background:var(--pale);border-radius:var(--r);padding:18px 14px;text-align:center;border:1.5px solid rgba(46,196,182,.15);}
.val-title{font-family:'Syne',sans-serif;font-size:14px;font-weight:800;color:var(--dark);margin-bottom:5px;}
.val-body{font-size:12px;color:var(--muted);}

/* ── Uni cards ── */
.uni-card{background:var(--white);border:1.5px solid var(--border);border-radius:var(--r);padding:18px 22px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;gap:20px;transition:all .18s;}
.uni-card:hover{border-color:var(--teal);box-shadow:0 4px 16px rgba(46,196,182,.08);}
.uni-name{font-size:14px;font-weight:700;color:var(--ink);margin-bottom:3px;}
.uni-sub{font-size:12px;color:#9AACAC;}
.uni-right{display:flex;align-items:center;gap:8px;flex-shrink:0;}
.uni-link{font-size:12px;font-weight:600;color:var(--teal);text-decoration:none;padding:5px 12px;border:1.5px solid rgba(46,196,182,.3);border-radius:7px;background:rgba(46,196,182,.05);transition:all .15s;white-space:nowrap;}
.uni-link:hover{background:var(--teal);color:var(--dark);border-color:var(--teal);}

/* ── Tags ── */
.tags{display:flex;flex-wrap:wrap;gap:5px;}
.tag{padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;}
.tag-gov{background:rgba(46,196,182,.1);color:var(--mid);border:1px solid rgba(46,196,182,.25);}
.tag-priv{background:rgba(23,37,42,.06);color:var(--ink);border:1px solid var(--border);}
.tag-sch{background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;}
.tag-lang{background:#F0F9FF;color:#0369A1;border:1px solid #BAE6FD;}

.chip{display:inline-flex;align-items:center;gap:6px;background:rgba(46,196,182,.08);border:1.5px solid rgba(46,196,182,.25);border-radius:100px;padding:5px 14px;font-size:12px;font-weight:700;color:var(--mid);margin-bottom:20px;}

/* ── Compare ── */
.comp-card{background:var(--white);border:1.5px solid var(--border);border-radius:16px;padding:22px;}
.comp-head{font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:var(--ink);margin-bottom:16px;padding-bottom:12px;border-bottom:1.5px solid var(--border);}
.comp-row{display:flex;justify-content:space-between;align-items:center;padding:9px 0;border-bottom:1px solid rgba(23,37,42,.04);}
.comp-label{font-size:12px;color:#9AACAC;font-weight:500;}
.comp-val{font-size:13px;color:var(--ink);font-weight:600;}

/* ── AI boxes ── */
.ai-box{background:var(--pale);border:1.5px solid rgba(46,196,182,.2);border-radius:14px;padding:24px 28px;margin-top:16px;line-height:2;color:var(--ink);}
.ai-label{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin-bottom:12px;display:block;}
.gap-box{background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:14px;padding:24px 28px;margin-top:16px;line-height:2;color:var(--ink);}

/* ── Section headings ── */
.section-tag{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin-bottom:8px;}
.section-h{font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:var(--ink);letter-spacing:-0.5px;margin-bottom:24px;text-align:right;}
.section-h-sm{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:var(--ink);letter-spacing:-0.3px;margin-bottom:14px;}
.divider{height:1px;background:var(--border);margin:40px 0;border:none;}

/* ── Back button ── */
.stButton>button[data-testid="back_btn"]{background:var(--pale)!important;border-color:rgba(46,196,182,.3)!important;color:var(--mid)!important;}

/* ── Streamlit input overrides ── */
.stTextInput>div>div{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;}
.stTextInput>div>div:focus-within{border-color:var(--teal)!important;box-shadow:0 0 0 3px rgba(46,196,182,.12)!important;}
.stTextInput>div>div>input{color:var(--ink)!important;background:transparent!important;font-family:'IBM Plex Sans Arabic',sans-serif!important;}
input::placeholder{color:#9AACAC!important;opacity:1!important;}
textarea::placeholder{color:#9AACAC!important;opacity:1!important;}
.stTextArea>div>div{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;}
.stTextArea>div>div>textarea{color:var(--ink)!important;background:transparent!important;}
div[data-baseweb="select"]>div{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:10px!important;color:var(--ink)!important;}
div[data-baseweb="select"] *{color:var(--ink)!important;}
div[data-baseweb="popover"] li{background:var(--white)!important;color:var(--ink)!important;}
div[data-baseweb="popover"] li:hover{background:var(--pale)!important;color:var(--teal)!important;}
.stButton>button{background:var(--white)!important;border:1.5px solid var(--border)!important;color:var(--ink)!important;border-radius:10px!important;font-weight:600!important;font-family:'IBM Plex Sans Arabic',sans-serif!important;font-size:13px!important;padding:10px 18px!important;transition:all .18s!important;}
.stButton>button:hover{background:var(--pale)!important;border-color:var(--teal)!important;color:var(--teal)!important;}
.stLinkButton a{background:rgba(46,196,182,.07)!important;border:1.5px solid rgba(46,196,182,.25)!important;color:var(--mid)!important;border-radius:9px!important;font-weight:600!important;font-size:12px!important;}
.stLinkButton a:hover{background:var(--teal)!important;color:var(--dark)!important;border-color:var(--teal)!important;}
div[data-testid="stExpander"]{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:var(--r)!important;overflow:hidden!important;margin-bottom:8px!important;}
[data-testid="stChatMessage"]{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:var(--r)!important;direction:rtl!important;margin-bottom:8px!important;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(46,196,182,.3);border-radius:4px;}
</style>"""

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

st.markdown(CSS, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "الرئيسية"
PAGES = ["الرئيسية","بحث الجامعات","المقارنة","رُشد","البيانات","من نحن"]

# ── Nav ──
nav_links_html = ""
for p in PAGES:
    active_cls = "on" if st.session_state.page == p else ""
    nav_links_html += f'<button class="baw-link {active_cls}" onclick="">{p}</button>'

st.markdown(f"""
<div class="baw-nav">
  <div class="baw-logo">بو<span>صلة</span></div>
  <div class="baw-links" id="nav-links">{nav_links_html}</div>
</div>
""", unsafe_allow_html=True)

# Invisible Streamlit nav buttons
nav_cols = st.columns(len(PAGES))
for i, name in enumerate(PAGES):
    with nav_cols[i]:
        if st.button(name, key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name; st.rerun()

# Style the nav buttons to be invisible (nav HTML above is decorative)
active_idx = PAGES.index(st.session_state.page)
st.markdown(f"""<style>
/* Hide all nav streamlit buttons visually — nav is handled by HTML above */
div[data-testid="stHorizontalBlock"]:nth-of-type(1) button{{
  opacity:0!important;height:2px!important;padding:0!important;min-height:0!important;border:none!important;background:none!important;margin:0!important;
}}
div[data-testid="stHorizontalBlock"]:nth-of-type(1){{
  height:2px!important;overflow:hidden!important;margin:0!important;padding:0!important;gap:0!important;
}}
</style>""", unsafe_allow_html=True)


def back_home():
    if st.button("← الرئيسية", key="back_home_btn"):
        st.session_state.page = "الرئيسية"; st.rerun()


# ══════════════════════════════════════════════
# الرئيسية
# ══════════════════════════════════════════════
if st.session_state.page == "الرئيسية":
    st.markdown('<div class="page-body">', unsafe_allow_html=True)

    # Hero
    st.markdown(f"""
<div style="text-align:center;padding:48px 0 0;direction:rtl;">
  <div style="display:flex;justify-content:center;margin-bottom:0;">
    <div class="hero-tag"><span class="hero-tag-dot"></span>الدليل الذكي للتعليم الخليجي</div>
  </div>
  <div class="hero-big">بو<em>صلة</em></div>
  <div class="hero-rule"></div>
  <div class="hero-sub">اكتشف الجامعات، قارن التخصصات، واتخذ قرارك التعليمي بثقة<br>مع مستشار ذكي يتحدث العربية</div>
  <div class="hero-stats">
    <div class="hero-stat-item"><div class="hero-stat-n">{N_UNIS}+</div><div class="hero-stat-l">جامعة</div></div>
    <div class="hero-stat-item"><div class="hero-stat-n">{N_CTRY}</div><div class="hero-stat-l">دولة خليجية</div></div>
    <div class="hero-stat-item"><div class="hero-stat-n">{N_PROGS}+</div><div class="hero-stat-l">برنامج</div></div>
    <div class="hero-stat-item"><div class="hero-stat-n">{N_SCH}</div><div class="hero-stat-l">منحة متاحة</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Divider label
    st.markdown("""
<div style="height:52px;display:flex;align-items:center;justify-content:center;">
  <div style="display:flex;align-items:center;gap:12px;color:#9AACAC;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;">
    <div style="width:40px;height:1px;background:#DEF2F1;"></div>
    ماذا يقدم بوصلة
    <div style="width:40px;height:1px;background:#DEF2F1;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-h" style="text-align:center;margin-bottom:28px;">منصة واحدة — كل خياراتك الأكاديمية</div>', unsafe_allow_html=True)

    # Feature cards with Streamlit buttons underneath
    st.markdown("""<div class="feat-grid">
  <div class="feat-card" id="card-rushd">
    <div class="feat-num">01 — المستشار الذكي</div>
    <div class="feat-title">رُشد</div>
    <div class="feat-body">تحدّث بالعربية — رُشد يفهم ملفك ويرشّح أفضل الجامعات مع شرح كل توصية.</div>
    <div class="feat-arrow">انتقل ←</div>
  </div>
  <div class="feat-card" id="card-data">
    <div class="feat-num">02 — الإحصاء والتحليل</div>
    <div class="feat-title">لوحة البيانات</div>
    <div class="feat-body">مخططات تفاعلية وتقارير ذكية تحوّل بيانات التعليم الخليجي إلى رؤى واضحة.</div>
    <div class="feat-arrow">انتقل ←</div>
  </div>
  <div class="feat-card" id="card-compare">
    <div class="feat-num">03 — القرار المدروس</div>
    <div class="feat-title">المقارنة</div>
    <div class="feat-body">قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — المنح، الترتيب، والروابط الرسمية.</div>
    <div class="feat-arrow">انتقل ←</div>
  </div>
</div>""", unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    if fc1.button("انتقل إلى رُشد",       use_container_width=True, key="hero_rushd"):   st.session_state.page="رُشد";       st.rerun()
    if fc2.button("انتقل إلى البيانات",   use_container_width=True, key="hero_data"):    st.session_state.page="البيانات";   st.rerun()
    if fc3.button("انتقل إلى المقارنة",   use_container_width=True, key="hero_compare"): st.session_state.page="المقارنة";   st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Vision / Mission / Values — compact cards
    st.markdown('<div class="section-tag">هويتنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">رؤيتنا ورسالتنا وقيمنا</div>', unsafe_allow_html=True)
    st.markdown("""<div class="vision-grid">
  <div class="vision-card">
    <div class="vision-title">رؤيتنا</div>
    <div class="vision-body">إعادة تعريف تجربة اختيار التعليم في الخليج — منصة ذكية توجّه الشباب نحو تخصصاتهم بثقة.</div>
  </div>
  <div class="vision-card">
    <div class="vision-title">رسالتنا</div>
    <div class="vision-body">تمكين الطلبة من اتخاذ قرارات تعليمية دقيقة باستخدام الذكاء الاصطناعي والبيانات الموثوقة.</div>
  </div>
  <div class="vision-card">
    <div class="vision-title">قيمنا</div>
    <div class="vision-body">الوضوح · العدالة · التمكين · الابتكار · الموثوقية — خمس ركائز تحرّك كل ما نبنيه.</div>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    if b1.button("المستشار رُشد",  use_container_width=True): st.session_state.page="رُشد";         st.rerun()
    if b2.button("تحليل البيانات", use_container_width=True): st.session_state.page="البيانات";     st.rerun()
    if b3.button("بحث الجامعات",  use_container_width=True): st.session_state.page="بحث الجامعات"; st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# بحث الجامعات
# ══════════════════════════════════════════════
elif st.session_state.page == "بحث الجامعات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    back_home()
    st.markdown('<div class="section-tag">الاستكشاف</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">بحث الجامعات</div>', unsafe_allow_html=True)

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

    # Check if user has searched / filtered
    has_searched = bool(q) or country != "الكل" or uni_type != "الكل" or level != "الكل" or major != "الكل" or yn != "الكل"

    if not has_searched:
        st.markdown("""
<div style="text-align:center;padding:56px 0;color:#9AACAC;">
  <div style="font-size:48px;margin-bottom:16px;">🔍</div>
  <div style="font-size:15px;font-weight:600;color:#3B7A77;margin-bottom:8px;">ابحث للبدء</div>
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

        st.markdown(f'<div class="chip">{len(f)} نتيجة</div>', unsafe_allow_html=True)
        if f.empty:
            st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
        else:
            for _, row in f.head(30).iterrows():
                is_pub   = str(row["type"]).strip().lower() in ["public", "حكومية"]
                type_tag = '<span class="tag tag-gov">حكومية</span>' if is_pub else '<span class="tag tag-priv">خاصة</span>'
                sch_tag  = '<span class="tag tag-sch">منحة دراسية</span>' if uni_has_sch(str(row["scholarship"])) else ""
                lang_tags = ""
                if not progs.empty:
                    for lg in progs[progs["uni_id"] == str(row["uni_id"])]["language"].dropna().unique()[:2]:
                        lang_tags += f'<span class="tag tag-lang">{lg}</span>'
                links = ""
                if str(row.get("website", "")).strip():        links += f'<a href="{row["website"]}" target="_blank" class="uni-link">الموقع الرسمي</a>'
                if str(row.get("admissions_url", "")).strip(): links += f'<a href="{row["admissions_url"]}" target="_blank" class="uni-link">القبول</a>'
                st.markdown(f"""<div class="uni-card">
  <div><div class="uni-name">{row["name_ar"]} <span style="font-weight:400;color:#9AACAC;font-size:12px;">— {row["name_en"]}</span></div><div class="uni-sub">{row["city"]}, {row["country"]}</div><div class="tags" style="margin-top:8px;">{type_tag}{sch_tag}{lang_tags}</div></div>
  <div class="uni-right">{links}</div>
</div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# المقارنة
# ══════════════════════════════════════════════
elif st.session_state.page == "المقارنة":
    unis = unis_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    back_home()
    st.markdown('<div class="section-tag">التقييم المقارن</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">مقارنة الجامعات</div>', unsafe_allow_html=True)

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + ", " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country", "city", "name_en"], na_position="last")

    selected = st.multiselect("اختر من ٢ إلى ٤ جامعات", options=unis["uni_id"].tolist(),
                              format_func=lambda x: label_map.get(str(x), str(x)), max_selections=4)
    if len(selected) < 2:
        st.info("يرجى اختيار جامعتين على الأقل.")
        st.markdown('</div>', unsafe_allow_html=True); st.stop()

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_c = st.columns(len(selected))
    for i, uid in enumerate(selected):
        row = comp[comp["uni_id"] == uid].iloc[0]
        with cols_c[i]:
            sch  = (str(row.get("scholarship", "")).strip() or "—")
            rank = (str(row.get("ranking_source", "")).strip() + " " + str(row.get("ranking_value", "")).strip()).strip() or "—"
            st.markdown(f"""<div class="comp-card">
  <div class="comp-head">{row['name_ar']}</div>
  <div class="comp-row"><span class="comp-label">الموقع</span><span class="comp-val">{row['city']}, {row['country']}</span></div>
  <div class="comp-row"><span class="comp-label">النوع</span><span class="comp-val">{row['type']}</span></div>
  <div class="comp-row"><span class="comp-label">المنح</span><span class="comp-val">{sch}</span></div>
  <div class="comp-row"><span class="comp-label">الترتيب</span><span class="comp-val">{rank}</span></div>
</div>""", unsafe_allow_html=True)
            st.write("")
            if str(row.get("website", "")).strip():        st.link_button("الموقع الرسمي",      row["website"],        use_container_width=True)
            if str(row.get("admissions_url", "")).strip(): st.link_button("القبول والتسجيل",    row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url", "")).strip():   st.link_button("البرامج الأكاديمية", row["programs_url"],   use_container_width=True)

    progs = progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-tag">البرامج الأكاديمية</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-h-sm">البرامج المتاحة للجامعات المختارة</div>', unsafe_allow_html=True)
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

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">الذكاء الاصطناعي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm">المقارنة الذكية</div>', unsafe_allow_html=True)
    profile_txt = st.text_input("", placeholder="ملفك الأكاديمي (اختياري) — مثال: طالب هندسة، IELTS 6.5", key="comp_profile", label_visibility="collapsed")
    if st.button("اطلب مقارنة ذكية", use_container_width=True, key="btn_compare_ai"):
        unis_data = [comp[comp["uni_id"] == uid].iloc[0].to_dict() for uid in selected if uid in comp["uni_id"].values]
        with st.spinner("جاري تحليل الجامعات..."):
            ai_result = compare_unis_ai(unis_data, profile_txt)
        st.markdown(f'<div class="ai-box"><span class="ai-label">المقارنة الذكية</span>{ai_result}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# رُشد
# ══════════════════════════════════════════════
elif st.session_state.page == "رُشد":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    back_home()
    st.markdown('<div class="section-tag">المستشار الأكاديمي الذكي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">رُشد</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9AACAC;font-size:14px;margin-bottom:28px;margin-top:-14px;">تحدّث بالعربية — رُشد يفهم ملفك ويرشّح الجامعات المناسبة</p>', unsafe_allow_html=True)

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    st.markdown('<div class="section-tag">التحليل الفوري</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm">التحليل السريع</div>', unsafe_allow_html=True)
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
                        if uni_has_sch(str(r.get("scholarship", ""))): sch_tag = '<span class="tag tag-sch">منحة دراسية</span>'
                    with qr_cols[i]:
                        st.markdown(f"""<div class="uni-card" style="flex-direction:column;align-items:flex-start;border-top:3px solid var(--teal);">
  <div class="uni-name">{name_ar}</div><div class="uni-sub">{city_country}</div>
  <div style="color:#9AACAC;font-size:13px;margin:8px 0;line-height:1.7;">{reason}</div>
  <div class="tags">{sch_tag}<span class="tag tag-gov">{fit}</span></div>
</div>""", unsafe_allow_html=True)
            if advice:
                st.markdown(f'<div class="ai-box" style="margin-top:16px;"><span class="ai-label">نصيحة رُشد</span>{advice}</div>', unsafe_allow_html=True)
            if missing:
                missing_html = "".join([f'<span class="tag tag-sch" style="margin:3px;">{m}</span>' for m in missing])
                st.markdown(f'<div style="margin-top:10px;"><span style="color:#9AACAC;font-size:13px;margin-left:8px;">قد تحتاج إلى:</span>{missing_html}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

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
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# البيانات
# ══════════════════════════════════════════════
elif st.session_state.page == "البيانات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("لا تتوفر بيانات."); st.stop()

    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    back_home()
    st.markdown('<div class="section-tag">الإحصاء والتحليل</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">لوحة البيانات</div>', unsafe_allow_html=True)

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    st.markdown(f"""<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:36px;justify-content:center;">
  <div style="background:var(--pale);border:1.5px solid rgba(46,196,182,.2);border-radius:var(--r);padding:20px 24px;min-width:130px;text-align:center;">
    <div style="font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:var(--teal);">{N_UNIS}</div>
    <div style="font-size:12px;color:var(--muted);margin-top:4px;">إجمالي الجامعات</div>
  </div>
  <div style="background:var(--pale);border:1.5px solid rgba(46,196,182,.2);border-radius:var(--r);padding:20px 24px;min-width:130px;text-align:center;">
    <div style="font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:var(--teal);">{N_PROGS}</div>
    <div style="font-size:12px;color:var(--muted);margin-top:4px;">إجمالي البرامج</div>
  </div>
  <div style="background:var(--pale);border:1.5px solid rgba(46,196,182,.2);border-radius:var(--r);padding:20px 24px;min-width:130px;text-align:center;">
    <div style="font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:var(--teal);">{with_sch}</div>
    <div style="font-size:12px;color:var(--muted);margin-top:4px;">تقدم منحاً</div>
  </div>
  <div style="background:var(--pale);border:1.5px solid rgba(46,196,182,.2);border-radius:var(--r);padding:20px 24px;min-width:130px;text-align:center;">
    <div style="font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:var(--teal);">{N_CTRY}</div>
    <div style="font-size:12px;color:var(--muted);margin-top:4px;">دولة خليجية</div>
  </div>
</div>""", unsafe_allow_html=True)

    # Chart theme — no height in T to avoid duplicate kwarg
    T = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
             font=dict(family="IBM Plex Sans Arabic", color="#9AACAC"),
             margin=dict(l=10, r=10, t=38, b=10), height=290)

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

    T_sm = {**T, "height": 260}  # separate dict to avoid duplicate height kwarg
    ch4, ch5 = st.columns(2)
    with ch4:
        pct = round(with_sch / max(len(unis), 1) * 100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=pct,
            title={"text":"نسبة الجامعات التي تقدم منحاً %","font":{"family":"IBM Plex Sans Arabic","color":"#9AACAC","size":13}},
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

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">المنح الدراسية</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm">توزيع المنح حسب الدولة</div>', unsafe_allow_html=True)

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

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    col_r, col_g = st.columns(2)
    with col_r:
        st.markdown('<div class="section-h-sm">التقرير التحليلي الذكي</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#9AACAC;margin-bottom:14px;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير", use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                report = generate_dashboard_report({"total_unis":len(unis),"by_country":by_country,"by_type":by_type,"top_fields":top_fields,"by_language":by_lang,"with_scholarships":with_sch,"total_progs":len(progs)})
            st.markdown(f'<div class="ai-box"><span class="ai-label">التقرير التحليلي</span>{report}</div>', unsafe_allow_html=True)
    with col_g:
        st.markdown('<div class="section-h-sm">تحليل الفجوات التعليمية</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#9AACAC;margin-bottom:14px;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div class="gap-box">{gaps}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# من نحن
# ══════════════════════════════════════════════
elif st.session_state.page == "من نحن":
    st.markdown('<div class="page-body">', unsafe_allow_html=True)
    back_home()
    st.markdown('<div class="section-tag">هويتنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">من نحن</div>', unsafe_allow_html=True)
    st.markdown("""<div style="font-size:15px;color:#2B7A77;line-height:2;margin-bottom:36px;max-width:760px;">
<p style="color:#17252A;font-size:17px;font-weight:600;margin-bottom:14px;">منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.</p>
<p>جاءت فكرة بوصلة استجابةً لتحدٍ واقعي — تشتّت المعلومات وصعوبة المقارنة بين الجامعات وتعدد المصادر غير الموثوقة.</p>
<p style="margin-top:12px;">نجمع البيانات التعليمية الخليجية ونقدّمها بطريقة مبسّطة، مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على اتخاذ قراره بثقة.</p>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">قيمنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm" style="margin-bottom:18px;">ما يحركنا</div>', unsafe_allow_html=True)
    st.markdown("""<div class="values-grid">
  <div class="val-card"><div class="val-title">الوضوح</div><div class="val-body">تبسيط القرار التعليمي</div></div>
  <div class="val-card"><div class="val-title">العدالة</div><div class="val-body">عرض الخيارات دون تحيّز</div></div>
  <div class="val-card"><div class="val-title">التمكين</div><div class="val-body">فهم الذات قبل التخصص</div></div>
  <div class="val-card"><div class="val-title">الابتكار</div><div class="val-body">AI في خدمة التعليم</div></div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">تواصل</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm" style="margin-bottom:18px;">تواصل معنا</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.text_input("الاسم",             placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني", placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=120)
    if st.button("إرسال", use_container_width=True):
        st.success("تم الاستلام. شكراً لتواصلك.")
    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
    st.markdown('</div>', unsafe_allow_html=True)
