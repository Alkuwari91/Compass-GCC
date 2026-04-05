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
html,body,[class*="css"]{font-family:'IBM Plex Sans Arabic',sans-serif!important;background:var(--white)!important;color:var(--ink)!important;direction:rtl!important;}
[data-testid="stSidebar"],[data-testid="stSidebarNav"],button[kind="header"],[data-testid="collapsedControl"],[data-testid="stDecoration"],footer,#MainMenu{display:none!important;}
[data-testid="stAppViewContainer"]{background:var(--white)!important;}
[data-testid="stMain"]{background:transparent!important;}
[data-testid="stMainBlockContainer"]{padding:0!important;max-width:100%!important;}
input,textarea,[role="textbox"]{direction:rtl!important;text-align:right!important;}
div[data-baseweb="select"] *{direction:rtl!important;}
label{direction:rtl!important;text-align:right!important;color:var(--muted)!important;font-size:13px!important;font-weight:500!important;}

.nav{background:var(--dark);display:flex;align-items:center;justify-content:space-between;padding:0 48px;height:60px;position:sticky;top:0;z-index:100;}
.nav-logo{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:var(--white);letter-spacing:-0.5px;}
.nav-logo span{color:var(--teal);}
.nav-links{display:flex;gap:4px;}
.nav-btn{font-size:13px;font-weight:600;color:#6B7280;padding:6px 14px;border-radius:8px;border:none;background:none;cursor:pointer;transition:all .15s;white-space:nowrap;font-family:'IBM Plex Sans Arabic',sans-serif;}
.nav-btn:hover{background:rgba(255,255,255,.07);color:var(--white);}
.nav-btn.on{background:var(--teal);color:var(--dark);font-weight:700;}

.hero{background:var(--dark);padding:80px 48px 72px;display:grid;grid-template-columns:.9fr 1.1fr;gap:60px;align-items:center;direction:ltr;}
.hero-left{direction:rtl;}
.hero-pill{display:inline-flex;align-items:center;gap:7px;border:1.5px solid rgba(46,196,182,.35);border-radius:100px;padding:5px 14px;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--teal);margin-bottom:28px;}
.hero-pill-dot{width:6px;height:6px;border-radius:50%;background:var(--teal);animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.hero-h1{font-family:'Syne',sans-serif;font-size:64px;font-weight:800;color:var(--white);line-height:1.0;letter-spacing:-2px;margin-bottom:20px;}
.hero-h1 em{color:var(--teal);font-style:normal;}
.hero-sub{font-size:16px;color:rgba(255,255,255,.5);line-height:1.8;max-width:420px;}
.hero-right{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.hero-stat{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:var(--r);padding:24px 20px;text-align:center;transition:all .2s;}
.hero-stat:hover{background:rgba(46,196,182,.08);border-color:rgba(46,196,182,.3);}
.hero-stat-n{font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:var(--teal);line-height:1;margin-bottom:6px;}
.hero-stat-l{font-size:12px;color:rgba(255,255,255,.4);font-weight:500;}

.hero-wrap{background:#17252A!important;width:100%;margin:0;padding:0;}
.hero-wrap [data-testid="stHorizontalBlock"]{background:#17252A!important;padding:72px 48px 64px!important;gap:48px!important;}
.hero-wrap [data-testid="column"]{background:#17252A!important;}
.wrap{max-width:1160px;margin:0 auto;padding:60px 40px;}
.wrap-sm{max-width:860px;margin:0 auto;padding:60px 40px;}
.section-tag{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin-bottom:10px;}
.section-h{font-family:'Syne',sans-serif;font-size:28px;font-weight:800;color:var(--ink);letter-spacing:-0.5px;margin-bottom:28px;}
.section-h-sm{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:var(--ink);letter-spacing:-0.3px;margin-bottom:18px;}
.divider{height:1px;background:var(--border);margin:48px 0;border:none;}

.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:56px;}
.feat-card{border:1.5px solid var(--border);border-radius:16px;padding:32px 26px;transition:all .2s;cursor:pointer;background:var(--white);position:relative;overflow:hidden;}
.feat-card::before{content:'';position:absolute;top:0;right:0;width:60px;height:60px;background:var(--teal);opacity:.06;border-radius:0 16px 0 60px;transition:all .3s;}
.feat-card:hover{border-color:var(--teal);transform:translateY(-3px);box-shadow:0 12px 32px rgba(46,196,182,.1);}
.feat-card:hover::before{opacity:.12;width:80px;height:80px;}
.feat-num{font-family:'Syne',sans-serif;font-size:11px;font-weight:800;letter-spacing:2px;color:var(--teal);margin-bottom:20px;}
.feat-title{font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:var(--ink);margin-bottom:10px;}
.feat-body{font-size:13px;color:var(--muted);line-height:1.8;}

.uni-card{background:var(--white);border:1.5px solid var(--border);border-radius:var(--r);padding:20px 24px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;gap:20px;transition:all .18s;}
.uni-card:hover{border-color:var(--teal);box-shadow:0 4px 16px rgba(46,196,182,.08);}
.uni-name{font-size:14px;font-weight:700;color:var(--ink);margin-bottom:3px;}
.uni-sub{font-size:12px;color:#9AACAC;}
.uni-right{display:flex;align-items:center;gap:8px;flex-shrink:0;}
.uni-link{font-size:12px;font-weight:600;color:var(--teal);text-decoration:none;padding:5px 12px;border:1.5px solid rgba(46,196,182,.3);border-radius:7px;background:rgba(46,196,182,.05);transition:all .15s;white-space:nowrap;}
.uni-link:hover{background:var(--teal);color:var(--dark);border-color:var(--teal);}

.tags{display:flex;flex-wrap:wrap;gap:5px;}
.tag{padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;}
.tag-gov{background:rgba(46,196,182,.1);color:var(--mid);border:1px solid rgba(46,196,182,.25);}
.tag-priv{background:rgba(23,37,42,.06);color:var(--ink);border:1px solid var(--border);}
.tag-sch{background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;}
.tag-lang{background:#F0F9FF;color:#0369A1;border:1px solid #BAE6FD;}

.chip{display:inline-flex;align-items:center;gap:6px;background:rgba(46,196,182,.08);border:1.5px solid rgba(46,196,182,.25);border-radius:100px;padding:5px 14px;font-size:12px;font-weight:700;color:var(--mid);margin-bottom:20px;}

.comp-card{background:var(--white);border:1.5px solid var(--border);border-radius:16px;padding:24px;}
.comp-head{font-family:'Syne',sans-serif;font-size:15px;font-weight:800;color:var(--ink);margin-bottom:18px;padding-bottom:14px;border-bottom:1.5px solid var(--border);}
.comp-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(23,37,42,.04);}
.comp-label{font-size:12px;color:#9AACAC;font-weight:500;}
.comp-val{font-size:13px;color:var(--ink);font-weight:600;}

.ai-box{background:var(--pale);border:1.5px solid rgba(46,196,182,.2);border-radius:14px;padding:28px 32px;margin-top:16px;line-height:2;color:var(--ink);}
.ai-label{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin-bottom:14px;display:block;}
.gap-box{background:#FFFBEB;border:1.5px solid #FDE68A;border-radius:14px;padding:28px 32px;margin-top:16px;line-height:2;color:var(--ink);}

.values-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.val-card{background:var(--pale);border-radius:var(--r);padding:22px 16px;text-align:center;border:1.5px solid rgba(46,196,182,.15);}
.val-title{font-family:'Syne',sans-serif;font-size:14px;font-weight:800;color:var(--dark);margin-bottom:6px;}
.val-body{font-size:12px;color:var(--muted);}

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
div[data-testid="stExpander"] details>summary p{font-weight:700!important;color:var(--ink)!important;font-size:14px!important;}
div[data-testid="stExpander"] details>div{color:var(--muted)!important;line-height:1.85!important;font-size:14px!important;}
[data-testid="stChatMessage"]{background:var(--white)!important;border:1.5px solid var(--border)!important;border-radius:var(--r)!important;direction:rtl!important;margin-bottom:8px!important;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(46,196,182,.3);border-radius:4px;}
/* Hero full-bleed fix */
[data-testid="stMainBlockContainer"]{padding-left:0!important;padding-right:0!important;max-width:100%!important;}
[data-testid="block-container"]{padding:0!important;max-width:100%!important;}
.baw-hero{margin-left:calc(-50vw + 50%) !important;margin-right:calc(-50vw + 50%) !important;width:100vw !important;padding-left:calc(48px + (50vw - 50%)) !important;padding-right:calc(48px + (50vw - 50%)) !important;}
[data-testid="stMainBlockContainer"]{padding-left:0!important;padding-right:0!important;max-width:100%!important;}
[data-testid="block-container"]{padding:0!important;max-width:100%!important;}
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
N_UNIS = len(unis_raw)
N_PROGS = len(progs_raw)
N_CTRY = unis_raw["country"].nunique() if not unis_raw.empty else 0

st.markdown(CSS, unsafe_allow_html=True)

if "page" not in st.session_state: st.session_state.page = "الرئيسية"
PAGES = ["الرئيسية","بحث الجامعات","المقارنة","رُشد","البيانات","من نحن"]

# ── Nav bar: HTML visual + Streamlit buttons styled as nav ──
st.markdown("""<style>
.nav{background:#FEFFFF;border-bottom:1px solid #DEF2F1;display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:58px;box-shadow:0 1px 8px rgba(46,196,182,.07);}
.nav-logo{font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#17252A;}
.nav-logo span{color:#2EC4B6;}
.nav-links{display:flex;gap:2px;}
.nav-lnk{font-size:13px;font-weight:500;color:#6B7280;padding:6px 12px;border-radius:7px;cursor:pointer;transition:all .15s;}
.nav-lnk:hover{background:#EEF8F8;color:#2B7A77;}
.nav-lnk.on{background:#2EC4B6;color:#17252A;font-weight:700;}
/* Style Streamlit nav buttons to look like nav links */
div.nav-row button{background:transparent!important;border:none!important;color:#6B7280!important;font-size:13px!important;font-weight:500!important;font-family:'IBM Plex Sans Arabic',sans-serif!important;padding:6px 12px!important;border-radius:7px!important;height:auto!important;box-shadow:none!important;transition:all .15s!important;}
div.nav-row button:hover{background:#EEF8F8!important;color:#2B7A77!important;}
div.nav-row{display:flex;gap:2px;align-items:center;}
/* sticky nav */
[data-testid="stMainBlockContainer"]{padding-top:58px!important;}
</style>""", unsafe_allow_html=True)

# الـ nav bar: لوغو + أزرار Streamlit مصممة كـ nav
logo_col, nav_area = st.columns([1, 4])
with logo_col:
    st.markdown("<div style=\"font-family:'Syne',sans-serif;font-size:20px;font-weight:800;color:#17252A;padding:12px 0 12px 16px;\">بو<span style=\"color:#2EC4B6;\">صلة</span></div>", unsafe_allow_html=True)
with nav_area:
    st.markdown('<div class="nav-row" style="display:flex;gap:2px;justify-content:flex-end;padding:8px 0;">', unsafe_allow_html=True)
    nc = st.columns(len(PAGES))
    for i, name in enumerate(PAGES):
        is_active = st.session_state.page == name
        btn_style = "background:#2EC4B6!important;color:#17252A!important;font-weight:700!important;" if is_active else ""
        if nc[i].button(name, key=f"nav_{name}", use_container_width=True):
            st.session_state.page = name; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# خط فاصل تحت الـ nav
st.markdown('<hr style="margin:0;border:none;border-top:1px solid #DEF2F1;">', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# الرئيسية
# ══════════════════════════════════════════════
if st.session_state.page == "الرئيسية":

    # ── Hero: تايبوغرافي كبير، وسط، بدون background ──
    st.markdown("""<style>
.hero-tag{display:inline-flex;align-items:center;gap:7px;background:rgba(46,196,182,.1);border:1px solid rgba(46,196,182,.25);border-radius:100px;padding:5px 16px;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#2B7A77;}
.hero-tag-dot{width:5px;height:5px;border-radius:50%;background:#2EC4B6;display:inline-block;animation:pulse 2s infinite;}
.hero-big{font-family:'Syne',sans-serif;font-size:88px;font-weight:800;color:#17252A;line-height:0.95;letter-spacing:-4px;margin:28px 0 0;}
.hero-big em{color:#2EC4B6;font-style:normal;}
.hero-rule{width:56px;height:3px;background:#2EC4B6;border-radius:2px;margin:28px auto;}
.hero-sub{font-size:17px;color:#3B7A77;line-height:1.8;max-width:560px;margin:0 auto 36px;}
.hero-btns{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:52px;}
.hero-btn-p{background:#17252A;color:#FEFFFF;font-weight:700;font-size:13px;padding:13px 28px;border-radius:10px;cursor:pointer;letter-spacing:0.2px;}
.hero-btn-s{background:white;color:#2B7A77;font-weight:600;font-size:13px;padding:13px 28px;border-radius:10px;border:1.5px solid #DEF2F1;cursor:pointer;}
.hero-stats{display:flex;justify-content:center;align-items:center;gap:0;border:1px solid #DEF2F1;border-radius:16px;overflow:hidden;max-width:480px;margin:0 auto;}
.hero-stat-item{flex:1;padding:18px 16px;text-align:center;border-left:1px solid #DEF2F1;}
.hero-stat-item:last-child{border-left:none;}
.hero-stat-n{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#17252A;line-height:1;}
.hero-stat-l{font-size:11px;color:#9AACAC;font-weight:500;margin-top:4px;letter-spacing:0.3px;}
</style>""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="text-align:center;padding:72px 40px 0;direction:rtl;">
  <div style="display:flex;justify-content:center;margin-bottom:0;">
    <div class="hero-tag"><span class="hero-tag-dot"></span>الدليل الذكي للتعليم الخليجي</div>
  </div>
  <div class="hero-big">بو<em>صلة</em></div>
  <div class="hero-rule"></div>
  <div class="hero-sub">اكتشف الجامعات، قارن التخصصات، واتخذ قرارك التعليمي بثقة<br>مع مستشار ذكي يتحدث العربية</div>
  <div class="hero-btns">
    <div class="hero-btn-p">ابدأ البحث الآن</div>
    <div class="hero-btn-s">تحدّث مع رُشد</div>
  </div>
  <div class="hero-stats">
    <div class="hero-stat-item">
      <div class="hero-stat-n">{N_UNIS}+</div>
      <div class="hero-stat-l">جامعة</div>
    </div>
    <div class="hero-stat-item">
      <div class="hero-stat-n">{N_CTRY}</div>
      <div class="hero-stat-l">دولة خليجية</div>
    </div>
    <div class="hero-stat-item">
      <div class="hero-stat-n">{N_PROGS}+</div>
      <div class="hero-stat-l">برنامج</div>
    </div>
    <div class="hero-stat-item">
      <div class="hero-stat-n">AI</div>
      <div class="hero-stat-l">توصيات ذكية</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # باقي الصفحة
    st.markdown("""
<div style="height:64px;display:flex;align-items:center;justify-content:center;margin:0;">
  <div style="display:flex;align-items:center;gap:12px;color:#9AACAC;font-size:12px;font-weight:500;letter-spacing:1px;text-transform:uppercase;">
    <div style="width:40px;height:1px;background:#DEF2F1;"></div>
    ماذا يقدم بوصلة
    <div style="width:40px;height:1px;background:#DEF2F1;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="max-width:1160px;margin:0 auto;padding:0 40px 60px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-h" style="text-align:center;margin-bottom:36px;">منصة واحدة — كل خياراتك الأكاديمية</div>', unsafe_allow_html=True)
    st.markdown("""<div class="feat-grid">

  <div class="feat-card">
    <svg viewBox="0 0 80 64" style="width:64px;height:52px;margin-bottom:16px;" xmlns="http://www.w3.org/2000/svg">
      <rect x="8" y="16" width="56" height="40" rx="8" fill="#EEF8F8" stroke="#DEF2F1" stroke-width="1.5"/>
      <rect x="16" y="24" width="40" height="5" rx="2.5" fill="#2EC4B6" opacity="0.6"/>
      <rect x="16" y="33" width="32" height="3.5" rx="1.75" fill="#DEF2F1"/>
      <rect x="16" y="40" width="36" height="3.5" rx="1.75" fill="#DEF2F1"/>
      <rect x="16" y="47" width="24" height="3.5" rx="1.75" fill="#DEF2F1"/>
      <circle cx="58" cy="18" r="14" fill="#2EC4B6" opacity="0.15"/>
      <circle cx="58" cy="18" r="9" fill="#2EC4B6" opacity="0.25"/>
      <text x="53" y="23" font-size="11" fill="#2B7A77" font-weight="800">AI</text>
    </svg>
    <div class="feat-num">01 — المستشار الذكي</div>
    <div class="feat-title">رُشد</div>
    <div class="feat-body">تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح أفضل الجامعات من قاعدة بياناتنا مع شرح أسباب كل توصية.</div>
  </div>

  <div class="feat-card">
    <svg viewBox="0 0 80 64" style="width:64px;height:52px;margin-bottom:16px;" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="44" width="12" height="16" rx="3" fill="#2EC4B6" opacity="0.4"/>
      <rect x="22" y="32" width="12" height="28" rx="3" fill="#2EC4B6" opacity="0.6"/>
      <rect x="38" y="20" width="12" height="40" rx="3" fill="#2EC4B6" opacity="0.8"/>
      <rect x="54" y="10" width="12" height="50" rx="3" fill="#2EC4B6"/>
      <polyline points="12,44 28,32 44,20 60,10" stroke="#17252A" stroke-width="2" fill="none" stroke-linecap="round"/>
      <circle cx="12" cy="44" r="3" fill="#17252A"/>
      <circle cx="28" cy="32" r="3" fill="#17252A"/>
      <circle cx="44" cy="20" r="3" fill="#17252A"/>
      <circle cx="60" cy="10" r="3" fill="#17252A"/>
    </svg>
    <div class="feat-num">02 — الإحصاء والتحليل</div>
    <div class="feat-title">لوحة البيانات</div>
    <div class="feat-body">مخططات تفاعلية وتقارير ذكية تحوّل بيانات التعليم الخليجي إلى رؤى إحصائية واضحة وقابلة للمقارنة.</div>
  </div>

  <div class="feat-card">
    <svg viewBox="0 0 80 64" style="width:64px;height:52px;margin-bottom:16px;" xmlns="http://www.w3.org/2000/svg">
      <rect x="4" y="12" width="32" height="40" rx="7" fill="#EEF8F8" stroke="#2EC4B6" stroke-width="1.5"/>
      <rect x="44" y="12" width="32" height="40" rx="7" fill="#EEF8F8" stroke="#DEF2F1" stroke-width="1.5"/>
      <rect x="10" y="20" width="20" height="4" rx="2" fill="#2EC4B6" opacity="0.7"/>
      <rect x="10" y="28" width="16" height="3" rx="1.5" fill="#DEF2F1"/>
      <rect x="10" y="35" width="18" height="3" rx="1.5" fill="#DEF2F1"/>
      <rect x="50" y="20" width="20" height="4" rx="2" fill="#9AACAC" opacity="0.5"/>
      <rect x="50" y="28" width="16" height="3" rx="1.5" fill="#DEF2F1"/>
      <rect x="50" y="35" width="18" height="3" rx="1.5" fill="#DEF2F1"/>
      <line x1="40" y1="20" x2="40" y2="52" stroke="#DEF2F1" stroke-width="1.5" stroke-dasharray="3,3"/>
    </svg>
    <div class="feat-num">03 — القرار المدروس</div>
    <div class="feat-title">المقارنة</div>
    <div class="feat-body">قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — النوع، المنح، الترتيب، والروابط الرسمية في مكان واحد.</div>
  </div>

</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">رؤيتنا ورسالتنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">نحو قرار تعليمي أفضل</div>', unsafe_allow_html=True)
    with st.expander("رؤيتنا", expanded=True):
        st.markdown("نسعى في بوصلة إلى إعادة تعريف تجربة اختيار التعليم في الخليج، عبر منصة ذكية توجّه الشباب نحو تخصصاتهم وجامعاتهم المناسبة، وتحوّل القرار التعليمي من حيرة فردية إلى مسار واضح مدروس.")
    with st.expander("رسالتنا"):
        st.markdown("تلتزم بوصلة بتمكين الطلبة وأولياء الأمور من اتخاذ قرارات تعليمية دقيقة من خلال منصة ذكية تعتمد على الذكاء الاصطناعي والبيانات الموثوقة.")
    with st.expander("قيمنا"):
        st.markdown("الوضوح · العدالة · التمكين · الابتكار · الموثوقية")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    if b1.button("المستشار رُشد",  use_container_width=True): st.session_state.page="رُشد"; st.rerun()
    if b2.button("تحليل البيانات", use_container_width=True): st.session_state.page="البيانات"; st.rerun()
    if b3.button("بحث الجامعات",  use_container_width=True): st.session_state.page="بحث الجامعات"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# بحث الجامعات
# ══════════════════════════════════════════════
elif st.session_state.page == "بحث الجامعات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">الاستكشاف</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">بحث الجامعات</div>', unsafe_allow_html=True)

    q = st.text_input("", placeholder="ابحث عن جامعة، مدينة، أو دولة...").strip().lower()
    c1,c2,c3,c4,c5 = st.columns([1.2,1,1,1.2,1])
    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c1.selectbox("الدولة",   ["الكل"]+countries)
    types_    = sorted([x for x in unis["type"].unique() if str(x).strip()])
    uni_type  = c2.selectbox("النوع",    ["الكل"]+types_)
    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c3.selectbox("المرحلة", ["الكل"]+levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c4.selectbox("التخصص",  ["الكل"]+majors_)
    yn        = c5.selectbox("المنح",   ["الكل","متاحة","غير متاحة"])

    f = unis.copy()
    if country  != "الكل": f = f[f["country"]==country]
    if uni_type != "الكل": f = f[f["type"]==uni_type]
    if yn=="متاحة":         f = f[f["scholarship"].apply(uni_has_sch)]
    if yn=="غير متاحة":     f = f[~f["scholarship"].apply(uni_has_sch)]
    if q:
        m = (f["name_en"].str.lower().str.contains(q,na=False)|f["name_ar"].str.lower().str.contains(q,na=False)|f["city"].str.lower().str.contains(q,na=False))
        f = f[m]
    if (major!="الكل" or level!="الكل") and not progs.empty:
        pm=progs.copy()
        if major!="الكل": pm=pm[pm["major_field"]==major]
        if level!="الكل": pm=pm[pm["level"]==level]
        f=f[f["uni_id"].isin(pm["uni_id"].unique())]

    st.markdown(f'<div class="chip">{len(f)} نتيجة</div>', unsafe_allow_html=True)
    if f.empty:
        st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
    else:
        for _, row in f.head(30).iterrows():
            is_pub   = str(row["type"]).strip().lower() in ["public","حكومية"]
            type_tag = '<span class="tag tag-gov">حكومية</span>' if is_pub else '<span class="tag tag-priv">خاصة</span>'
            sch_tag  = '<span class="tag tag-sch">منحة دراسية</span>' if uni_has_sch(str(row["scholarship"])) else ""
            lang_tags=""
            if not progs.empty:
                for lg in progs[progs["uni_id"]==str(row["uni_id"])]["language"].dropna().unique()[:2]:
                    lang_tags+=f'<span class="tag tag-lang">{lg}</span>'
            links=""
            if str(row.get("website","")).strip(): links+=f'<a href="{row["website"]}" target="_blank" class="uni-link">الموقع الرسمي</a>'
            if str(row.get("admissions_url","")).strip(): links+=f'<a href="{row["admissions_url"]}" target="_blank" class="uni-link">القبول</a>'
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

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">التقييم المقارن</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">مقارنة الجامعات</div>', unsafe_allow_html=True)

    unis["uni_id"]=unis["uni_id"].astype(str).str.strip()
    unis=unis[unis["uni_id"].ne("")&unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"]=unis["name_ar"]+" — "+unis["name_en"]+" ("+unis["city"]+", "+unis["country"]+")"
    label_map=dict(zip(unis["uni_id"],unis["label"]))
    unis=unis.sort_values(["country","city","name_en"],na_position="last")

    selected=st.multiselect("اختر من ٢ إلى ٤ جامعات",options=unis["uni_id"].tolist(),format_func=lambda x:label_map.get(str(x),str(x)),max_selections=4)
    if len(selected)<2:
        st.info("يرجى اختيار جامعتين على الأقل.")
        st.markdown('</div>', unsafe_allow_html=True); st.stop()

    comp=unis[unis["uni_id"].isin(selected)].copy()
    cols_c=st.columns(len(selected))
    for i,uid in enumerate(selected):
        row=comp[comp["uni_id"]==uid].iloc[0]
        with cols_c[i]:
            sch=(str(row.get("scholarship","")).strip() or "—")
            rank=(str(row.get("ranking_source","")).strip()+" "+str(row.get("ranking_value","")).strip()).strip() or "—"
            st.markdown(f"""<div class="comp-card">
  <div class="comp-head">{row['name_ar']}</div>
  <div class="comp-row"><span class="comp-label">الموقع</span><span class="comp-val">{row['city']}, {row['country']}</span></div>
  <div class="comp-row"><span class="comp-label">النوع</span><span class="comp-val">{row['type']}</span></div>
  <div class="comp-row"><span class="comp-label">المنح</span><span class="comp-val">{sch}</span></div>
  <div class="comp-row"><span class="comp-label">الترتيب</span><span class="comp-val">{rank}</span></div>
</div>""", unsafe_allow_html=True)
            st.write("")
            if str(row.get("website","")).strip():        st.link_button("الموقع الرسمي",      row["website"],        use_container_width=True)
            if str(row.get("admissions_url","")).strip(): st.link_button("القبول والتسجيل",    row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url","")).strip():   st.link_button("البرامج الأكاديمية", row["programs_url"],   use_container_width=True)

    progs=progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-tag">البرامج الأكاديمية</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-h-sm">البرامج المتاحة للجامعات المختارة</div>', unsafe_allow_html=True)
        comp_progs=progs[progs["uni_id"].isin(selected)].copy()
        if comp_progs.empty:
            st.info("لا تتوفر بيانات برامج للجامعات المختارة.")
        else:
            show_cols=[c for c in ["uni_id","program_name_ar","program_name_en","level","major_field","language","duration_years"] if c in comp_progs.columns]
            rename_map={"uni_id":"الجامعة","program_name_ar":"البرنامج","program_name_en":"Program","level":"المرحلة","major_field":"التخصص","language":"اللغة","duration_years":"المدة (سنوات)"}
            display_df=comp_progs[show_cols].rename(columns=rename_map)
            if "الجامعة" in display_df.columns:
                id_to_ar=dict(zip(unis["uni_id"],unis["name_ar"]))
                display_df["الجامعة"]=display_df["الجامعة"].map(id_to_ar).fillna(display_df["الجامعة"])
            st.dataframe(display_df,use_container_width=True,hide_index=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">الذكاء الاصطناعي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm">المقارنة الذكية</div>', unsafe_allow_html=True)
    profile_txt=st.text_input("",placeholder="ملفك الأكاديمي (اختياري) — مثال: طالب هندسة، IELTS 6.5، يفضل المنح",key="comp_profile",label_visibility="collapsed")
    if st.button("اطلب مقارنة ذكية",use_container_width=True,key="btn_compare_ai"):
        unis_data=[comp[comp["uni_id"]==uid].iloc[0].to_dict() for uid in selected if uid in comp["uni_id"].values]
        with st.spinner("جاري تحليل الجامعات..."):
            ai_result=compare_unis_ai(unis_data,profile_txt)
        st.markdown(f'<div class="ai-box"><span class="ai-label">المقارنة الذكية</span>{ai_result}</div>',unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# رُشد
# ══════════════════════════════════════════════
elif st.session_state.page == "رُشد":
    unis=unis_raw.copy(); progs=progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">المستشار الأكاديمي الذكي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">رُشد</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#9AACAC;font-size:14px;margin-bottom:28px;margin-top:-14px;">تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح لك الجامعات المناسبة</p>', unsafe_allow_html=True)

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context=build_unis_context(unis,progs)

    st.markdown('<div class="section-tag">التحليل الفوري</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm">التحليل السريع</div>', unsafe_allow_html=True)
    qm_c1,qm_c2,qm_c3=st.columns(3)
    countries_list=sorted([x for x in unis["country"].unique() if str(x).strip()])
    qm_country=qm_c1.selectbox("الدولة المفضلة",["الكل"]+countries_list,key="qm_country")
    qm_major=qm_c2.text_input("التخصص المطلوب",placeholder="مثال: هندسة الحاسب",key="qm_major")
    qm_ielts=qm_c3.text_input("درجة IELTS",placeholder="مثال: 6.5",key="qm_ielts")

    if st.button("حلّل بسرعة",use_container_width=True,key="btn_quick_match"):
        if not qm_major.strip():
            st.warning("يرجى إدخال التخصص المطلوب.")
        else:
            profile_data={"country":qm_country,"major":qm_major,"ielts":qm_ielts or "غير محدد"}
            with st.spinner("جاري التحليل..."):
                qm_result=quick_match(profile_data,st.session_state.unis_context)
            top3=qm_result.get("top_3",[])
            advice=qm_result.get("advice","")
            missing=qm_result.get("missing",[])
            if top3:
                qr_cols=st.columns(len(top3))
                for i,item in enumerate(top3[:3]):
                    uid=item.get("uni_id",""); name_ar=item.get("name_ar",uid)
                    reason=item.get("reason",""); fit=item.get("fit","مناسب")
                    uni_row=unis[unis["uni_id"]==uid]
                    city_country=""; sch_tag=""
                    if not uni_row.empty:
                        r=uni_row.iloc[0]; city_country=f"{r.get('city','')}, {r.get('country','')}"
                        if uni_has_sch(str(r.get("scholarship",""))): sch_tag='<span class="tag tag-sch">منحة دراسية</span>'
                    with qr_cols[i]:
                        st.markdown(f"""<div class="uni-card" style="flex-direction:column;align-items:flex-start;border-top:3px solid var(--teal);">
  <div class="uni-name">{name_ar}</div><div class="uni-sub">{city_country}</div>
  <div style="color:#9AACAC;font-size:13px;margin:8px 0;line-height:1.7;">{reason}</div>
  <div class="tags">{sch_tag}<span class="tag tag-gov">{fit}</span></div>
</div>""", unsafe_allow_html=True)
            if advice:
                st.markdown(f'<div class="ai-box" style="margin-top:16px;"><span class="ai-label">نصيحة رُشد</span>{advice}</div>',unsafe_allow_html=True)
            if missing:
                missing_html="".join([f'<span class="tag tag-sch" style="margin:3px;">{m}</span>' for m in missing])
                st.markdown(f'<div style="margin-top:10px;"><span style="color:#9AACAC;font-size:13px;margin-left:8px;">قد تحتاج إلى:</span>{missing_html}</div>',unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages=[{"role":"assistant","content":"مرحباً، أنا رُشد.\n\nأخبرني عن نفسك:\n- التخصص الذي تريده\n- الدولة المفضلة\n- معدلك التقريبي\n- هل عندك IELTS وكم درجتك؟\n\nوسأرشّح لك الجامعات المناسبة."}]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"],avatar="🧭" if msg["role"]=="assistant" else "🎓"):
            st.markdown(msg["content"])

    if user_input:=st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":user_input})
        with st.chat_message("user",avatar="🎓"): st.markdown(user_input)
        with st.chat_message("assistant",avatar="🧭"):
            with st.spinner(""):
                history=[m for m in st.session_state.rushd_messages if not(m["role"]=="assistant" and "مرحباً" in m["content"])]
                reply=chat_rushd(history,st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role":"assistant","content":reply})

    if len(st.session_state.rushd_messages)>1:
        if st.button("محادثة جديدة"): st.session_state.rushd_messages=[]; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# البيانات
# ══════════════════════════════════════════════
elif st.session_state.page == "البيانات":
    unis=unis_raw.copy(); progs=progs_raw.copy()
    if unis.empty: st.error("لا تتوفر بيانات."); st.stop()

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">الإحصاء والتحليل</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">لوحة البيانات</div>', unsafe_allow_html=True)

    by_country=unis["country"].value_counts().to_dict()
    by_type=unis["type"].value_counts().to_dict()
    with_sch=int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields=progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang=progs["language"].value_counts().to_dict() if not progs.empty else {}

    st.markdown(f"""<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:36px;">
  <div class="hero-stat" style="background:var(--pale);border-color:rgba(46,196,182,.2);min-width:130px;"><div class="hero-stat-n" style="font-size:24px;">{N_UNIS}</div><div class="hero-stat-l" style="color:var(--muted);">إجمالي الجامعات</div></div>
  <div class="hero-stat" style="background:var(--pale);border-color:rgba(46,196,182,.2);min-width:130px;"><div class="hero-stat-n" style="font-size:24px;">{N_PROGS}</div><div class="hero-stat-l" style="color:var(--muted);">إجمالي البرامج</div></div>
  <div class="hero-stat" style="background:var(--pale);border-color:rgba(46,196,182,.2);min-width:130px;"><div class="hero-stat-n" style="font-size:24px;">{with_sch}</div><div class="hero-stat-l" style="color:var(--muted);">تقدم منحاً</div></div>
  <div class="hero-stat" style="background:var(--pale);border-color:rgba(46,196,182,.2);min-width:130px;"><div class="hero-stat-n" style="font-size:24px;">{N_CTRY}</div><div class="hero-stat-l" style="color:var(--muted);">دولة خليجية</div></div>
</div>""", unsafe_allow_html=True)

    T=dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="IBM Plex Sans Arabic",color="#9AACAC"),margin=dict(l=10,r=10,t=38,b=10),height=290)

    ch1,ch2,ch3=st.columns(3)
    with ch1:
        fig=px.bar(x=list(by_country.values()),y=list(by_country.keys()),orientation="h",title="الجامعات حسب الدولة",color_discrete_sequence=["#2EC4B6"])
        fig.update_layout(**T); fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True)
    with ch2:
        fig=px.pie(values=list(by_type.values()),names=list(by_type.keys()),title="حكومية / خاصة",hole=0.55,color_discrete_sequence=["#2EC4B6","#17252A","#3AAFA9"])
        fig.update_layout(**T); fig.update_traces(textfont_color="white"); st.plotly_chart(fig,use_container_width=True)
    with ch3:
        if top_fields:
            fig=px.bar(x=list(top_fields.keys()),y=list(top_fields.values()),title="أبرز التخصصات",color_discrete_sequence=["#3AAFA9"])
            fig.update_layout(**T,xaxis_tickangle=-30); fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True)

    ch4,ch5=st.columns(2)
    with ch4:
        pct=round(with_sch/max(len(unis),1)*100,1)
        fig=go.Figure(go.Indicator(mode="gauge+number",value=pct,
            title={"text":"نسبة الجامعات التي تقدم منحاً %","font":{"family":"IBM Plex Sans Arabic","color":"#9AACAC","size":13}},
            number={"font":{"color":"#2EC4B6","family":"IBM Plex Sans Arabic"}},
            gauge={"axis":{"range":[0,100],"tickcolor":"#DEF2F1"},"bar":{"color":"#2EC4B6"},"bgcolor":"rgba(0,0,0,0)","bordercolor":"rgba(46,196,182,.1)","steps":[{"range":[0,100],"color":"rgba(46,196,182,.05)"}]}))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(family="IBM Plex Sans Arabic",color="#9AACAC"),height=260,margin=dict(l=20,r=20,t=38,b=10))
        st.plotly_chart(fig,use_container_width=True)
    with ch5:
        if by_lang:
            fig=px.bar(x=list(by_lang.keys()),y=list(by_lang.values()),title="لغات الدراسة",color_discrete_sequence=["#17252A"])
            fig.update_layout(**T,height=260); fig.update_traces(marker_line_width=0); st.plotly_chart(fig,use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">المنح الدراسية</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm">توزيع المنح حسب الدولة</div>', unsafe_allow_html=True)

    if not unis.empty and "scholarship" in unis.columns:
        sch_data=[]
        for _,row in unis.iterrows():
            ctry=str(row.get("country","")).strip(); sch=str(row.get("scholarship","")).strip()
            if not ctry or ctry=="nan": continue
            for cat in ["Local","GCC","International"]:
                sch_data.append({"الدولة":ctry,"نوع المنحة":cat,"عدد":1 if cat in sch else 0})
        sch_df=pd.DataFrame(sch_data).groupby(["الدولة","نوع المنحة"],as_index=False)["عدد"].sum()
        sch_df=sch_df[sch_df["عدد"]>0]
        if not sch_df.empty:
            fig_sch=px.bar(sch_df,x="عدد",y="الدولة",color="نوع المنحة",orientation="h",barmode="stack",title="عدد الجامعات التي تقدم منحاً لكل فئة حسب الدولة",color_discrete_map={"Local":"#2EC4B6","GCC":"#17252A","International":"#3AAFA9"})
            fig_sch.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="IBM Plex Sans Arabic",color="#9AACAC"),margin=dict(l=10,r=10,t=38,b=10),height=320,legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#9AACAC")))
            fig_sch.update_traces(marker_line_width=0); st.plotly_chart(fig_sch,use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    col_r,col_g=st.columns(2)
    with col_r:
        st.markdown('<div class="section-h-sm">التقرير التحليلي الذكي</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#9AACAC;margin-bottom:14px;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير",use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                report=generate_dashboard_report({"total_unis":len(unis),"by_country":by_country,"by_type":by_type,"top_fields":top_fields,"by_language":by_lang,"with_scholarships":with_sch,"total_progs":len(progs)})
            st.markdown(f'<div class="ai-box"><span class="ai-label">التقرير التحليلي</span>{report}</div>',unsafe_allow_html=True)
    with col_g:
        st.markdown('<div class="section-h-sm">تحليل الفجوات التعليمية</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#9AACAC;margin-bottom:14px;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات",use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps=analyze_gaps(unis,progs)
            st.markdown(f'<div class="gap-box">{gaps}</div>',unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# من نحن
# ══════════════════════════════════════════════
elif st.session_state.page == "من نحن":
    st.markdown('<div class="wrap-sm">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">هويتنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">من نحن</div>', unsafe_allow_html=True)
    st.markdown("""<div style="font-size:15px;color:#2B7A77;line-height:2;margin-bottom:40px;">
<p style="color:#17252A;font-size:17px;font-weight:600;margin-bottom:16px;">منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.</p>
<p>جاءت فكرة بوصلة استجابةً لتحدٍ واقعي يواجه الكثير من الطلبة — تشتّت المعلومات وصعوبة المقارنة بين الجامعات والبرامج وتعدد المصادر غير الموثوقة.</p>
<p>نعمل على جمع البيانات التعليمية الخليجية وتنظيمها وتقديمها بطريقة مبسطة، مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على فهم خياراته واتخاذ قراره بثقة.</p>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">قيمنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm" style="margin-bottom:20px;">ما يحركنا</div>', unsafe_allow_html=True)
    st.markdown("""<div class="values-grid">
  <div class="val-card"><div class="val-title">الوضوح</div><div class="val-body">تبسيط القرار التعليمي</div></div>
  <div class="val-card"><div class="val-title">العدالة</div><div class="val-body">عرض الخيارات دون تحيّز</div></div>
  <div class="val-card"><div class="val-title">التمكين</div><div class="val-body">فهم الذات قبل التخصص</div></div>
  <div class="val-card"><div class="val-title">الابتكار</div><div class="val-body">AI في خدمة التعليم</div></div>
</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">تواصل</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h-sm" style="margin-bottom:20px;">تواصل معنا</div>', unsafe_allow_html=True)
    ca,cb=st.columns(2)
    with ca:
        st.text_input("الاسم",placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني",placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك",placeholder="اكتب رسالتك هنا...",height=120)
    if st.button("إرسال",use_container_width=True):
        st.success("تم الاستلام. شكراً لتواصلك.")
    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
    st.markdown('</div>', unsafe_allow_html=True)
