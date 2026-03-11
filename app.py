import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from ai_engine import build_unis_context, chat_rushd, generate_dashboard_report, analyze_gaps

st.set_page_config(page_title="Bawsala | بوصلة", layout="wide", initial_sidebar_state="collapsed")

# ── CSS injected in small chunks to avoid Streamlit rendering bug ──
def inject_css():
    # Chunk 1: variables + base
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
:root{
  --bg:#0A0B0F;
  --surface:#111318;
  --card:rgba(255,255,255,0.04);
  --card-h:rgba(255,255,255,0.07);
  --indigo:#5B5FEE;
  --indigo-soft:rgba(91,95,238,0.18);
  --gold:#D4A853;
  --gold-soft:rgba(212,168,83,0.14);
  --text-1:#EAEDF2;
  --text-2:#8A94A6;
  --text-3:#3D4454;
  --border:rgba(255,255,255,0.06);
  --border-a:rgba(91,95,238,0.35);
}
html,body,[class*="css"]{font-family:'Cairo',sans-serif!important;background:var(--bg)!important;color:var(--text-1)!important;}
[data-testid="stSidebar"],[data-testid="stSidebarNav"],button[kind="header"],section[data-testid="stSidebar"]{display:none!important;}
[data-testid="stAppViewContainer"]{background:var(--bg)!important;}
[data-testid="stMain"]{background:transparent!important;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{direction:rtl!important;text-align:right!important;}
input,textarea,[role="textbox"]{direction:rtl!important;text-align:right!important;}
div[data-baseweb="select"] *{direction:rtl!important;text-align:right!important;}
label{direction:rtl!important;text-align:right!important;color:var(--text-2)!important;}
</style>""", unsafe_allow_html=True)

    # Chunk 2: header + nav
    st.markdown("""<style>
.baw-header{text-align:center;padding:64px 20px 40px;position:relative;}
.baw-header::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:600px;height:300px;background:radial-gradient(ellipse,rgba(91,95,238,0.1) 0%,transparent 70%);pointer-events:none;}
.baw-title{font-size:4.5rem;font-weight:900;letter-spacing:-3px;color:var(--text-1);line-height:1;margin-bottom:14px;}
.baw-title em{color:var(--indigo);font-style:normal;}
.baw-rule{width:48px;height:2px;background:linear-gradient(90deg,var(--indigo),var(--gold));margin:16px auto;border-radius:2px;}
.baw-sub{font-size:1rem;color:var(--text-2);font-weight:400;letter-spacing:0.2px;}
.stat-row{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:28px auto 0;max-width:600px;}
.stat-item{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:10px 20px;text-align:center;}
.stat-item strong{display:block;font-size:1.25rem;font-weight:900;color:var(--indigo);}
.stat-item small{font-size:0.8rem;color:var(--text-2);}
</style>""", unsafe_allow_html=True)

    # Chunk 3: buttons + cards
    st.markdown("""<style>
.stButton>button{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--text-2)!important;border-radius:8px!important;font-weight:600!important;font-family:'Cairo',sans-serif!important;font-size:0.875rem!important;padding:9px 18px!important;transition:all 0.2s!important;}
.stButton>button:hover{background:var(--indigo-soft)!important;border-color:var(--indigo)!important;color:var(--text-1)!important;}
.uni-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:22px 26px;margin-bottom:12px;transition:all 0.25s;border-left:2px solid transparent;}
.uni-card:hover{background:var(--card-h);border-left-color:var(--indigo);}
.uni-card-title{font-size:1rem;font-weight:800;color:var(--text-1);margin:0 0 6px;}
.uni-card-meta{color:var(--text-2);font-size:0.85rem;margin-bottom:10px;}
.uni-card-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;}
.tag{padding:3px 10px;border-radius:5px;font-size:0.77rem;font-weight:700;letter-spacing:0.2px;}
.tag-gov{background:rgba(91,95,238,0.12);color:#9EA2FF;border:1px solid rgba(91,95,238,0.2);}
.tag-priv{background:rgba(139,92,246,0.1);color:#C4B5FD;border:1px solid rgba(139,92,246,0.2);}
.tag-sch{background:var(--gold-soft);color:#E5C07B;border:1px solid rgba(212,168,83,0.25);}
.tag-lang{background:rgba(6,182,212,0.1);color:#67E8F9;border:1px solid rgba(6,182,212,0.2);}
.card-link{color:var(--indigo);font-size:0.82rem;text-decoration:none;font-weight:600;margin-left:14px;}
.card-link:hover{color:var(--gold);}
</style>""", unsafe_allow_html=True)

    # Chunk 4: home + sections + misc
    st.markdown("""<style>
.home-feature{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:28px 24px;height:100%;transition:all 0.25s;}
.home-feature:hover{background:var(--card-h);border-color:var(--border-a);}
.home-feature-label{font-size:0.72rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--indigo);margin-bottom:10px;}
.home-feature-title{font-size:1.1rem;font-weight:900;color:var(--text-1);margin-bottom:10px;}
.home-feature-text{font-size:0.88rem;color:var(--text-2);line-height:1.9;}
.section-label{font-size:0.72rem;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:var(--indigo);text-align:center;margin-bottom:8px;}
.section-title{font-size:1.7rem;font-weight:900;color:var(--text-1);text-align:center;margin-bottom:28px;letter-spacing:-0.5px;}
.divider{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:36px 0;border:none;}
.chip{display:inline-block;background:var(--indigo-soft);border:1px solid rgba(91,95,238,0.25);color:#9EA2FF;border-radius:6px;padding:3px 12px;font-size:0.8rem;font-weight:700;margin-bottom:20px;}
.ai-result{background:var(--surface);border:1px solid var(--border-a);border-radius:14px;padding:26px 28px;line-height:2;color:var(--text-1);margin-top:14px;}
.ai-result-label{font-size:0.7rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--indigo);margin-bottom:14px;display:block;}
.gap-result{background:var(--surface);border:1px solid rgba(212,168,83,0.2);border-radius:14px;padding:26px 28px;line-height:2.1;color:var(--text-1);margin-top:14px;}
.comp-card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:22px;}
.comp-head{font-size:0.95rem;font-weight:900;color:var(--text-1);margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--border);}
.comp-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);}
.comp-label{color:var(--text-3);font-size:0.82rem;font-weight:600;}
.comp-val{color:var(--text-1);font-size:0.85rem;font-weight:700;}
div[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;overflow:hidden!important;margin-bottom:10px!important;}
div[data-testid="stExpander"] details>summary p{font-weight:800!important;color:var(--text-1)!important;font-size:0.95rem!important;}
div[data-testid="stExpander"] details>div{color:var(--text-2)!important;line-height:2!important;}
div[data-baseweb="select"]>div{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:9px!important;color:var(--text-1)!important;}
.stTextInput>div>div{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:9px!important;}
input{color:var(--text-1)!important;}
[data-testid="stChatMessage"]{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:12px!important;direction:rtl!important;margin-bottom:10px!important;}
.stLinkButton a{background:var(--indigo-soft)!important;border:1px solid rgba(91,95,238,0.25)!important;color:#9EA2FF!important;border-radius:8px!important;font-weight:700!important;font-size:0.83rem!important;}
.stLinkButton a:hover{background:var(--indigo)!important;color:white!important;}
::-webkit-scrollbar{width:3px;}::-webkit-scrollbar-thumb{background:var(--border-a);border-radius:3px;}
</style>""", unsafe_allow_html=True)

inject_css()

# ─── Data ───
ROOT       = Path(__file__).resolve().parent
UNIS_PATH  = ROOT / "universities.csv"
PROGS_PATH = ROOT / "programs.csv"

@st.cache_data(show_spinner=False)
def load_unis_csv(path):
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    kw = dict(encoding="utf-8", engine="python", on_bad_lines="skip")
    try:
        first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].lower()
        return pd.read_csv(path, **kw) if "uni_id" in first else pd.read_csv(path, header=None, **kw)
    except:
        return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_csv(path):
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="skip")
    except:
        return pd.DataFrame()

def normalize_unis(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    cols = ["uni_id","name_ar","name_en","country","city","type",
            "website","admissions_url","programs_url","ranking_source","extra_1","extra_2",
            "scholarship","sch_notes","sch_url"]
    if list(df.columns) == list(range(len(df.columns))):
        df.columns = cols[:len(df.columns)]
    if "uni_id" in df.columns and str(df.iloc[0].get("uni_id","")).lower().strip() == "uni_id":
        df = df.iloc[1:].copy()
    for c in ["ranking_value","accreditation_notes","scholarship","sch_notes","sch_url",
              "website","admissions_url","programs_url","ranking_source"]:
        if c not in df.columns: df[c] = ""
    df["scholarship"] = df["scholarship"].fillna("").astype(str).str.strip().replace({"nan":""})
    needed = ["uni_id","name_ar","name_en","country","city","type",
              "scholarship","sch_notes","sch_url","website","admissions_url","programs_url",
              "ranking_source","ranking_value","accreditation_notes"]
    for c in needed:
        if c not in df.columns: df[c] = ""
    return df[needed].dropna(subset=["uni_id"])

def normalize_progs(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    needed = ["program_id","uni_id","level","degree_type","major_field",
              "program_name_en","program_name_ar","city","language",
              "duration_years","tuition_notes","admissions_requirements","url"]
    for c in needed:
        if c not in df.columns: df[c] = ""
    return df[needed]

def uni_has_sch(s):
    return str(s).strip() not in ["","No","Unknown","nan","none","None"]

unis_raw  = normalize_unis(load_unis_csv(UNIS_PATH))
progs_raw = normalize_progs(load_csv(PROGS_PATH))
N_UNIS    = len(unis_raw)
N_PROGS   = len(progs_raw)
N_CTRY    = unis_raw["country"].nunique() if not unis_raw.empty else 0

# ─── Header ───
st.markdown(f"""
<div class="baw-header">
  <div class="baw-title">بو<em>صلة</em></div>
  <div class="baw-rule"></div>
  <div class="baw-sub">الدليل الذكي للتعليم العالي في دول مجلس التعاون الخليجي</div>
  <div class="stat-row">
    <div class="stat-item"><strong>{N_UNIS}+</strong><small>جامعة</small></div>
    <div class="stat-item"><strong>{N_CTRY}</strong><small>دولة</small></div>
    <div class="stat-item"><strong>{N_PROGS}+</strong><small>برنامج</small></div>
    <div class="stat-item"><strong>GPT-4</strong><small>مدعوم بالذكاء الاصطناعي</small></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Navigation ───
if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

PAGES = ["من نحن", "تحليل البيانات", "رُشد", "المقارنة", "بحث الجامعات", "الرئيسية"]
nav = st.columns(len(PAGES))
for i, name in enumerate(PAGES):
    c = nav[-(i+1)]
    if c.button(name, use_container_width=True, key=f"n_{name}"):
        st.session_state.page = name; st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ══ الرئيسية ══════════════════════════════════
if st.session_state.page == "الرئيسية":
    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown('<div class="section-label">ماذا يقدم بوصلة</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">منصة واحدة — كل خياراتك الأكاديمية</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""<div class="home-feature">
<div class="home-feature-label">المستشار الذكي</div>
<div class="home-feature-title">رُشد</div>
<div class="home-feature-text">تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح لك أفضل الجامعات من قاعدة بياناتنا مع شرح أسباب كل توصية.</div>
</div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="home-feature">
<div class="home-feature-label">الإحصاء والتحليل</div>
<div class="home-feature-title">لوحة البيانات</div>
<div class="home-feature-text">مخططات تفاعلية وتقارير ذكية تحوّل بيانات التعليم الخليجي إلى رؤى إحصائية واضحة وقابلة للمقارنة.</div>
</div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class="home-feature">
<div class="home-feature-label">القرار المدروس</div>
<div class="home-feature-title">المقارنة</div>
<div class="home-feature-text">قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — النوع، المنح، الترتيب، والروابط الرسمية في مكان واحد.</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        with st.expander("رؤيتنا", expanded=True):
            st.markdown("نسعى في بوصلة إلى إعادة تعريف تجربة اختيار التعليم في الخليج، عبر منصة ذكية توجّه الشباب نحو تخصصاتهم وجامعاتهم المناسبة، وتحوّل القرار التعليمي من حيرة فردية إلى مسار واضح مدروس.")
        with st.expander("رسالتنا"):
            st.markdown("تلتزم بوصلة بتمكين الطلبة وأولياء الأمور من اتخاذ قرارات تعليمية دقيقة من خلال منصة ذكية تعتمد على الذكاء الاصطناعي والبيانات الموثوقة، لتقديم توجيه واضح ومخصص يربط بين قدرات الطالب وخيارات التعليم.")
        with st.expander("قيمنا"):
            st.markdown("الوضوح — العدالة — التمكين — الابتكار — الموثوقية")

        st.write("")
        b1, b2, b3 = st.columns(3)
        if b1.button("المستشار رُشد",   use_container_width=True): st.session_state.page="رُشد";              st.rerun()
        if b2.button("تحليل البيانات",  use_container_width=True): st.session_state.page="تحليل البيانات";   st.rerun()
        if b3.button("بحث الجامعات",    use_container_width=True): st.session_state.page="بحث الجامعات";     st.rerun()


# ══ بحث الجامعات ══════════════════════════════
elif st.session_state.page == "بحث الجامعات":
    st.markdown('<div class="section-label">الاستكشاف</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">بحث الجامعات</div>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    c4,c3,c2,c1 = st.columns([1.2,1,1,1.2])
    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c4.selectbox("الدولة",   ["الكل"]+countries)
    types_    = sorted([x for x in unis["type"].unique()    if str(x).strip()])
    uni_type  = c3.selectbox("النوع",    ["الكل"]+types_)
    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c2.selectbox("المرحلة", ["الكل"]+levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c1.selectbox("التخصص",  ["الكل"]+majors_)

    rs,ls = st.columns([3,1.2])
    q  = rs.text_input("", placeholder="ابحث عن جامعة أو مدينة...").strip().lower()
    yn = ls.selectbox("المنح", ["الكل","متاحة","غير متاحة"])

    f = unis.copy()
    if country  != "الكل": f = f[f["country"]==country]
    if uni_type != "الكل": f = f[f["type"]==uni_type]
    if yn=="متاحة":         f = f[f["scholarship"].apply(uni_has_sch)]
    if yn=="غير متاحة":     f = f[~f["scholarship"].apply(uni_has_sch)]
    if q:
        m = (f["name_en"].str.lower().str.contains(q,na=False)|
             f["name_ar"].str.lower().str.contains(q,na=False)|
             f["city"].str.lower().str.contains(q,na=False))
        f = f[m]
    if (major!="الكل" or level!="الكل") and not progs.empty:
        pm=progs.copy()
        if major!="الكل": pm=pm[pm["major_field"]==major]
        if level!="الكل": pm=pm[pm["level"]==level]
        f=f[f["uni_id"].isin(pm["uni_id"].unique())]

    st.markdown(f'<span class="chip">{len(f)} نتيجة</span>', unsafe_allow_html=True)

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
            if str(row.get("website","")).strip(): links+=f'<a href="{row["website"]}" target="_blank" class="card-link">الموقع الرسمي</a>'
            if str(row.get("admissions_url","")).strip(): links+=f'<a href="{row["admissions_url"]}" target="_blank" class="card-link">القبول والتسجيل</a>'

            st.markdown(f"""<div class="uni-card">
<div class="uni-card-title">{row["name_ar"]}&ensp;—&ensp;<span style="font-weight:400;color:var(--text-2);font-size:.92rem;">{row["name_en"]}</span></div>
<div class="uni-card-meta">{row["city"]}, {row["country"]}</div>
<div class="uni-card-tags">{type_tag}{sch_tag}{lang_tags}</div>
<div style="margin-top:12px;">{links}</div>
</div>""", unsafe_allow_html=True)


# ══ المقارنة ══════════════════════════════════
elif st.session_state.page == "المقارنة":
    st.markdown('<div class="section-label">التقييم المقارن</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">مقارنة الجامعات</div>', unsafe_allow_html=True)

    unis = unis_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("")&unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"]+" — "+unis["name_en"]+" ("+unis["city"]+", "+unis["country"]+")"
    label_map = dict(zip(unis["uni_id"],unis["label"]))
    unis = unis.sort_values(["country","city","name_en"],na_position="last")

    selected = st.multiselect("اختر من ٢ إلى ٤ جامعات",
        options=unis["uni_id"].tolist(),
        format_func=lambda x: label_map.get(str(x),str(x)),
        max_selections=4)

    if len(selected)<2: st.info("يرجى اختيار جامعتين على الأقل."); st.stop()

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_c = st.columns(len(selected))
    for i,uid in enumerate(selected):
        row = comp[comp["uni_id"]==uid].iloc[0]
        with cols_c[i]:
            sch  = str(row.get("scholarship","")).strip() or "—"
            rank = (str(row.get("ranking_source","")).strip()+" "+str(row.get("ranking_value","")).strip()).strip() or "—"
            st.markdown(f"""<div class="comp-card">
<div class="comp-head">{row['name_ar']}</div>
<div class="comp-row"><span class="comp-label">الموقع</span><span class="comp-val">{row['city']}, {row['country']}</span></div>
<div class="comp-row"><span class="comp-label">النوع</span><span class="comp-val">{row['type']}</span></div>
<div class="comp-row"><span class="comp-label">المنح</span><span class="comp-val">{sch}</span></div>
<div class="comp-row"><span class="comp-label">الترتيب</span><span class="comp-val">{rank}</span></div>
</div>""", unsafe_allow_html=True)
            st.write("")
            if str(row.get("website","")).strip():        st.link_button("الموقع الرسمي",       row["website"],        use_container_width=True)
            if str(row.get("admissions_url","")).strip(): st.link_button("القبول والتسجيل",     row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url","")).strip():   st.link_button("البرامج الأكاديمية",  row["programs_url"],   use_container_width=True)


# ══ رُشد ══════════════════════════════════════
elif st.session_state.page == "رُشد":
    st.markdown('<div class="section-label">المستشار الأكاديمي الذكي</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">رُشد</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:var(--text-2);font-size:.9rem;margin-bottom:28px;">تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح لك الجامعات المناسبة من قاعدة البيانات</p>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("ملف universities.csv غير موجود."); st.stop()

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{"role":"assistant","content":
            "مرحباً، أنا رُشد.\n\nأخبرني عن نفسك:\n- التخصص الذي تريده\n- الدولة المفضلة\n- معدلك التقريبي\n- هل عندك IELTS وكم درجتك؟\n\nوسأرشّح لك الجامعات المناسبة."}]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"], avatar="R" if msg["role"]=="assistant" else "U"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":user_input})
        with st.chat_message("user", avatar="U"): st.markdown(user_input)
        with st.chat_message("assistant", avatar="R"):
            with st.spinner(""):
                history=[m for m in st.session_state.rushd_messages
                         if not(m["role"]=="assistant" and "مرحباً" in m["content"])]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role":"assistant","content":reply})

    if len(st.session_state.rushd_messages)>1:
        if st.button("محادثة جديدة"):
            st.session_state.rushd_messages=[]; st.rerun()


# ══ تحليل البيانات ════════════════════════════
elif st.session_state.page == "تحليل البيانات":
    st.markdown('<div class="section-label">الإحصاء والتحليل</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">لوحة البيانات</div>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty: st.error("لا تتوفر بيانات."); st.stop()

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    T = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
             font=dict(family="Cairo",color="#8A94A6"),
             margin=dict(l=10,r=10,t=38,b=10),height=290)

    ch1,ch2,ch3 = st.columns(3)
    with ch1:
        fig=px.bar(x=list(by_country.values()),y=list(by_country.keys()),
                   orientation="h",title="الجامعات حسب الدولة",
                   color_discrete_sequence=["#5B5FEE"])
        fig.update_layout(**T); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig,use_container_width=True)
    with ch2:
        fig=px.pie(values=list(by_type.values()),names=list(by_type.keys()),
                   title="حكومية / خاصة",hole=0.55,
                   color_discrete_sequence=["#5B5FEE","#D4A853","#06B6D4"])
        fig.update_layout(**T); fig.update_traces(textfont_color="white")
        st.plotly_chart(fig,use_container_width=True)
    with ch3:
        if top_fields:
            fig=px.bar(x=list(top_fields.keys()),y=list(top_fields.values()),
                       title="أبرز التخصصات",color_discrete_sequence=["#D4A853"])
            fig.update_layout(**T,xaxis_tickangle=-30); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig,use_container_width=True)

    ch4,ch5 = st.columns(2)
    with ch4:
        pct=round(with_sch/max(len(unis),1)*100,1)
        fig=go.Figure(go.Indicator(
            mode="gauge+number",value=pct,
            title={"text":"نسبة الجامعات التي تقدم منحاً %","font":{"family":"Cairo","color":"#8A94A6","size":13}},
            number={"font":{"color":"#D4A853","family":"Cairo"}},
            gauge={"axis":{"range":[0,100],"tickcolor":"#3D4454"},
                   "bar":{"color":"#D4A853"},
                   "bgcolor":"rgba(0,0,0,0)",
                   "bordercolor":"rgba(255,255,255,0.04)",
                   "steps":[{"range":[0,100],"color":"rgba(91,95,238,0.07)"}]}))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(family="Cairo",color="#8A94A6"),height=260,margin=dict(l=20,r=20,t=38,b=10))
        st.plotly_chart(fig,use_container_width=True)
    with ch5:
        if by_lang:
            fig=px.bar(x=list(by_lang.keys()),y=list(by_lang.values()),
                       title="لغات الدراسة",color_discrete_sequence=["#06B6D4"])
            fig.update_layout(**T,height=260); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig,use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_r,col_g = st.columns(2)
    with col_r:
        st.markdown("**التقرير التحليلي الذكي**")
        st.caption("الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً")
        if st.button("اطلب التقرير", use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                report = generate_dashboard_report({"total_unis":len(unis),"by_country":by_country,
                    "by_type":by_type,"top_fields":top_fields,"by_language":by_lang,
                    "with_scholarships":with_sch,"total_progs":len(progs)})
            st.markdown(f'<div class="ai-result"><span class="ai-result-label">التقرير التحليلي</span>{report}</div>',unsafe_allow_html=True)
    with col_g:
        st.markdown("**تحليل الفجوات التعليمية**")
        st.caption("رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي")
        if st.button("اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div class="gap-result">{gaps}</div>',unsafe_allow_html=True)


# ══ من نحن ════════════════════════════════════
elif st.session_state.page == "من نحن":
    st.markdown('<div class="section-label">هويتنا</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">من نحن</div>', unsafe_allow_html=True)

    _,col,_ = st.columns([1,2.6,1])
    with col:
        st.markdown("""<div style="direction:rtl;text-align:center;color:var(--text-2);line-height:2.1;font-size:.95rem;">
<p style="color:var(--text-1);font-size:1.05rem;font-weight:700;margin-bottom:18px;">
منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.</p>
<p>جاءت فكرة بوصلة استجابةً لتحدٍ واقعي يواجه الكثير من الطلبة — تشتّت المعلومات وصعوبة المقارنة بين الجامعات والبرامج وتعدد المصادر غير الموثوقة.</p>
<p>نعمل على جمع البيانات التعليمية الخليجية وتنظيمها وتقديمها بطريقة مبسطة، مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على فهم خياراته واتخاذ قراره بثقة.</p>
</div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        v1,v2,v3,v4 = st.columns(4)
        for c,title,desc in [(v1,"الوضوح","تبسيط القرار التعليمي"),
                              (v2,"العدالة","عرض الخيارات دون تحيّز"),
                              (v3,"التمكين","فهم الذات قبل التخصص"),
                              (v4,"الابتكار","AI في خدمة التعليم")]:
            c.markdown(f"""<div style="text-align:center;padding:18px 10px;background:var(--card);border:1px solid var(--border);border-radius:12px;">
<div style="font-size:.75rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--indigo);margin-bottom:6px;">{title}</div>
<div style="font-size:.82rem;color:var(--text-2);">{desc}</div></div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;font-size:1.2rem;color:var(--text-1);'>تواصل معنا</h3>", unsafe_allow_html=True)
        ca,cb = st.columns(2)
        with ca:
            st.text_input("الاسم",             placeholder="اكتب اسمك")
            st.text_input("البريد الإلكتروني", placeholder="example@email.com")
        with cb:
            st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=118)
        if st.button("إرسال", use_container_width=True):
            st.success("تم الاستلام. شكراً لتواصلك.")
        st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
