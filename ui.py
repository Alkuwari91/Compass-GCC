"""
ui.py — صفحات بوصلة — كاملة بدون حذف بيانات
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components import (
    section_header, h2, divider, stat_bar, feat_cards,
    uni_card_html, comp_card_html, ai_box,
    empty_state, metric_card, C
)
from ai_engine import (
    build_unis_context, chat_rushd,
    generate_dashboard_report, analyze_gaps,
    compare_unis_ai, quick_match,
)


def _sch(s: str) -> bool:
    """تحقق من وجود منحة — يتعامل مع NaN و Unknown بشكل صحيح"""
    v = str(s).strip()
    return v not in ("", "No", "Unknown", "nan", "none", "None", "NaN")


SVG_AI = """<svg viewBox="0 0 52 42" style="width:46px;height:36px;margin-bottom:14px;" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="8" width="36" height="28" rx="7" fill="#F0FAFA" stroke="#DEF2F1" stroke-width="1.5"/>
  <rect x="10" y="15" width="24" height="5" rx="2.5" fill="#2EC4B6" opacity="0.6"/>
  <rect x="10" y="24" width="18" height="3.5" rx="1.75" fill="#E5E7EB"/>
  <rect x="10" y="30" width="21" height="3.5" rx="1.75" fill="#E5E7EB"/>
  <circle cx="39" cy="10" r="10" fill="#2EC4B6" opacity="0.15"/>
  <text x="33.5" y="14.5" font-size="8.5" fill="#1B4F4A" font-weight="800">AI</text>
</svg>"""

SVG_CHART = """<svg viewBox="0 0 52 42" style="width:46px;height:36px;margin-bottom:14px;" xmlns="http://www.w3.org/2000/svg">
  <rect x="3"  y="28" width="9" height="12" rx="2.5" fill="#2EC4B6" opacity="0.3"/>
  <rect x="15" y="20" width="9" height="20" rx="2.5" fill="#2EC4B6" opacity="0.55"/>
  <rect x="27" y="11" width="9" height="29" rx="2.5" fill="#2EC4B6" opacity="0.8"/>
  <rect x="39" y="4"  width="9" height="36" rx="2.5" fill="#2EC4B6"/>
  <polyline points="7.5,28 19.5,20 31.5,11 43.5,4"
    stroke="#1B4F4A" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="7.5"  cy="28" r="3" fill="#1B4F4A"/>
  <circle cx="19.5" cy="20" r="3" fill="#1B4F4A"/>
  <circle cx="31.5" cy="11" r="3" fill="#1B4F4A"/>
  <circle cx="43.5" cy="4"  r="3" fill="#1B4F4A"/>
</svg>"""

SVG_COMPARE = """<svg viewBox="0 0 52 42" style="width:46px;height:36px;margin-bottom:14px;" xmlns="http://www.w3.org/2000/svg">
  <rect x="2"  y="6" width="22" height="32" rx="6" fill="#F0FAFA" stroke="#2EC4B6" stroke-width="1.5"/>
  <rect x="28" y="6" width="22" height="32" rx="6" fill="#F0FAFA" stroke="#E5E7EB" stroke-width="1.5"/>
  <rect x="7"  y="13" width="12" height="4"   rx="2" fill="#2EC4B6" opacity="0.7"/>
  <rect x="7"  y="21" width="10" height="3"   rx="1.5" fill="#E5E7EB"/>
  <rect x="7"  y="27" width="11" height="3"   rx="1.5" fill="#E5E7EB"/>
  <rect x="33" y="13" width="12" height="4"   rx="2" fill="#9CA3AF" opacity="0.45"/>
  <rect x="33" y="21" width="10" height="3"   rx="1.5" fill="#E5E7EB"/>
  <rect x="33" y="27" width="11" height="3"   rx="1.5" fill="#E5E7EB"/>
  <line x1="27" y1="12" x2="27" y2="38" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="3,2.5"/>
</svg>"""

CHART_PALETTE = ["#2EC4B6", "#1B4F4A", "#3AAFA9", "#B2DFD8", "#DEF2F1"]
CHART_LAYOUT  = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans Arabic", color="#6B7280", size=13),
    margin=dict(l=12, r=12, t=40, b=12),
)


# ══════════════════════════════════════════════
# الرئيسية
# ══════════════════════════════════════════════
def page_home(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY):

    # Hero — centered
    st.markdown(f"""
<div style="
  text-align:center;
  padding:56px 36px 40px;
  direction:rtl;
">
  <div style="
    display:inline-flex;align-items:center;gap:8px;
    background:rgba(46,196,182,.10);
    border:1px solid rgba(46,196,182,.28);
    border-radius:100px;
    padding:6px 18px;
    font-size:12px;font-weight:700;
    letter-spacing:2px;text-transform:uppercase;
    color:#1B4F4A;
    margin-bottom:26px;
  ">
    <span style="width:5px;height:5px;border-radius:50%;background:#2EC4B6;display:inline-block;"></span>
    الدليل الذكي للتعليم العالي الخليجي
  </div>

  <div style="
    font-family:'Syne',sans-serif;
    font-size:72px;font-weight:800;
    color:#1B4F4A;
    line-height:.92;letter-spacing:-4px;
    margin-bottom:22px;
  ">بوصلة</div>

  <div style="
    width:48px;height:4px;
    background:#2EC4B6;border-radius:2px;
    margin:0 auto 24px;
  "></div>

  <div style="
    font-size:16px;color:#6B7280;
    line-height:1.85;
    max-width:500px;margin:0 auto 38px;
  ">
    اكتشف الجامعات وقارن التخصصات واتخذ قرارك التعليمي بثقة
    مع مستشار ذكي يتحدث العربية
  </div>
</div>
""", unsafe_allow_html=True)

    stat_bar([
        (f"{N_UNIS}", "جامعة"),
        (str(N_CTRY),  "دولة خليجية"),
        (f"{N_PROGS}", "برنامج"),
        ("AI",         "ذكاء اصطناعي"),
    ])

    # Section divider with label
    st.markdown("""<div style="
  display:flex;align-items:center;gap:14px;
  color:#9CA3AF;font-size:12px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  margin:0 0 30px;direction:rtl;
">
  <div style="flex:1;height:1px;background:#E5E7EB;"></div>
  ما تقدمه بوصلة
  <div style="flex:1;height:1px;background:#E5E7EB;"></div>
</div>""", unsafe_allow_html=True)

    feat_cards([
        {
            "num": "01", "overline": "المستشار الذكي",
            "title": "رُشد",
            "body": "تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح أفضل الجامعات من قاعدة بياناتنا مع شرح أسباب كل توصية.",
            "svg": SVG_AI,
        },
        {
            "num": "02", "overline": "الإحصاء والتحليل",
            "title": "لوحة البيانات",
            "body": "مخططات تفاعلية وتقارير ذكية تحوّل بيانات التعليم الخليجي إلى رؤى إحصائية واضحة وقابلة للمقارنة.",
            "svg": SVG_CHART,
        },
        {
            "num": "03", "overline": "القرار المدروس",
            "title": "المقارنة",
            "body": "قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — النوع، المنح، الترتيب، والروابط الرسمية في مكان واحد.",
            "svg": SVG_COMPARE,
        },
    ])

    divider()

    section_header("رؤيتنا ورسالتنا", "نحو قرار تعليمي أفضل")

    with st.expander("الرؤية", expanded=True):
        st.markdown("""نسعى في بوصلة إلى إعادة تعريف تجربة اختيار التعليم في الخليج، عبر منصة ذكية
توجّه الشباب نحو تخصصاتهم وجامعاتهم المناسبة، وتحوّل القرار التعليمي من حيرة فردية إلى مسار واضح مدروس.""")

    with st.expander("الرسالة"):
        st.markdown("""تلتزم بوصلة بتمكين الطلبة وأولياء الأمور من اتخاذ قرارات تعليمية دقيقة
من خلال منصة ذكية تعتمد على الذكاء الاصطناعي والبيانات الموثوقة،
لتقديم توجيه واضح ومخصص يربط بين قدرات الطالب وخيارات التعليم.""")

    with st.expander("القيم"):
        st.markdown("""<div class="baw-values-grid">
  <div class="baw-val-card"><div class="baw-val-title">الوضوح</div><div class="baw-val-body">تبسيط القرار التعليمي</div></div>
  <div class="baw-val-card"><div class="baw-val-title">العدالة</div><div class="baw-val-body">عرض الخيارات دون تحيّز</div></div>
  <div class="baw-val-card"><div class="baw-val-title">التمكين</div><div class="baw-val-body">فهم الذات قبل التخصص</div></div>
  <div class="baw-val-card"><div class="baw-val-title">الابتكار</div><div class="baw-val-body">AI في خدمة التعليم</div></div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# بحث الجامعات — جميع الـ 58 جامعة
# ══════════════════════════════════════════════
def page_search(unis_raw, progs_raw):
    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    section_header("الاستكشاف", "بحث الجامعات")

    if unis.empty:
        st.error("ملف universities.csv غير موجود.")
        return

    # Search bar
    q = st.text_input("", placeholder="ابحث عن جامعة أو مدينة أو دولة...")

    # Filters — 3 columns
    c1, c2, c3 = st.columns(3)
    countries = sorted([x for x in unis["country"].dropna().unique() if str(x).strip()])
    country   = c1.selectbox("الدولة",  ["الكل"] + countries, key="f_country")
    types_    = sorted([x for x in unis["type"].dropna().unique() if str(x).strip()])
    uni_type  = c2.selectbox("النوع",   ["الكل"] + types_,    key="f_type")
    yn        = c3.selectbox("المنح",   ["الكل", "متاحة", "غير متاحة"], key="f_sch")

    # Filters — 2 columns
    c4, c5 = st.columns(2)
    levels_ = sorted([x for x in progs["level"].dropna().unique() if str(x).strip()]) \
              if not progs.empty else []
    level   = c4.selectbox("المرحلة الدراسية", ["الكل"] + levels_, key="f_level")
    majors_ = sorted([x for x in progs["major_field"].dropna().unique() if str(x).strip()]) \
              if not progs.empty else []
    major   = c5.selectbox("التخصص",          ["الكل"] + majors_,  key="f_major")

    # حدد إذا في فلتر نشط
    has_filter = (
        q.strip() != "" or
        country   != "الكل" or
        uni_type  != "الكل" or
        yn        != "الكل" or
        level     != "الكل" or
        major     != "الكل"
    )

    if not has_filter:
        empty_state("🔍", "ابدأ البحث",
                    "اكتب اسم جامعة أو مدينة، أو استخدم أحد الفلاتر أعلاه لاستعراض الجامعات")
        return

    # ── Apply filters (data-complete, no row limits) ──
    f = unis.copy()
    if country  != "الكل": f = f[f["country"] == country]
    if uni_type != "الكل": f = f[f["type"]    == uni_type]

    if yn == "متاحة":
        f = f[f["scholarship"].apply(_sch)]
    elif yn == "غير متاحة":
        f = f[~f["scholarship"].apply(_sch)]

    if q.strip():
        ql = q.strip().lower()
        mask = (
            f["name_en"].str.lower().str.contains(ql, na=False) |
            f["name_ar"].str.lower().str.contains(ql, na=False) |
            f["city"].str.lower().str.contains(ql, na=False)    |
            f["country"].str.lower().str.contains(ql, na=False)
        )
        f = f[mask]

    # Program-based filters — no aggressive join
    if (major != "الكل" or level != "الكل") and not progs.empty:
        pm = progs.copy()
        if major != "الكل": pm = pm[pm["major_field"] == major]
        if level != "الكل": pm = pm[pm["level"]       == level]
        matching_ids = pm["uni_id"].dropna().unique()
        f = f[f["uni_id"].isin(matching_ids)]

    total = len(f)
    st.markdown(f'<div class="baw-chip">{total} جامعة</div>', unsafe_allow_html=True)

    if f.empty:
        st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
        return

    # ── Render ALL matching unis (no head() limit) ──
    for _, row in f.iterrows():
        langs = []
        if not progs.empty:
            langs = list(
                progs[progs["uni_id"] == str(row["uni_id"])]["language"]
                .dropna().unique()[:3]
            )
        uni_card_html(
            name_ar=row["name_ar"],
            name_en=row["name_en"],
            city=row["city"],
            country=row["country"],
            uni_type=row["type"],
            scholarship=row.get("scholarship", ""),
            langs=langs,
            website=row.get("website", ""),
            admissions_url=row.get("admissions_url", ""),
            uni_has_sch_fn=_sch,
        )


# ══════════════════════════════════════════════
# المقارنة
# ══════════════════════════════════════════════
def page_compare(unis_raw, progs_raw):
    unis = unis_raw.copy()

    section_header("التقييم المقارن", "مقارنة الجامعات")

    if unis.empty:
        st.error("ملف universities.csv غير موجود.")
        return

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = (
        unis["name_ar"] + " — " +
        unis["name_en"] + " (" +
        unis["city"]    + "، " +
        unis["country"] + ")"
    )
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country","city","name_en"], na_position="last")

    selected = st.multiselect(
        "اختر من ٢ إلى ٤ جامعات للمقارنة",
        options=unis["uni_id"].tolist(),
        format_func=lambda x: label_map.get(str(x), str(x)),
        max_selections=4,
        key="compare_sel",
    )

    if len(selected) < 2:
        empty_state("⚖️", "اختر جامعتين على الأقل", "يمكنك مقارنة حتى ٤ جامعات معاً")
        return

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_c = st.columns(len(selected))
    for i, uid in enumerate(selected):
        row_df = comp[comp["uni_id"] == uid]
        if row_df.empty:
            continue
        row = row_df.iloc[0]
        with cols_c[i]:
            st.markdown(comp_card_html(row.to_dict()), unsafe_allow_html=True)
            st.write("")
            w  = str(row.get("website","")).strip()
            au = str(row.get("admissions_url","")).strip()
            pu = str(row.get("programs_url","")).strip()
            if w  and w  != "nan": st.link_button("الموقع الرسمي",      w,  use_container_width=True)
            if au and au != "nan": st.link_button("القبول والتسجيل",    au, use_container_width=True)
            if pu and pu != "nan": st.link_button("البرامج الأكاديمية", pu, use_container_width=True)

    # Programs table — all rows, all columns
    progs = progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        divider()
        h2("البرامج المتاحة للجامعات المختارة")

        cp = progs[progs["uni_id"].isin(selected)].copy()
        if cp.empty:
            st.info("لا تتوفر بيانات برامج للجامعات المختارة.")
        else:
            show = [c for c in [
                "uni_id","program_name_ar","program_name_en",
                "level","degree_type","major_field",
                "language","duration_years"
            ] if c in cp.columns]
            rename = {
                "uni_id": "الجامعة",
                "program_name_ar": "البرنامج",
                "program_name_en": "Program",
                "level": "المرحلة",
                "degree_type": "الدرجة",
                "major_field": "التخصص",
                "language": "اللغة",
                "duration_years": "المدة",
            }
            df = cp[show].rename(columns=rename)
            if "الجامعة" in df.columns:
                id_to_ar = dict(zip(unis["uni_id"], unis["name_ar"]))
                df["الجامعة"] = df["الجامعة"].map(id_to_ar).fillna(df["الجامعة"])
            st.dataframe(df, use_container_width=True, hide_index=True)

    divider()
    h2("المقارنة الذكية بالذكاء الاصطناعي")
    st.markdown('<p class="t-small" style="margin:-8px 0 16px;">أضف ملفك الأكاديمي للحصول على توصية مخصصة (اختياري)</p>', unsafe_allow_html=True)
    profile_txt = st.text_input(
        "",
        placeholder="مثال: طالب هندسة، IELTS 6.5، يفضل المنح الدراسية",
        key="comp_profile",
        label_visibility="collapsed",
    )
    if st.button("اطلب المقارنة الذكية", use_container_width=True, key="btn_compare"):
        unis_data = [
            comp[comp["uni_id"] == uid].iloc[0].to_dict()
            for uid in selected
            if uid in comp["uni_id"].values
        ]
        with st.spinner("جاري التحليل..."):
            result = compare_unis_ai(unis_data, profile_txt)
        ai_box("المقارنة الذكية", result)


# ══════════════════════════════════════════════
# رُشد
# ══════════════════════════════════════════════
def page_rushd(unis_raw, progs_raw):
    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    section_header(
        "المستشار الأكاديمي الذكي", "رُشد",
        subtitle="تحدّث بالعربية — رُشد يفهم ملفك ويرشّح لك الجامعات المناسبة من قاعدة بياناتنا الكاملة"
    )

    if unis.empty:
        st.error("ملف universities.csv غير موجود.")
        return

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    # ── Quick match ────────────────────────────
    h2("التحليل السريع")
    c1, c2, c3 = st.columns(3)
    countries_list = sorted([x for x in unis["country"].dropna().unique() if str(x).strip()])
    qm_country = c1.selectbox("الدولة المفضلة", ["الكل"] + countries_list, key="qm_country")
    qm_major   = c2.text_input("التخصص المطلوب",  placeholder="مثال: هندسة الحاسب",  key="qm_major")
    qm_ielts   = c3.text_input("درجة IELTS",       placeholder="مثال: 6.5",            key="qm_ielts")

    if st.button("حلّل بسرعة", use_container_width=True, key="btn_quick"):
        if not qm_major.strip():
            st.warning("يرجى إدخال التخصص المطلوب.")
        else:
            with st.spinner("جاري التحليل..."):
                res = quick_match(
                    {"country": qm_country, "major": qm_major,
                     "ielts": qm_ielts or "غير محدد"},
                    st.session_state.unis_context,
                )
            top3    = res.get("top_3", [])
            advice  = res.get("advice", "")
            missing = res.get("missing", [])

            if top3:
                qr_cols = st.columns(len(top3))
                for i, item in enumerate(top3[:3]):
                    uid    = item.get("uni_id", "")
                    row_df = unis[unis["uni_id"] == uid]
                    city_c = sch_tag = ""
                    if not row_df.empty:
                        r      = row_df.iloc[0]
                        city_c = f"{r.get('city','')}، {r.get('country','')}"
                        if _sch(str(r.get("scholarship",""))):
                            sch_tag = '<span class="baw-tag baw-tag-sch">منحة دراسية</span>'
                    with qr_cols[i]:
                        fit = item.get("fit","مناسب")
                        st.markdown(f"""<div class="baw-uni-card" style="
  flex-direction:column;align-items:flex-start;
  border-top:3px solid #2EC4B6;padding:18px;">
  <div class="baw-uni-name">{item.get('name_ar', uid)}</div>
  <div class="baw-uni-sub">{city_c}</div>
  <div style="color:#6B7280;font-size:13px;margin:8px 0;line-height:1.75;">
    {item.get('reason','')}
  </div>
  <div class="baw-tags">
    {sch_tag}
    <span class="baw-tag baw-tag-gov">{fit}</span>
  </div>
</div>""", unsafe_allow_html=True)

            if advice:
                ai_box("نصيحة رُشد", advice)
            if missing:
                m_html = " ".join(
                    f'<span class="baw-tag baw-tag-sch">{m}</span>'
                    for m in missing
                )
                st.markdown(
                    f'<div style="margin-top:12px;font-size:14px;color:#6B7280;">'
                    f'قد تحتاج إلى: {m_html}</div>',
                    unsafe_allow_html=True,
                )

    divider()
    h2("المحادثة مع رُشد")

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{
            "role": "assistant",
            "content": (
                "مرحباً، أنا رُشد 🧭\n\n"
                "أخبرني عن نفسك:\n"
                "- التخصص الذي تريده\n"
                "- الدولة المفضلة\n"
                "- معدلك التقريبي\n"
                "- هل عندك IELTS وكم درجتك؟\n\n"
                "وسأرشّح لك الجامعات المناسبة."
            ),
        }]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"],
                             avatar="🧭" if msg["role"] == "assistant" else "🎓"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🎓"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner(""):
                history = [
                    m for m in st.session_state.rushd_messages
                    if not (m["role"] == "assistant" and "مرحباً" in m["content"])
                ]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role": "assistant", "content": reply})

    if len(st.session_state.rushd_messages) > 1:
        if st.button("محادثة جديدة", key="new_chat"):
            st.session_state.rushd_messages = []
            st.rerun()


# ══════════════════════════════════════════════
# لوحة البيانات
# ══════════════════════════════════════════════
def page_data(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY):
    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    section_header("الإحصاء والتحليل", "لوحة البيانات")

    if unis.empty:
        st.error("لا تتوفر بيانات.")
        return

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(_sch).sum())
    top_fields = progs["major_field"].value_counts().head(10).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict()             if not progs.empty else {}

    # Metric cards
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card(N_UNIS,   "إجمالي الجامعات")
    with m2: metric_card(N_PROGS,  "إجمالي البرامج")
    with m3: metric_card(with_sch, "جامعة تقدم منحاً")
    with m4: metric_card(N_CTRY,   "دولة خليجية")

    st.write("")

    T260 = {**CHART_LAYOUT, "height": 260}
    T300 = {**CHART_LAYOUT, "height": 300}

    ch1, ch2 = st.columns(2)
    with ch1:
        fig = px.bar(
            x=list(by_country.values()), y=list(by_country.keys()),
            orientation="h", title="الجامعات حسب الدولة",
            color_discrete_sequence=[CHART_PALETTE[0]],
        )
        fig.update_layout(**T260); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        fig = px.pie(
            values=list(by_type.values()), names=list(by_type.keys()),
            title="توزيع النوع (حكومية / خاصة)", hole=0.52,
            color_discrete_sequence=CHART_PALETTE,
        )
        fig.update_layout(**T260); fig.update_traces(textfont_color="white", textfont_size=13)
        st.plotly_chart(fig, use_container_width=True)

    if top_fields:
        fig = px.bar(
            x=list(top_fields.keys()), y=list(top_fields.values()),
            title="أبرز التخصصات (أكثر عدداً من البرامج)",
            color_discrete_sequence=[CHART_PALETTE[1]],
        )
        fig.update_layout(**{**CHART_LAYOUT, "height":280, "xaxis_tickangle":-35})
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        if by_lang:
            fig = px.bar(
                x=list(by_lang.keys()), y=list(by_lang.values()),
                title="لغات الدراسة",
                color_discrete_sequence=[CHART_PALETTE[2]],
            )
            fig.update_layout(**T260); fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with ch4:
        pct = round(with_sch / max(len(unis), 1) * 100, 1)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=pct,
            title={"text": "% الجامعات التي تقدم منحاً",
                   "font": {"family":"IBM Plex Sans Arabic","color":"#6B7280","size":13}},
            number={"font":{"color":"#1B4F4A","family":"IBM Plex Sans Arabic","size":28}},
            gauge={
                "axis":   {"range":[0,100],"tickcolor":"#D1D5DB","tickfont":{"size":11}},
                "bar":    {"color":"#2EC4B6"},
                "bgcolor":"rgba(0,0,0,0)",
                "bordercolor":"#E5E7EB",
                "steps":  [{"range":[0,100],"color":"rgba(46,196,182,.07)"}],
            },
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans Arabic", color="#6B7280"),
            height=250, margin=dict(l=20,r=20,t=40,b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Scholarship stacked bar — all countries
    if not unis.empty and "scholarship" in unis.columns:
        divider()
        h2("توزيع المنح الدراسية حسب الدولة")
        sch_rows = []
        for _, row in unis.iterrows():
            ctry = str(row.get("country","")).strip()
            sch  = str(row.get("scholarship","")).strip()
            if not ctry or ctry == "nan":
                continue
            for cat in ["Local", "GCC", "International"]:
                sch_rows.append({
                    "الدولة":    ctry,
                    "نوع المنحة": cat,
                    "عدد":       1 if cat in sch else 0,
                })
        sch_df = pd.DataFrame(sch_rows).groupby(
            ["الدولة","نوع المنحة"], as_index=False
        )["عدد"].sum()
        sch_df = sch_df[sch_df["عدد"] > 0]
        if not sch_df.empty:
            fig_sch = px.bar(
                sch_df, x="عدد", y="الدولة", color="نوع المنحة",
                orientation="h", barmode="stack",
                color_discrete_map={
                    "Local":         CHART_PALETTE[0],
                    "GCC":           CHART_PALETTE[1],
                    "International": CHART_PALETTE[2],
                },
            )
            fig_sch.update_layout(
                **{**CHART_LAYOUT, "height":320},
                legend=dict(bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#6B7280", size=13)),
            )
            fig_sch.update_traces(marker_line_width=0)
            st.plotly_chart(fig_sch, use_container_width=True)

    divider()
    col_r, col_g = st.columns(2)
    with col_r:
        h2("التقرير التحليلي الذكي")
        st.markdown('<p class="t-small" style="margin:-6px 0 14px;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير", use_container_width=True, key="btn_report"):
            with st.spinner("جاري كتابة التقرير..."):
                report = generate_dashboard_report({
                    "total_unis":      len(unis),
                    "by_country":      by_country,
                    "by_type":         by_type,
                    "top_fields":      top_fields,
                    "by_language":     by_lang,
                    "with_scholarships": with_sch,
                    "total_progs":     len(progs),
                })
            ai_box("التقرير التحليلي", report)

    with col_g:
        h2("تحليل الفجوات التعليمية")
        st.markdown('<p class="t-small" style="margin:-6px 0 14px;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات", use_container_width=True, key="btn_gaps"):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            ai_box("الفجوات التعليمية", gaps, variant="gold")


# ══════════════════════════════════════════════
# من نحن
# ══════════════════════════════════════════════
def page_about():
    section_header("هويتنا", "من نحن")

    st.markdown("""<div style="font-size:15px;color:#6B7280;line-height:2;margin-bottom:32px;direction:rtl;">
  <p style="font-size:17px;font-weight:700;color:#0F1923;margin-bottom:16px;">
    منصة رقمية ذكية لاتخاذ قرارات تعليمية مدروسة في دول مجلس التعاون الخليجي.
  </p>
  <p style="margin-bottom:12px;">
    جاءت فكرة بوصلة استجابةً لتحدٍ واقعي يواجه الكثير من الطلبة —
    تشتّت المعلومات وصعوبة المقارنة بين الجامعات والبرامج وتعدد المصادر غير الموثوقة.
  </p>
  <p>
    نعمل على جمع البيانات التعليمية الخليجية وتنظيمها وتقديمها بطريقة مبسطة،
    مع توظيف الذكاء الاصطناعي لمساعدة المستخدم على فهم خياراته واتخاذ قراره بثقة.
  </p>
</div>""", unsafe_allow_html=True)

    divider()
    section_header("قيمنا", "ما يحركنا")
    st.markdown("""<div class="baw-values-grid">
  <div class="baw-val-card"><div class="baw-val-title">الوضوح</div><div class="baw-val-body">تبسيط القرار التعليمي</div></div>
  <div class="baw-val-card"><div class="baw-val-title">العدالة</div><div class="baw-val-body">عرض الخيارات دون تحيّز</div></div>
  <div class="baw-val-card"><div class="baw-val-title">التمكين</div><div class="baw-val-body">فهم الذات قبل التخصص</div></div>
  <div class="baw-val-card"><div class="baw-val-title">الابتكار</div><div class="baw-val-body">AI في خدمة التعليم</div></div>
</div>""", unsafe_allow_html=True)

    divider()
    section_header("تواصل", "تواصل معنا")

    ca, cb = st.columns(2)
    with ca:
        st.text_input("الاسم",              placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني", placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=118)

    if st.button("إرسال", use_container_width=True, key="btn_contact"):
        st.success("تم الاستلام. شكراً لتواصلك.")

    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
