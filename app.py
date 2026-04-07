import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_engine import build_unis_context, chat_rushd, generate_dashboard_report, analyze_gaps, compare_unis_ai, quick_match

st.set_page_config(page_title="بوصلة", layout="wide", initial_sidebar_state="collapsed")

# ═══════════════════════════════════════════
#  DESIGN SYSTEM  —  inspired by prize.gaserc.org
# ═══════════════════════════════════════════
# Colors
C = dict(
    nav   = "#102a27",   # dark teal — nav + hero
    sec1  = "#364b49",   # slate green — accent sections
    sage  = "#d6e8d6",   # light sage — card backgrounds
    base  = "#fffef6",   # warm off-white — page bg
    ink   = "#302b26",   # dark charcoal — main text
    ink2  = "#364b49",   # blue-green — secondary text
    teal  = "#2EC4B6",   # brand accent
    white = "#fffef6",
)

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body,[class*="css"]{{
  font-family:'IBM Plex Sans Arabic',sans-serif!important;
  direction:rtl!important;
  background:{C['base']}!important;
  color:{C['ink']}!important;
}}

/* ── Chrome ── */
[data-testid="stSidebar"],[data-testid="stSidebarNav"],
button[kind="header"],[data-testid="collapsedControl"],
[data-testid="stDecoration"],footer,#MainMenu{{display:none!important;}}

/* ── App containers ── */
[data-testid="stApp"],[data-testid="stAppViewContainer"]{{background:{C['base']}!important;}}
[data-testid="stMain"]{{background:{C['base']}!important;padding:0!important;}}
[data-testid="stMainBlockContainer"]{{
  padding:0!important;max-width:100%!important;background:{C['base']}!important;
}}
[data-testid="block-container"]{{padding:0!important;max-width:100%!important;}}

/* ── RTL inputs ── */
input,textarea,[role="textbox"]{{direction:rtl!important;text-align:right!important;}}
div[data-baseweb="select"] *{{direction:rtl!important;}}
label{{font-family:'IBM Plex Sans Arabic',sans-serif!important;color:{C['ink2']}!important;font-size:14px!important;font-weight:500!important;}}

/* ── Text inputs ── */
.stTextInput>div>div{{background:#fff!important;border:1px solid rgba(54,75,73,.25)!important;border-radius:0!important;}}
.stTextInput>div>div:focus-within{{border-color:{C['teal']}!important;box-shadow:none!important;}}
.stTextInput>div>div>input{{color:{C['ink']}!important;background:transparent!important;font-size:15px!important;}}
input::placeholder,textarea::placeholder{{color:#9AACAC!important;opacity:1!important;}}
.stTextArea>div>div{{background:#fff!important;border:1px solid rgba(54,75,73,.25)!important;border-radius:0!important;}}
div[data-baseweb="select"]>div{{background:#fff!important;border:1px solid rgba(54,75,73,.25)!important;border-radius:0!important;color:{C['ink']}!important;}}
div[data-baseweb="select"] *{{color:{C['ink']}!important;}}
div[data-baseweb="popover"] li{{background:#fff!important;color:{C['ink']}!important;}}
div[data-baseweb="popover"] li:hover{{background:{C['sage']}!important;color:{C['ink']}!important;}}

/* ── Buttons ── */
.stButton>button{{
  background:transparent!important;
  border:1px solid {C['ink']}!important;
  color:{C['ink']}!important;
  border-radius:100px!important;
  font-family:'IBM Plex Sans Arabic',sans-serif!important;
  font-size:15px!important;font-weight:600!important;
  padding:11px 28px!important;
  transition:all .2s!important;
  letter-spacing:.2px!important;
}}
.stButton>button:hover{{
  background:{C['ink']}!important;color:{C['base']}!important;
}}
.stLinkButton a{{
  border:1px solid rgba(54,75,73,.3)!important;border-radius:100px!important;
  color:{C['ink2']}!important;font-size:14px!important;font-weight:600!important;
  padding:8px 18px!important;background:transparent!important;
}}
.stLinkButton a:hover{{background:{C['sec1']}!important;color:{C['base']}!important;border-color:{C['sec1']}!important;}}
div[data-testid="stExpander"]{{background:#fff!important;border:1px solid rgba(54,75,73,.2)!important;border-radius:0!important;margin-bottom:8px!important;}}
[data-testid="stChatMessage"]{{background:#fff!important;border:1px solid rgba(54,75,73,.2)!important;border-radius:0!important;direction:rtl!important;margin-bottom:8px!important;}}
::-webkit-scrollbar{{width:4px;}}
::-webkit-scrollbar-thumb{{background:rgba(54,75,73,.3);border-radius:0;}}

/* ══ NAV ROW ══ */
[data-testid="stHorizontalBlock"]:first-of-type{{
  background:{C['nav']}!important;
  padding:0 80px!important;
  gap:0!important;
  align-items:stretch!important;
  min-height:64px!important;
  flex-wrap:nowrap!important;
  margin:0!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]{{
  display:flex!important;align-items:center!important;justify-content:center!important;
  padding:0!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child{{
  justify-content:flex-end!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type button{{
  background:transparent!important;border:none!important;box-shadow:none!important;
  color:rgba(214,232,214,.65)!important;
  font-size:14px!important;font-weight:400!important;
  font-family:'IBM Plex Sans Arabic',sans-serif!important;
  padding:0 12px!important;border-radius:0!important;
  white-space:nowrap!important;height:64px!important;min-height:64px!important;
  border-bottom:2px solid transparent!important;
  transition:all .15s!important;width:100%!important;
}}
[data-testid="stHorizontalBlock"]:first-of-type button:hover{{
  color:{C['base']}!important;border-bottom-color:rgba(214,232,214,.4)!important;
  background:rgba(255,255,255,.04)!important;
}}
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

# ── Session ──
if "page" not in st.session_state: st.session_state.page = "الرئيسية"
PAGES = ["الرئيسية","بحث الجامعات","المقارنة","رُشد","البيانات","من نحن"]
active_idx = PAGES.index(st.session_state.page)

# ══════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════
_nc = st.columns([1.8] + [1]*len(PAGES))
with _nc[0]:
    st.markdown(f'<span style="font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:{C["base"]};letter-spacing:-.5px;">بو<span style="color:{C["teal"]};">صلة</span></span>', unsafe_allow_html=True)
for _i, _name in enumerate(PAGES):
    with _nc[_i + 1]:
        if st.button(_name, key=f"nav_{_name}", use_container_width=True):
            st.session_state.page = _name; st.rerun()

# Active underline
st.markdown(f"""<style>
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:nth-child({active_idx+2}) button{{
  color:{C['base']}!important;font-weight:600!important;
  border-bottom:2px solid {C['teal']}!important;
}}
</style>""", unsafe_allow_html=True)

# ── Shared layout helpers ──
PAD = "padding:0 80px;"
MAX = "max-width:1257px;margin:0 auto;"

def wrap(content, bg=C['base'], extra_style=""):
    return f'<div style="background:{bg};{extra_style}"><div style="{MAX}{PAD}">{content}</div></div>'

def section_label(t):
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:10px;text-align:right;">{t}</p>', unsafe_allow_html=True)

def section_title(t, color=None):
    col = color or C['ink']
    st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{col};margin-bottom:28px;text-align:right;line-height:1.3;">{t}</h2>', unsafe_allow_html=True)

def section_title_sm(t, color=None):
    col = color or C['ink']
    st.markdown(f'<h3 style="font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:{col};margin-bottom:18px;text-align:right;">{t}</h3>', unsafe_allow_html=True)

def divider(color="rgba(54,75,73,.12)"):
    st.markdown(f'<div style="height:1px;background:{color};margin:48px 0;"></div>', unsafe_allow_html=True)

def page_pad():
    st.markdown(f'<div style="{PAD}padding-top:0;padding-bottom:0;">', unsafe_allow_html=True)

def back_btn():
    if st.button("← الرئيسية", key="back_btn"):
        st.session_state.page = "الرئيسية"; st.rerun()
    st.markdown('<div style="margin-bottom:32px;"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# الرئيسية
# ══════════════════════════════════════════════
if st.session_state.page == "الرئيسية":

    # ── Hero ──
    st.markdown(f"""
<div style="background:{C['nav']};padding:120px 80px 100px;direction:rtl;">
  <div style="{MAX}">
    <p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C['teal']};margin-bottom:20px;text-align:center;">الدليل الذكي للتعليم الخليجي</p>
    <h1 style="font-family:Syne,sans-serif;font-size:64px;font-weight:800;color:{C['base']};line-height:1;letter-spacing:-3px;text-align:center;margin-bottom:16px;">
      بو<span style="color:{C['teal']};">صلة</span>
    </h1>
    <div style="width:48px;height:3px;background:{C['teal']};margin:0 auto 24px;"></div>
    <p style="font-size:17px;color:rgba(214,232,214,.8);line-height:1.85;max-width:520px;margin:0 auto 56px;text-align:center;">
      اكتشف الجامعات، قارن التخصصات، واتخذ قرارك التعليمي بثقة مع مستشار ذكي يتحدث العربية
    </p>
    <div style="display:flex;justify-content:center;gap:0;border:1px solid rgba(214,232,214,.2);">
      <div style="padding:24px 40px;text-align:center;border-left:1px solid rgba(214,232,214,.2);">
        <div style="font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:{C['base']};line-height:1;">{N_UNIS}+</div>
        <div style="font-size:13px;color:rgba(214,232,214,.6);margin-top:6px;letter-spacing:.5px;">جامعة</div>
      </div>
      <div style="padding:24px 40px;text-align:center;border-left:1px solid rgba(214,232,214,.2);">
        <div style="font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:{C['base']};line-height:1;">{N_CTRY}</div>
        <div style="font-size:13px;color:rgba(214,232,214,.6);margin-top:6px;letter-spacing:.5px;">دولة خليجية</div>
      </div>
      <div style="padding:24px 40px;text-align:center;border-left:1px solid rgba(214,232,214,.2);">
        <div style="font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:{C['base']};line-height:1;">{N_PROGS}+</div>
        <div style="font-size:13px;color:rgba(214,232,214,.6);margin-top:6px;letter-spacing:.5px;">برنامج</div>
      </div>
      <div style="padding:24px 40px;text-align:center;">
        <div style="font-family:Syne,sans-serif;font-size:32px;font-weight:800;color:{C['base']};line-height:1;">{N_SCH}</div>
        <div style="font-size:13px;color:rgba(214,232,214,.6);margin-top:6px;letter-spacing:.5px;">منحة متاحة</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Services section (sage bg) ──
    st.markdown(f'<div style="background:{C["sage"]};padding:80px 80px 72px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["sec1"]};margin-bottom:12px;text-align:right;">خدماتنا</p>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{C["nav"]};margin-bottom:40px;text-align:right;line-height:1.3;">اختر ما يناسبك</h2>', unsafe_allow_html=True)

    services = [
        ("بحث الجامعات",         "ابحث في قاعدة بيانات الجامعات الخليجية وصفّ النتائج حسب الدولة والتخصص والمنح.",          "بحث الجامعات"),
        ("مقارنة الجامعات",       "قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — المنح، الترتيب، والروابط الرسمية.",              "المقارنة"),
        ("رُشد — المستشار الذكي", "تحدّث بالعربية مع مستشار AI يرشّح لك الجامعات ويشرح أسباب كل توصية.",                    "رُشد"),
        ("لوحة البيانات",         "مخططات تفاعلية وتقارير إحصائية شاملة عن التعليم العالي في دول الخليج.",                  "البيانات"),
        ("من نحن",                "تعرّف على منصة بوصلة ورؤيتها ورسالتها وفريق العمل.",                                      "من نحن"),
    ]
    cols = st.columns(3, gap="medium")
    for idx, (title, body, dest) in enumerate(services):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
<div style="background:{C['base']};padding:32px 28px;height:100%;direction:rtl;border-top:3px solid {C['nav']};">
  <h3 style="font-family:Syne,sans-serif;font-size:18px;font-weight:800;color:{C['nav']};margin-bottom:12px;text-align:right;">{title}</h3>
  <p style="font-size:14px;color:{C['sec1']};line-height:1.8;text-align:right;margin-bottom:24px;">{body}</p>
</div>
""", unsafe_allow_html=True)
            if st.button(f"انتقل ←", key=f"svc_{dest}", use_container_width=True):
                st.session_state.page = dest; st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Vision/Mission/Values (dark section) ──
    st.markdown(f'<div style="background:{C["sec1"]};padding:80px 80px 72px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;text-align:right;">هويتنا</p>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{C["base"]};margin-bottom:40px;text-align:right;">رؤيتنا ورسالتنا وقيمنا</h2>', unsafe_allow_html=True)

    v1, v2, v3 = st.columns(3, gap="medium")
    for col, title, body in [
        (v1, "رؤيتنا",  "إعادة تعريف تجربة اختيار التعليم في الخليج — منصة ذكية توجّه الشباب نحو مستقبلهم بثقة."),
        (v2, "رسالتنا", "تمكين الطلبة من اتخاذ قرارات تعليمية دقيقة باستخدام الذكاء الاصطناعي والبيانات الموثوقة."),
        (v3, "قيمنا",   "الوضوح · العدالة · التمكين · الابتكار · الموثوقية"),
    ]:
        col.markdown(f"""
<div style="background:rgba(255,254,250,.07);padding:28px 24px;border-top:2px solid {C['teal']};direction:rtl;">
  <div style="font-family:Syne,sans-serif;font-size:17px;font-weight:800;color:{C['base']};margin-bottom:12px;text-align:right;">{title}</div>
  <div style="font-size:14px;color:rgba(214,232,214,.8);line-height:1.8;text-align:right;">{body}</div>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# بحث الجامعات
# ══════════════════════════════════════════════
elif st.session_state.page == "بحث الجامعات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    # Page header
    st.markdown(f'<div style="background:{C["nav"]};padding:64px 80px 56px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;">الاستكشاف</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-family:Syne,sans-serif;font-size:40px;font-weight:800;color:{C["base"]};margin-bottom:0;">بحث الجامعات</h1>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Content
    st.markdown(f'<div style="padding:48px 80px 64px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    back_btn()

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
        st.markdown(f"""
<div style="text-align:center;padding:72px 0;color:#9AACAC;direction:rtl;">
  <div style="font-size:40px;margin-bottom:16px;">🔍</div>
  <div style="font-size:17px;font-weight:600;color:{C['sec1']};margin-bottom:8px;">ابحث للبدء</div>
  <div style="font-size:14px;">اكتب اسم جامعة أو دولة، أو استخدم الفلاتر أعلاه</div>
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

        st.markdown(f'<p style="font-size:14px;font-weight:600;color:{C["sec1"]};margin-bottom:20px;">{len(f)} نتيجة</p>', unsafe_allow_html=True)

        if f.empty:
            st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
        else:
            for _, row in f.head(30).iterrows():
                is_pub   = str(row["type"]).strip().lower() in ["public","حكومية"]
                type_lbl = "حكومية" if is_pub else "خاصة"
                type_bg  = f"background:rgba(54,75,73,.1);color:{C['sec1']};" if is_pub else f"background:rgba(48,43,38,.07);color:{C['ink']};"
                sch_tag  = f'<span style="padding:3px 12px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;margin-right:6px;">منحة دراسية</span>' if uni_has_sch(str(row["scholarship"])) else ""
                lang_tags = ""
                if not progs.empty:
                    for lg in progs[progs["uni_id"] == str(row["uni_id"])]["language"].dropna().unique()[:2]:
                        lang_tags += f'<span style="padding:3px 12px;font-size:11px;font-weight:600;background:rgba(16,42,39,.07);color:{C["nav"]};margin-right:6px;">{lg}</span>'
                links = ""
                if str(row.get("website","")).strip():        links += f'<a href="{row["website"]}" target="_blank" style="font-size:13px;font-weight:600;color:{C["teal"]};text-decoration:none;padding:6px 14px;border:1px solid rgba(46,196,182,.3);white-space:nowrap;">الموقع الرسمي</a>'
                if str(row.get("admissions_url","")).strip(): links += f'<a href="{row["admissions_url"]}" target="_blank" style="font-size:13px;font-weight:600;color:{C["teal"]};text-decoration:none;padding:6px 14px;border:1px solid rgba(46,196,182,.3);white-space:nowrap;margin-right:8px;">القبول</a>'
                st.markdown(f"""
<div style="background:#fff;border-bottom:1px solid rgba(54,75,73,.12);padding:20px 0;display:flex;justify-content:space-between;align-items:center;gap:16px;direction:rtl;">
  <div>
    <div style="font-size:15px;font-weight:700;color:{C['ink']};margin-bottom:4px;">{row["name_ar"]} <span style="font-weight:400;color:#9AACAC;font-size:13px;">— {row["name_en"]}</span></div>
    <div style="font-size:13px;color:#9AACAC;margin-bottom:10px;">{row["city"]}, {row["country"]}</div>
    <div><span style="padding:3px 12px;font-size:11px;font-weight:600;{type_bg}margin-left:6px;">{type_lbl}</span>{sch_tag}{lang_tags}</div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">{links}</div>
</div>""", unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# المقارنة
# ══════════════════════════════════════════════
elif st.session_state.page == "المقارنة":
    unis = unis_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown(f'<div style="background:{C["nav"]};padding:64px 80px 56px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;">التقييم المقارن</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-family:Syne,sans-serif;font-size:40px;font-weight:800;color:{C["base"]};margin-bottom:0;">مقارنة الجامعات</h1>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="padding:48px 80px 64px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    back_btn()

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + ", " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country","city","name_en"], na_position="last")

    selected = st.multiselect("اختر من ٢ إلى ٤ جامعات", options=unis["uni_id"].tolist(),
                              format_func=lambda x: label_map.get(str(x), str(x)), max_selections=4)
    if len(selected) < 2:
        st.info("يرجى اختيار جامعتين على الأقل.")
        st.markdown('</div></div>', unsafe_allow_html=True); st.stop()

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_c = st.columns(len(selected), gap="medium")
    for i, uid in enumerate(selected):
        row = comp[comp["uni_id"] == uid].iloc[0]
        with cols_c[i]:
            sch  = str(row.get("scholarship","")).strip() or "—"
            rank = (str(row.get("ranking_source","")).strip() + " " + str(row.get("ranking_value","")).strip()).strip() or "—"
            st.markdown(f"""
<div style="background:{C['sage']};padding:24px;border-top:3px solid {C['nav']};direction:rtl;">
  <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:{C['nav']};margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(54,75,73,.2);">{row['name_ar']}</div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(54,75,73,.1);"><span style="font-size:12px;color:{C['sec1']};">الموقع</span><span style="font-size:13px;font-weight:600;color:{C['ink']};">{row['city']}, {row['country']}</span></div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(54,75,73,.1);"><span style="font-size:12px;color:{C['sec1']};">النوع</span><span style="font-size:13px;font-weight:600;color:{C['ink']};">{row['type']}</span></div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(54,75,73,.1);"><span style="font-size:12px;color:{C['sec1']};">المنح</span><span style="font-size:13px;font-weight:600;color:{C['ink']};">{sch}</span></div>
  <div style="display:flex;justify-content:space-between;padding:8px 0;"><span style="font-size:12px;color:{C['sec1']};">الترتيب</span><span style="font-size:13px;font-weight:600;color:{C['ink']};">{rank}</span></div>
</div>""", unsafe_allow_html=True)
            st.write("")
            if str(row.get("website","")).strip():        st.link_button("الموقع الرسمي",      row["website"],        use_container_width=True)
            if str(row.get("admissions_url","")).strip(): st.link_button("القبول والتسجيل",    row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url","")).strip():   st.link_button("البرامج الأكاديمية", row["programs_url"],   use_container_width=True)

    progs = progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        st.markdown(f'<div style="height:1px;background:rgba(54,75,73,.12);margin:40px 0;"></div>', unsafe_allow_html=True)
        section_title_sm("البرامج المتاحة للجامعات المختارة")
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

    st.markdown(f'<div style="height:1px;background:rgba(54,75,73,.12);margin:40px 0;"></div>', unsafe_allow_html=True)
    section_title_sm("المقارنة الذكية")
    profile_txt = st.text_input("", placeholder="ملفك الأكاديمي (اختياري) — مثال: طالب هندسة، IELTS 6.5", key="comp_profile", label_visibility="collapsed")
    if st.button("اطلب مقارنة ذكية", use_container_width=True, key="btn_compare_ai"):
        unis_data = [comp[comp["uni_id"]==uid].iloc[0].to_dict() for uid in selected if uid in comp["uni_id"].values]
        with st.spinner("جاري تحليل الجامعات..."):
            ai_result = compare_unis_ai(unis_data, profile_txt)
        st.markdown(f'<div style="background:{C["sage"]};border-top:2px solid {C["teal"]};padding:24px 28px;margin-top:16px;line-height:2;color:{C["ink"]};direction:rtl;"><span style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{C["teal"]};display:block;margin-bottom:10px;">المقارنة الذكية</span>{ai_result}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# رُشد
# ══════════════════════════════════════════════
elif st.session_state.page == "رُشد":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    st.markdown(f'<div style="background:{C["nav"]};padding:64px 80px 56px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;">المستشار الأكاديمي الذكي</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-family:Syne,sans-serif;font-size:40px;font-weight:800;color:{C["base"]};margin-bottom:8px;">رُشد</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:16px;color:rgba(214,232,214,.7);">تحدّث بالعربية — رُشد يفهم ملفك ويرشّح الجامعات المناسبة</p>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="padding:48px 80px 64px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    back_btn()

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    section_title_sm("التحليل السريع")
    qm_c1, qm_c2, qm_c3 = st.columns(3)
    countries_list = sorted([x for x in unis["country"].unique() if str(x).strip()])
    qm_country = qm_c1.selectbox("الدولة المفضلة", ["الكل"] + countries_list, key="qm_country")
    qm_major   = qm_c2.text_input("التخصص المطلوب", placeholder="مثال: هندسة الحاسب", key="qm_major")
    qm_ielts   = qm_c3.text_input("درجة IELTS",     placeholder="مثال: 6.5",          key="qm_ielts")

    if st.button("حلّل بسرعة", use_container_width=True, key="btn_quick_match"):
        if not qm_major.strip():
            st.warning("يرجى إدخال التخصص المطلوب.")
        else:
            with st.spinner("جاري التحليل..."):
                qm_result = quick_match({"country":qm_country,"major":qm_major,"ielts":qm_ielts or "غير محدد"}, st.session_state.unis_context)
            top3 = qm_result.get("top_3",[])
            advice = qm_result.get("advice","")
            missing = qm_result.get("missing",[])
            if top3:
                qr_cols = st.columns(len(top3))
                for i, item in enumerate(top3[:3]):
                    uid = item.get("uni_id",""); name_ar = item.get("name_ar", uid)
                    reason = item.get("reason",""); fit = item.get("fit","مناسب")
                    uni_row = unis[unis["uni_id"]==uid]
                    city_country=""; sch_tag=""
                    if not uni_row.empty:
                        r = uni_row.iloc[0]; city_country = f"{r.get('city','')}, {r.get('country','')}"
                        if uni_has_sch(str(r.get("scholarship",""))): sch_tag = f'<span style="padding:3px 12px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;">منحة دراسية</span>'
                    with qr_cols[i]:
                        st.markdown(f"""
<div style="background:{C['sage']};border-top:3px solid {C['nav']};padding:20px;direction:rtl;">
  <div style="font-size:15px;font-weight:700;color:{C['nav']};margin-bottom:4px;">{name_ar}</div>
  <div style="font-size:13px;color:#9AACAC;margin-bottom:10px;">{city_country}</div>
  <div style="font-size:13px;color:{C['sec1']};line-height:1.7;margin-bottom:12px;">{reason}</div>
  <div>{sch_tag} <span style="padding:3px 12px;font-size:11px;font-weight:600;background:rgba(54,75,73,.1);color:{C['sec1']};">{fit}</span></div>
</div>""", unsafe_allow_html=True)
            if advice:
                st.markdown(f'<div style="background:{C["sage"]};border-top:2px solid {C["teal"]};padding:22px 26px;margin-top:14px;line-height:2;color:{C["ink"]};direction:rtl;"><span style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{C["teal"]};display:block;margin-bottom:8px;">نصيحة رُشد</span>{advice}</div>', unsafe_allow_html=True)
            if missing:
                missing_html = "".join([f'<span style="padding:3px 12px;font-size:11px;font-weight:600;background:#FFFBEB;color:#92400E;border:1px solid #FDE68A;margin:3px;">{m}</span>' for m in missing])
                st.markdown(f'<div style="margin-top:10px;direction:rtl;"><span style="color:#9AACAC;font-size:13px;margin-left:8px;">قد تحتاج إلى:</span>{missing_html}</div>', unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:rgba(54,75,73,.12);margin:40px 0;"></div>', unsafe_allow_html=True)

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{"role":"assistant","content":"مرحباً، أنا رُشد.\n\nأخبرني عن نفسك:\n- التخصص الذي تريده\n- الدولة المفضلة\n- معدلك التقريبي\n- هل عندك IELTS وكم درجتك؟\n\nوسأرشّح لك الجامعات المناسبة."}]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"], avatar="🧭" if msg["role"]=="assistant" else "🎓"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":user_input})
        with st.chat_message("user", avatar="🎓"): st.markdown(user_input)
        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner(""):
                history = [m for m in st.session_state.rushd_messages if not (m["role"]=="assistant" and "مرحباً" in m["content"])]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role":"assistant","content":reply})

    if len(st.session_state.rushd_messages) > 1:
        if st.button("محادثة جديدة"): st.session_state.rushd_messages=[]; st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# البيانات
# ══════════════════════════════════════════════
elif st.session_state.page == "البيانات":
    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("لا تتوفر بيانات."); st.stop()

    st.markdown(f'<div style="background:{C["nav"]};padding:64px 80px 56px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;">الإحصاء والتحليل</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-family:Syne,sans-serif;font-size:40px;font-weight:800;color:{C["base"]};margin-bottom:0;">لوحة البيانات</h1>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Stats band (sage)
    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    st.markdown(f'<div style="background:{C["sage"]};padding:0 80px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    stats_cols = st.columns(4)
    for col, (label, val) in zip(stats_cols, [("إجمالي الجامعات",N_UNIS),("إجمالي البرامج",N_PROGS),("تقدم منحاً",with_sch),("دولة خليجية",N_CTRY)]):
        col.markdown(f"""
<div style="padding:36px 0;text-align:center;border-left:1px solid rgba(54,75,73,.15);">
  <div style="font-family:Syne,sans-serif;font-size:36px;font-weight:800;color:{C['nav']};line-height:1;">{val}</div>
  <div style="font-size:13px;color:{C['sec1']};margin-top:8px;letter-spacing:.5px;">{label}</div>
</div>""", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Charts
    st.markdown(f'<div style="padding:48px 80px 64px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    back_btn()

    T    = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="IBM Plex Sans Arabic",color="#364b49"), margin=dict(l=10,r=10,t=38,b=10), height=290)
    T_sm = {**T, "height":260}

    ch1, ch2, ch3 = st.columns(3, gap="medium")
    with ch1:
        fig = px.bar(x=list(by_country.values()), y=list(by_country.keys()), orientation="h", title="الجامعات حسب الدولة", color_discrete_sequence=[C['nav']])
        fig.update_layout(**T); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        fig = px.pie(values=list(by_type.values()), names=list(by_type.keys()), title="حكومية / خاصة", hole=0.55, color_discrete_sequence=[C['teal'], C['nav'], C['sec1']])
        fig.update_layout(**T); fig.update_traces(textfont_color="white")
        st.plotly_chart(fig, use_container_width=True)
    with ch3:
        if top_fields:
            fig = px.bar(x=list(top_fields.keys()), y=list(top_fields.values()), title="أبرز التخصصات", color_discrete_sequence=[C['sec1']])
            fig.update_layout(**T, xaxis_tickangle=-30); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    ch4, ch5 = st.columns(2, gap="medium")
    with ch4:
        pct = round(with_sch/max(len(unis),1)*100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=pct,
            title={"text":"% نسبة الجامعات التي تقدم منحاً","font":{"family":"IBM Plex Sans Arabic","color":C['sec1'],"size":13}},
            number={"font":{"color":C['nav'],"family":"IBM Plex Sans Arabic"}},
            gauge={"axis":{"range":[0,100],"tickcolor":C['sage']},"bar":{"color":C['nav']},
                   "bgcolor":"rgba(0,0,0,0)","bordercolor":C['sage'],
                   "steps":[{"range":[0,100],"color":C['sage']}]}))
        fig.update_layout(**T_sm)
        st.plotly_chart(fig, use_container_width=True)
    with ch5:
        if by_lang:
            fig = px.bar(x=list(by_lang.keys()), y=list(by_lang.values()), title="لغات الدراسة", color_discrete_sequence=[C['sec1']])
            fig.update_layout(**T_sm); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown(f'<div style="height:1px;background:rgba(54,75,73,.12);margin:40px 0;"></div>', unsafe_allow_html=True)
    section_title_sm("توزيع المنح حسب الدولة")
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
            fig_sch = px.bar(sch_df, x="عدد", y="الدولة", color="نوع المنحة", orientation="h", barmode="stack",
                             title="عدد الجامعات التي تقدم منحاً لكل فئة حسب الدولة",
                             color_discrete_map={"Local":C['teal'],"GCC":C['nav'],"International":C['sec1']})
            fig_sch.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                                  font=dict(family="IBM Plex Sans Arabic",color=C['sec1']),
                                  margin=dict(l=10,r=10,t=38,b=10),height=320,
                                  legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color=C['sec1'])))
            fig_sch.update_traces(marker_line_width=0)
            st.plotly_chart(fig_sch, use_container_width=True)

    st.markdown(f'<div style="height:1px;background:rgba(54,75,73,.12);margin:40px 0;"></div>', unsafe_allow_html=True)
    col_r, col_g = st.columns(2, gap="medium")
    with col_r:
        section_title_sm("التقرير التحليلي الذكي")
        st.markdown(f'<p style="font-size:14px;color:{C["sec1"]};margin-bottom:16px;text-align:right;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير", use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                report = generate_dashboard_report({"total_unis":len(unis),"by_country":by_country,"by_type":by_type,"top_fields":top_fields,"by_language":by_lang,"with_scholarships":with_sch,"total_progs":len(progs)})
            st.markdown(f'<div style="background:{C["sage"]};border-top:2px solid {C["teal"]};padding:22px 26px;margin-top:14px;line-height:2;color:{C["ink"]};direction:rtl;"><span style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{C["teal"]};display:block;margin-bottom:8px;">التقرير التحليلي</span>{report}</div>', unsafe_allow_html=True)
    with col_g:
        section_title_sm("تحليل الفجوات التعليمية")
        st.markdown(f'<p style="font-size:14px;color:{C["sec1"]};margin-bottom:16px;text-align:right;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div style="background:#FFFBEB;border-top:2px solid #FDE68A;padding:22px 26px;margin-top:14px;line-height:2;color:{C["ink"]};direction:rtl;">{gaps}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# من نحن
# ══════════════════════════════════════════════
elif st.session_state.page == "من نحن":
    st.markdown(f'<div style="background:{C["nav"]};padding:64px 80px 56px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;">هويتنا</p>', unsafe_allow_html=True)
    st.markdown(f'<h1 style="font-family:Syne,sans-serif;font-size:40px;font-weight:800;color:{C["base"]};margin-bottom:0;">من نحن</h1>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # About text (sage bg)
    st.markdown(f'<div style="background:{C["sage"]};padding:72px 80px 64px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f"""
<p style="font-size:20px;font-weight:700;color:{C['nav']};margin-bottom:20px;text-align:right;line-height:1.5;">منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.</p>
<p style="font-size:17px;color:{C['sec1']};line-height:1.9;text-align:right;">جاءت فكرة بوصلة استجابةً لتحدٍ واقعي — تشتّت المعلومات وصعوبة المقارنة بين الجامعات وتعدد المصادر غير الموثوقة.</p>
<p style="font-size:17px;color:{C['sec1']};line-height:1.9;text-align:right;margin-top:16px;">نجمع البيانات التعليمية الخليجية ونقدّمها بطريقة مبسّطة، مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على اتخاذ قراره بثقة.</p>
""", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Values (dark bg)
    st.markdown(f'<div style="background:{C["sec1"]};padding:72px 80px 64px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;text-align:right;">قيمنا</p>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{C["base"]};margin-bottom:36px;text-align:right;">ما يحركنا</h2>', unsafe_allow_html=True)
    v1, v2, v3, v4 = st.columns(4, gap="medium")
    for col, title, body in [
        (v1,"الوضوح","تبسيط القرار التعليمي"),
        (v2,"العدالة","عرض الخيارات دون تحيّز"),
        (v3,"التمكين","فهم الذات قبل التخصص"),
        (v4,"الابتكار","AI في خدمة التعليم"),
    ]:
        col.markdown(f"""
<div style="background:rgba(255,254,250,.07);padding:24px 18px;border-top:2px solid {C['teal']};direction:rtl;">
  <div style="font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:{C['base']};margin-bottom:8px;text-align:right;">{title}</div>
  <div style="font-size:13px;color:rgba(214,232,214,.75);text-align:right;">{body}</div>
</div>""", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Contact
    st.markdown(f'<div style="padding:72px 80px 80px;direction:rtl;"><div style="{MAX}">', unsafe_allow_html=True)
    back_btn()
    st.markdown(f'<p style="font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:{C["teal"]};margin-bottom:12px;text-align:right;">تواصل</p>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{C["nav"]};margin-bottom:32px;text-align:right;">تواصل معنا</h2>', unsafe_allow_html=True)
    ca, cb = st.columns(2, gap="medium")
    with ca:
        st.text_input("الاسم",             placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني", placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=120)
    if st.button("إرسال", use_container_width=True):
        st.success("تم الاستلام. شكراً لتواصلك.")
    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
    st.markdown('</div></div>', unsafe_allow_html=True)
