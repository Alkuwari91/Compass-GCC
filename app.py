import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from src.core.ai_engine import (
    build_unis_context,
    chat_rushd,
    generate_dashboard_report,
    explain_matches,
    analyze_gaps,
)

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(page_title="بوصلة", layout="wide", initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#F5F7FA; --card:#FFFFFF; --text:#334155;
  --navy:#0F1B33; --navy2:#12264A;
  --teal:#1A6B72; --teal-light:#E8F4F5;
  --gold:#C8922A; --gold-light:#FEF3CD;
  --border:#E5E7EB; --muted:#64748B;
}
html,body,[class*="css"]{
  font-family:'Cairo',sans-serif !important;
  background:var(--bg); color:var(--text);
}
[data-testid="stSidebar"],[data-testid="stSidebarNav"],
button[kind="header"],section[data-testid="stSidebar"]{display:none !important;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  direction:rtl !important; text-align:right !important;
}
input,textarea,[role="textbox"]{direction:rtl !important;text-align:right !important;}
div[data-baseweb="select"] *{direction:rtl !important;text-align:right !important;}
label{direction:rtl !important;text-align:right !important;}

.baw-header{
  background:linear-gradient(135deg,var(--navy2),var(--navy));
  padding:50px 20px 40px;text-align:center;
  border-radius:0 0 28px 28px;margin-bottom:8px;
}
.baw-header h1{font-size:3rem;font-weight:900;margin:0;color:#fff;}
.baw-header p{margin-top:8px;font-size:1.1rem;color:rgba(255,255,255,.85);}

.stat-row{display:flex;justify-content:center;gap:20px;margin:18px 0;flex-wrap:wrap;}
.stat-chip{
  background:var(--teal-light);border:1px solid var(--teal);
  border-radius:12px;padding:10px 22px;text-align:center;
}
.stat-chip b{display:block;font-size:1.5rem;color:var(--teal);font-weight:900;}
.stat-chip span{font-size:.85rem;color:var(--muted);}

.stButton>button{
  border-radius:12px !important;font-weight:700 !important;
  font-family:'Cairo',sans-serif !important;
}

.uni-card{
  background:var(--card);border:1px solid var(--border);
  border-radius:16px;padding:20px 22px;margin-bottom:14px;
  box-shadow:0 4px 16px rgba(15,27,51,.06);
  border-right:4px solid var(--teal);
}
.uni-card h3{margin:0 0 6px;font-size:1.1rem;color:var(--navy);font-weight:800;}
.uni-card .meta{color:var(--muted);font-size:.9rem;margin-bottom:10px;}
.uni-card .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.tag{padding:3px 10px;border-radius:20px;font-size:.8rem;font-weight:600;}
.tag-gov{background:#DBEAFE;color:#1D4ED8;}
.tag-priv{background:#F3E8FF;color:#7C3AED;}
.tag-sch{background:var(--gold-light);color:var(--gold);}
.tag-lang{background:#D1FAE5;color:#065F46;}

.ai-report{
  background:linear-gradient(135deg,var(--navy),var(--navy2));
  color:#fff;border-radius:18px;padding:24px 28px;
  margin-top:16px;line-height:2;
}
.ai-report h4{color:var(--gold);margin:0 0 12px;font-size:1.1rem;}

.gap-box{
  background:var(--teal-light);border:1px solid var(--teal);
  border-radius:14px;padding:20px 24px;line-height:2;
}

.page-title{text-align:center;font-weight:900;font-size:1.8rem;margin:10px 0 20px;color:var(--navy);}

div[data-testid="stExpander"]{
  border:1px solid var(--border) !important;border-radius:16px !important;
  background:#fff !important;box-shadow:0 4px 16px rgba(15,27,51,.06) !important;
  overflow:hidden !important;margin-bottom:14px !important;
}
div[data-testid="stExpander"] details>summary p{
  font-size:1.1rem !important;font-weight:800 !important;color:var(--teal) !important;
}
div[data-testid="stExpander"] details>summary:hover{background:var(--teal-light) !important;}
[data-testid="stChatMessage"]{direction:rtl !important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Data helpers
# ─────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent
DATA_DIR   = ROOT / "data"
UNIS_PATH  = DATA_DIR / "universities.csv"
PROGS_PATH = DATA_DIR / "programs.csv"


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


# ─────────────────────────────────────────────
# Load data once
# ─────────────────────────────────────────────
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
  <h1>🧭 بوصلة</h1>
  <p>من الحيرة إلى القرار — دليلك الذكي للتعليم العالي الخليجي</p>
</div>
<div class="stat-row">
  <div class="stat-chip"><b>{n_unis}+</b><span>جامعة</span></div>
  <div class="stat-chip"><b>{n_countries}</b><span>دول خليجية</span></div>
  <div class="stat-chip"><b>{n_progs}+</b><span>برنامج أكاديمي</span></div>
  <div class="stat-chip"><b>AI</b><span>مدعوم بالذكاء الاصطناعي</span></div>
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
    label = f"● {name}" if st.session_state.page == name else name
    if col.button(label, use_container_width=True, key=f"nav_{name}"):
        st.session_state.page = name
        st.rerun()

st.markdown("---")

# ═══════════════════════════════════════════════
# PAGE: الرئيسية
# ═══════════════════════════════════════════════
if st.session_state.page == "الرئيسية":
    _, center, _ = st.columns([1, 2.4, 1])
    with center:
        with st.expander("رؤيتنا", expanded=True):
            st.markdown("نسعى في بوصلة إلى إعادة تعريف تجربة اختيار التعليم في الخليج، عبر منصة ذكية توجّه الشباب نحو تخصصاتهم وجامعاتهم المناسبة، وتحوّل القرار التعليمي من حيرة فردية إلى مسار واضح مدروس.")
        with st.expander("رسالتنا"):
            st.markdown("تلتزم بوصلة بتمكين الطلبة وأولياء الأمور من اتخاذ قرارات تعليمية دقيقة من خلال منصة ذكية تعتمد على الذكاء الاصطناعي والبيانات الموثوقة، لتقديم توجيه واضح ومخصص يربط بين قدرات الطالب، خيارات التعليم، ومتطلبات سوق العمل.")
        with st.expander("قيمنا"):
            st.markdown("""
- **الوضوح:** تبسيط القرار التعليمي بلغة سهلة
- **العدالة:** عرض الخيارات دون تحيّز
- **التمكين:** فهم الذات قبل اختيار التخصص
- **الابتكار:** توظيف الذكاء الاصطناعي لخدمة التعليم
- **الموثوقية:** بيانات دقيقة ومحدّثة
""")
        with st.expander("لماذا بوصلة؟"):
            st.markdown("لأن قرار اختيار الجامعة والتخصص لم يعد بسيطاً، بل قرار مصيري يواجه فيه الطلبة تعدد الخيارات وغياب التوجيه وضغط التوقعات.")
        st.markdown("---")
        b1, b2, b3 = st.columns(3)
        if b1.button("🔍 ابدأ البحث", use_container_width=True):
            st.session_state.page = "بحث الجامعات"; st.rerun()
        if b2.button("📊 تحليل البيانات", use_container_width=True):
            st.session_state.page = "تحليل البيانات"; st.rerun()
        if b3.button("💬 تحدث مع رُشد", use_container_width=True):
            st.session_state.page = "رُشد"; st.rerun()


# ═══════════════════════════════════════════════
# PAGE: بحث الجامعات
# ═══════════════════════════════════════════════
elif st.session_state.page == "بحث الجامعات":
    st.markdown('<h1 class="page-title">🔍 بحث الجامعات</h1>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    if unis.empty:
        st.error("ملف universities.csv غير موجود أو فارغ."); st.stop()

    c4, c3, c2, c1 = st.columns([1.2, 1, 1, 1.2])
    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c4.selectbox("🌍 الدولة",       ["الكل"] + countries)
    types_    = sorted([x for x in unis["type"].unique() if str(x).strip()])
    uni_type  = c3.selectbox("🏛️ نوع الجامعة", ["الكل"] + types_)
    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c2.selectbox("🎓 المرحلة",      ["الكل"] + levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c1.selectbox("📚 التخصص",       ["الكل"] + majors_)

    rs, ls = st.columns([3, 1.2])
    q  = rs.text_input("🔎 بحث نصي", value="").strip().lower()
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

    st.markdown(f"**{len(f)} نتيجة**")
    st.markdown("---")

    if f.empty:
        st.info("لا توجد نتائج. جرّب تعديل الفلاتر.")
    else:
        for _, row in f.head(30).iterrows():
            is_public = str(row["type"]).strip().lower() in ["public", "حكومية"]
            type_tag  = '<span class="tag tag-gov">حكومية</span>' if is_public else '<span class="tag tag-priv">خاصة</span>'
            sch_tag   = '<span class="tag tag-sch">💰 منحة</span>' if uni_has_sch(str(row["scholarship"])) else ""
            lang_tags = ""
            if not progs.empty and "uni_id" in progs.columns:
                for lg in progs[progs["uni_id"] == str(row["uni_id"])]["language"].dropna().unique()[:3]:
                    lang_tags += f'<span class="tag tag-lang">📖 {lg}</span>'
            links = ""
            if str(row.get("website","")).strip():
                links += f'<a href="{row["website"]}" target="_blank" style="margin-left:10px;color:var(--teal);font-size:.85rem;">🌐 الموقع</a>'
            if str(row.get("admissions_url","")).strip():
                links += f'<a href="{row["admissions_url"]}" target="_blank" style="margin-left:10px;color:var(--teal);font-size:.85rem;">📋 القبول</a>'
            st.markdown(f"""
<div class="uni-card">
  <h3>{row["name_ar"]} — {row["name_en"]}</h3>
  <div class="meta">📍 {row["city"]}, {row["country"]}</div>
  <div class="tags">{type_tag}{sch_tag}{lang_tags}</div>
  <div style="margin-top:10px;">{links}</div>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: المقارنة
# ═══════════════════════════════════════════════
elif st.session_state.page == "المقارنة":
    st.markdown('<h1 class="page-title">⚖️ المقارنة بين الجامعات</h1>', unsafe_allow_html=True)

    unis = unis_raw.copy()
    if unis.empty:
        st.error("ملف universities.csv غير موجود."); st.stop()

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + ", " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country", "city", "name_en"], na_position="last")

    selected = st.multiselect(
        "اختر ٢ إلى ٤ جامعات للمقارنة",
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
            with st.expander(f"{row['name_ar']}", expanded=True):
                st.markdown(f"**📍 الموقع:** {row['city']} — {row['country']}")
                st.markdown(f"**🏛️ النوع:** {row['type']}")
                st.markdown(f"**💰 المنح:** {row.get('scholarship','')}")
                rank = f"{str(row.get('ranking_source','')).strip()} {str(row.get('ranking_value','')).strip()}".strip()
                if rank:
                    st.markdown(f"**🏆 الترتيب:** {rank}")
                notes = str(row.get("accreditation_notes","")).strip()
                if notes:
                    st.markdown(f"**📝 ملاحظات:** {notes}")
                st.write("")
                if str(row.get("website","")).strip():
                    st.link_button("🌐 Website",    row["website"],        use_container_width=True)
                if str(row.get("admissions_url","")).strip():
                    st.link_button("📋 Admissions", row["admissions_url"], use_container_width=True)
                if str(row.get("programs_url","")).strip():
                    st.link_button("📚 Programs",   row["programs_url"],   use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE: رُشد — محادثة عربية ذكية
# ═══════════════════════════════════════════════
elif st.session_state.page == "رُشد":
    st.markdown("""
<div dir="rtl" style="text-align:center;margin-bottom:16px;">
  <h2 style="margin:0;">💬 رُشد — مستشارك الأكاديمي الذكي</h2>
  <p style="color:var(--muted);font-size:1rem;">
    تحدّث بالعربية بشكل طبيعي — رُشد يفهمك ويرشّح لك الجامعات المناسبة من قاعدة بياناتنا
  </p>
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
                "مرحباً! أنا رُشد، مستشارك الأكاديمي 🎓\n\n"
                "أخبرني عن نفسك:\n"
                "- ما التخصص الذي تفضله؟\n"
                "- في أي دولة تريد الدراسة؟\n"
                "- ما معدلك التقريبي؟\n"
                "- هل عندك IELTS؟ وكم درجتك؟\n\n"
                "كلّمني بشكل طبيعي وسأرشّح لك أفضل الجامعات المناسبة!"
            )
        }]

    for msg in st.session_state.rushd_messages:
        avatar = "🧭" if msg["role"] == "assistant" else "🎓"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك هنا..."):
        st.session_state.rushd_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🎓"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner("رُشد يفكر..."):
                history = [m for m in st.session_state.rushd_messages
                           if not (m["role"] == "assistant" and "مرحباً" in m["content"])]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role": "assistant", "content": reply})

    if len(st.session_state.rushd_messages) > 1:
        if st.button("🔄 محادثة جديدة", use_container_width=False):
            st.session_state.rushd_messages = []
            st.rerun()


# ═══════════════════════════════════════════════
# PAGE: تحليل البيانات ✨
# ═══════════════════════════════════════════════
elif st.session_state.page == "تحليل البيانات":
    st.markdown('<h1 class="page-title">📊 لوحة تحليل البيانات</h1>', unsafe_allow_html=True)

    unis  = unis_raw.copy()
    progs = progs_raw.copy()
    if unis.empty:
        st.error("لا تتوفر بيانات."); st.stop()

    # إحصاءات
    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    # ── صف 1: ثلاثة مخططات ──
    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        fig = px.bar(
            x=list(by_country.values()), y=list(by_country.keys()),
            orientation="h", title="الجامعات حسب الدولة",
            color=list(by_country.values()), color_continuous_scale="teal",
            labels={"x":"العدد","y":"الدولة"},
        )
        fig.update_layout(font_family="Cairo", showlegend=False,
                          coloraxis_showscale=False,
                          margin=dict(l=10,r=10,t=40,b=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        fig = px.pie(
            values=list(by_type.values()), names=list(by_type.keys()),
            title="حكومية / خاصة",
            color_discrete_sequence=["#1A6B72","#C8922A","#38BDF8"],
            hole=0.45,
        )
        fig.update_layout(font_family="Cairo",
                          margin=dict(l=10,r=10,t=40,b=10), height=300)
        st.plotly_chart(fig, use_container_width=True)

    with ch3:
        if top_fields:
            fig = px.bar(
                x=list(top_fields.keys()), y=list(top_fields.values()),
                title="أبرز التخصصات",
                color=list(top_fields.values()), color_continuous_scale="teal",
                labels={"x":"التخصص","y":"البرامج"},
            )
            fig.update_layout(font_family="Cairo", showlegend=False,
                              coloraxis_showscale=False, xaxis_tickangle=-30,
                              margin=dict(l=10,r=10,t=40,b=10), height=300)
            st.plotly_chart(fig, use_container_width=True)

    # ── صف 2: منح + لغات ──
    ch4, ch5 = st.columns(2)

    with ch4:
        pct = round(with_sch / max(len(unis), 1) * 100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pct,
            title={"text": "نسبة الجامعات التي تقدم منحاً %",
                   "font": {"family":"Cairo","size":14}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar":  {"color": "#C8922A"},
                "steps": [
                    {"range":[0,40],  "color":"#FEE2E2"},
                    {"range":[40,70], "color":"#FEF3CD"},
                    {"range":[70,100],"color":"#D1FAE5"},
                ],
            }
        ))
        fig.update_layout(font_family="Cairo", height=280,
                          margin=dict(l=20,r=20,t=40,b=10))
        st.plotly_chart(fig, use_container_width=True)

    with ch5:
        if by_lang:
            fig = px.bar(
                x=list(by_lang.keys()), y=list(by_lang.values()),
                title="لغات الدراسة",
                color=list(by_lang.values()), color_continuous_scale="blues",
                labels={"x":"اللغة","y":"البرامج"},
            )
            fig.update_layout(font_family="Cairo", showlegend=False,
                              coloraxis_showscale=False,
                              margin=dict(l=10,r=10,t=40,b=10), height=280)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── AI: تقرير + فجوات ──
    col_rep, col_gap = st.columns(2)

    with col_rep:
        st.markdown("### 🤖 تقرير ذكي تلقائي")
        st.caption("الذكاء الاصطناعي يحلل الإحصاءات ويكتب لك تقريراً شاملاً")
        if st.button("📝 اطلب التقرير الآن", use_container_width=True):
            stats = {
                "total_unis": len(unis), "by_country": by_country,
                "by_type": by_type, "top_fields": top_fields,
                "by_language": by_lang, "with_scholarships": with_sch,
                "total_progs": len(progs),
            }
            with st.spinner("الذكاء الاصطناعي يكتب التقرير..."):
                report = generate_dashboard_report(stats)
            st.markdown(f'<div class="ai-report"><h4>📊 التقرير التحليلي</h4>{report}</div>',
                        unsafe_allow_html=True)

    with col_gap:
        st.markdown("### 🔍 تحليل فجوات تعليمية")
        st.caption("الذكاء الاصطناعي يكشف الفجوات والملاحظات في منظومة التعليم الخليجي")
        if st.button("🔎 اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            st.markdown(f'<div class="gap-box">{gaps}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: من نحن
# ═══════════════════════════════════════════════
elif st.session_state.page == "من نحن":
    st.markdown('<h1 class="page-title">من نحن</h1>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 2.8, 1])
    with center:
        st.markdown("""
<div dir="rtl" style="text-align:center;font-size:1.05rem;line-height:2;">
  <p><b>بوصلة</b> منصة رقمية ذكية تهدف إلى مساعدة الطلاب وأولياء الأمور في اتخاذ قرار واعٍ ومدروس
  لاختيار الجامعة والبرنامج الأكاديمي داخل دول الخليج.</p>
  <p>جاءت فكرة بوصلة استجابةً لتحدٍ واقعي يواجه الكثير من الطلبة، وهو <b>تشتّت المعلومات</b>
  وصعوبة المقارنة بين الجامعات والبرامج وتعدد المصادر غير الموثوقة.</p>
  <p>نعمل على جمع البيانات وتنظيمها وتقديمها بطريقة مبسطة مع توظيف الذكاء الاصطناعي
  لمساعدة المستخدم على فهم الخيارات واتخاذ القرار بثقة.</p>
  <hr style="margin:18px 0;border:none;border-top:1px solid #e5e7eb;">
  <p><b>ما يميز بوصلة:</b></p>
  <p>🌍 تركيز على السياق الخليجي واحتياجات الطلبة في المنطقة</p>
  <p>💬 مستشار ذكي يتحدث العربية بشكل طبيعي</p>
  <p>📊 تحليلات إحصائية مبنية على بيانات حقيقية</p>
  <p>🛡️ استخدام مسؤول للذكاء الاصطناعي لدعم القرار لا استبداله</p>
</div>
""", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<h3 style='text-align:center;'>تواصل معنا</h3>", unsafe_allow_html=True)
        _, c2, _ = st.columns([1, 2.8, 1])
        with c2:
            ca, cb = st.columns(2)
            with ca:
                st.text_input("الاسم", placeholder="اكتب اسمك")
                st.text_input("البريد الإلكتروني", placeholder="example@email.com")
            with cb:
                st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=120)
            if st.button("إرسال", use_container_width=True):
                st.success("تم الاستلام. شكراً لتواصلك!")
            st.caption("للتعاون والشراكات: يسعدنا التواصل مع الجهات التعليمية والمبادرات المجتمعية.")
