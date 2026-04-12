"""
ui.py — صفحات وأقسام بوصلة
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components import (
    section, divider, stat_bar, feat_cards, uni_card,
    comp_card, ai_box, empty_state, metric_card, COLORS
)
from ai_engine import (
    build_unis_context, chat_rushd,
    generate_dashboard_report, analyze_gaps,
    compare_unis_ai, quick_match
)


def uni_has_sch(s):
    return str(s).strip() not in ["", "No", "Unknown", "nan", "none", "None"]


# ══════════════════════════════════════════════
# 1. الرئيسية
# ══════════════════════════════════════════════
def page_home(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY):

    # ── Hero ──────────────────────────────────
    st.markdown(f"""
<div style="text-align:center;padding:52px 32px 36px;">

  <div style="
    display:inline-flex;align-items:center;gap:7px;
    background:rgba(46,196,182,.10);
    border:1px solid rgba(46,196,182,.25);
    border-radius:100px;padding:5px 16px;
    font-size:10px;font-weight:700;letter-spacing:2px;
    text-transform:uppercase;color:#1B4F4A;
    margin-bottom:24px;
  ">
    <span style="width:5px;height:5px;border-radius:50%;background:#2EC4B6;display:inline-block;"></span>
    الدليل الذكي للتعليم الخليجي
  </div>

  <div style="
    font-family:'Syne',sans-serif;
    font-size:68px;font-weight:800;
    color:#1B4F4A;
    line-height:.95;letter-spacing:-3px;
    margin-bottom:20px;
  ">بوصلة</div>

  <div style="
    width:44px;height:3px;
    background:#2EC4B6;border-radius:2px;
    margin:0 auto 22px;
  "></div>

  <div style="
    font-size:15px;color:#6B7280;
    line-height:1.85;max-width:480px;
    margin:0 auto 36px;
  ">
    اكتشف الجامعات وقارن التخصصات واتخذ قرارك التعليمي بثقة
    مع مستشار ذكي يتحدث العربية
  </div>

</div>
""", unsafe_allow_html=True)

    # ── Stats bar ──────────────────────────────
    stat_bar([
        (f"{N_UNIS}+", "جامعة"),
        (str(N_CTRY),   "دولة خليجية"),
        (f"{N_PROGS}+", "برنامج"),
        ("AI",          "ذكاء اصطناعي"),
    ])

    # ── Divider with label ─────────────────────
    st.markdown("""
<div style="
  display:flex;align-items:center;gap:12px;
  color:#9CA3AF;font-size:10px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  margin:0 0 28px;
">
  <div style="flex:1;height:1px;background:#E5E7EB;"></div>
  ما تقدمه بوصلة
  <div style="flex:1;height:1px;background:#E5E7EB;"></div>
</div>""", unsafe_allow_html=True)

    # ── Feature cards ──────────────────────────
    feat_cards([
        {
            "num": "01",
            "overline": "المستشار الذكي",
            "title": "رُشد",
            "body": "تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح أفضل الجامعات من قاعدة بياناتنا مع شرح أسباب كل توصية.",
            "svg": """<svg viewBox="0 0 52 40" style="width:44px;height:34px;margin-bottom:12px;" xmlns="http://www.w3.org/2000/svg">
  <rect x="5" y="8" width="34" height="26" rx="6" fill="#F0FAFA" stroke="#DEF2F1" stroke-width="1.5"/>
  <rect x="11" y="15" width="22" height="4" rx="2" fill="#2EC4B6" opacity="0.6"/>
  <rect x="11" y="23" width="16" height="3" rx="1.5" fill="#E5E7EB"/>
  <rect x="11" y="29" width="19" height="3" rx="1.5" fill="#E5E7EB"/>
  <circle cx="38" cy="10" r="9" fill="#2EC4B6" opacity="0.18"/>
  <text x="33" y="14" font-size="8" fill="#1B4F4A" font-weight="800">AI</text>
</svg>"""
        },
        {
            "num": "02",
            "overline": "الإحصاء والتحليل",
            "title": "لوحة البيانات",
            "body": "مخططات تفاعلية وتقارير ذكية تحوّل بيانات التعليم الخليجي إلى رؤى إحصائية واضحة وقابلة للمقارنة.",
            "svg": """<svg viewBox="0 0 52 40" style="width:44px;height:34px;margin-bottom:12px;" xmlns="http://www.w3.org/2000/svg">
  <rect x="3"  y="27" width="8" height="10" rx="2" fill="#2EC4B6" opacity="0.3"/>
  <rect x="14" y="20" width="8" height="17" rx="2" fill="#2EC4B6" opacity="0.5"/>
  <rect x="25" y="12" width="8" height="25" rx="2" fill="#2EC4B6" opacity="0.75"/>
  <rect x="36" y="5"  width="8" height="32" rx="2" fill="#2EC4B6"/>
  <polyline points="7,27 18,20 29,12 40,5" stroke="#1B4F4A" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <circle cx="7"  cy="27" r="2.5" fill="#1B4F4A"/>
  <circle cx="18" cy="20" r="2.5" fill="#1B4F4A"/>
  <circle cx="29" cy="12" r="2.5" fill="#1B4F4A"/>
  <circle cx="40" cy="5"  r="2.5" fill="#1B4F4A"/>
</svg>"""
        },
        {
            "num": "03",
            "overline": "القرار المدروس",
            "title": "المقارنة",
            "body": "قارن بين ٢ إلى ٤ جامعات جنباً إلى جنب — النوع، المنح، الترتيب، والروابط الرسمية في مكان واحد.",
            "svg": """<svg viewBox="0 0 52 40" style="width:44px;height:34px;margin-bottom:12px;" xmlns="http://www.w3.org/2000/svg">
  <rect x="2"  y="6" width="21" height="30" rx="5" fill="#F0FAFA" stroke="#2EC4B6" stroke-width="1.5"/>
  <rect x="29" y="6" width="21" height="30" rx="5" fill="#F0FAFA" stroke="#E5E7EB" stroke-width="1.5"/>
  <rect x="7"  y="13" width="11" height="3" rx="1.5" fill="#2EC4B6" opacity="0.7"/>
  <rect x="7"  y="20" width="9"  height="2.5" rx="1.25" fill="#E5E7EB"/>
  <rect x="7"  y="26" width="10" height="2.5" rx="1.25" fill="#E5E7EB"/>
  <rect x="34" y="13" width="11" height="3" rx="1.5" fill="#9CA3AF" opacity="0.45"/>
  <rect x="34" y="20" width="9"  height="2.5" rx="1.25" fill="#E5E7EB"/>
  <rect x="34" y="26" width="10" height="2.5" rx="1.25" fill="#E5E7EB"/>
  <line x1="26" y1="12" x2="26" y2="36" stroke="#E5E7EB" stroke-width="1.5" stroke-dasharray="3,2"/>
</svg>"""
        },
    ])

    divider()

    # ── Vision / Mission / Values ──────────────
    section("رؤيتنا ورسالتنا", "نحو قرار تعليمي أفضل")

    with st.expander("الرؤية", expanded=True):
        st.markdown("نسعى في بوصلة إلى إعادة تعريف تجربة اختيار التعليم في الخليج، عبر منصة ذكية توجّه الشباب نحو تخصصاتهم وجامعاتهم المناسبة، وتحوّل القرار التعليمي من حيرة فردية إلى مسار واضح مدروس.")
    with st.expander("الرسالة"):
        st.markdown("تلتزم بوصلة بتمكين الطلبة وأولياء الأمور من اتخاذ قرارات تعليمية دقيقة من خلال منصة ذكية تعتمد على الذكاء الاصطناعي والبيانات الموثوقة، لتقديم توجيه واضح ومخصص.")
    with st.expander("القيم"):
        st.markdown("""<div class="baw-values-grid" style="margin-top:12px;">
  <div class="baw-val-card"><div class="baw-val-title">الوضوح</div><div class="baw-val-body">تبسيط القرار التعليمي</div></div>
  <div class="baw-val-card"><div class="baw-val-title">العدالة</div><div class="baw-val-body">عرض الخيارات دون تحيّز</div></div>
  <div class="baw-val-card"><div class="baw-val-title">التمكين</div><div class="baw-val-body">فهم الذات قبل التخصص</div></div>
  <div class="baw-val-card"><div class="baw-val-title">الابتكار</div><div class="baw-val-body">AI في خدمة التعليم</div></div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# 2. بحث الجامعات
# ══════════════════════════════════════════════
def page_search(unis_raw, progs_raw):
    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    section("الاستكشاف", "بحث الجامعات")

    if unis.empty:
        st.error("ملف universities.csv غير موجود.")
        return

    # Search bar
    q = st.text_input("", placeholder="ابحث عن جامعة، مدينة، أو دولة...")

    # Filters
    c1, c2, c3 = st.columns(3)
    c4, c5     = st.columns(2)

    countries = sorted([x for x in unis["country"].unique() if str(x).strip()])
    country   = c1.selectbox("الدولة",    ["الكل"] + countries)
    types_    = sorted([x for x in unis["type"].unique() if str(x).strip()])
    uni_type  = c2.selectbox("النوع",     ["الكل"] + types_)
    yn        = c3.selectbox("المنح",     ["الكل", "متاحة", "غير متاحة"])

    levels_   = sorted([x for x in progs["level"].unique() if str(x).strip()]) if not progs.empty else []
    level     = c4.selectbox("المرحلة",  ["الكل"] + levels_)
    majors_   = sorted([x for x in progs["major_field"].unique() if str(x).strip()]) if not progs.empty else []
    major     = c5.selectbox("التخصص",   ["الكل"] + majors_)

    # Show results only when user filters/searches
    has_filter = (
        q.strip() != "" or country != "الكل" or uni_type != "الكل" or
        level != "الكل" or major != "الكل" or yn != "الكل"
    )

    if not has_filter:
        empty_state("🔍", "ابدأ البحث", "اكتب اسم جامعة أو مدينة، أو اختر فلتراً من الأعلى")
        return

    f = unis.copy()
    if country  != "الكل": f = f[f["country"] == country]
    if uni_type != "الكل": f = f[f["type"] == uni_type]
    if yn == "متاحة":       f = f[f["scholarship"].apply(uni_has_sch)]
    if yn == "غير متاحة":   f = f[~f["scholarship"].apply(uni_has_sch)]
    if q.strip():
        ql = q.strip().lower()
        mask = (
            f["name_en"].str.lower().str.contains(ql, na=False) |
            f["name_ar"].str.lower().str.contains(ql, na=False) |
            f["city"].str.lower().str.contains(ql, na=False)
        )
        f = f[mask]
    if (major != "الكل" or level != "الكل") and not progs.empty:
        pm = progs.copy()
        if major != "الكل": pm = pm[pm["major_field"] == major]
        if level != "الكل": pm = pm[pm["level"] == level]
        f = f[f["uni_id"].isin(pm["uni_id"].unique())]

    st.markdown(f'<div class="baw-chip">{len(f)} نتيجة</div>', unsafe_allow_html=True)

    if f.empty:
        st.info("لا توجد نتائج — جرّب تعديل الفلاتر.")
        return

    for _, row in f.head(40).iterrows():
        langs = []
        if not progs.empty:
            langs = list(progs[progs["uni_id"] == str(row["uni_id"])]["language"].dropna().unique()[:2])
        uni_card(
            name_ar=row["name_ar"],
            name_en=row["name_en"],
            city=row["city"],
            country=row["country"],
            uni_type=row["type"],
            scholarship=row.get("scholarship", ""),
            langs=langs,
            website=row.get("website", ""),
            admissions_url=row.get("admissions_url", ""),
            uni_has_sch_fn=uni_has_sch,
        )


# ══════════════════════════════════════════════
# 3. المقارنة
# ══════════════════════════════════════════════
def page_compare(unis_raw, progs_raw):
    unis = unis_raw.copy()

    section("التقييم المقارن", "مقارنة الجامعات")

    if unis.empty:
        st.error("ملف universities.csv غير موجود.")
        return

    unis["uni_id"] = unis["uni_id"].astype(str).str.strip()
    unis = unis[unis["uni_id"].ne("") & unis["uni_id"].ne("nan")].drop_duplicates("uni_id")
    unis["label"] = unis["name_ar"] + " — " + unis["name_en"] + " (" + unis["city"] + "، " + unis["country"] + ")"
    label_map = dict(zip(unis["uni_id"], unis["label"]))
    unis = unis.sort_values(["country", "city", "name_en"], na_position="last")

    selected = st.multiselect(
        "اختر من ٢ إلى ٤ جامعات للمقارنة",
        options=unis["uni_id"].tolist(),
        format_func=lambda x: label_map.get(str(x), str(x)),
        max_selections=4,
    )

    if len(selected) < 2:
        empty_state("⚖️", "اختر جامعتين للمقارنة", "يمكنك مقارنة حتى ٤ جامعات معاً")
        return

    comp = unis[unis["uni_id"].isin(selected)].copy()
    cols_c = st.columns(len(selected))
    for i, uid in enumerate(selected):
        row = comp[comp["uni_id"] == uid].iloc[0]
        with cols_c[i]:
            st.markdown(comp_card(row), unsafe_allow_html=True)
            st.write("")
            if str(row.get("website","")).strip():
                st.link_button("الموقع الرسمي",      row["website"],        use_container_width=True)
            if str(row.get("admissions_url","")).strip():
                st.link_button("القبول والتسجيل",    row["admissions_url"], use_container_width=True)
            if str(row.get("programs_url","")).strip():
                st.link_button("البرامج الأكاديمية", row["programs_url"],   use_container_width=True)

    # Programs table
    progs = progs_raw.copy()
    if not progs.empty and "uni_id" in progs.columns:
        divider()
        section("", "البرامج المتاحة للجامعات المختارة", tight=True)
        cp = progs[progs["uni_id"].isin(selected)].copy()
        if cp.empty:
            st.info("لا تتوفر بيانات برامج للجامعات المختارة.")
        else:
            show = [c for c in ["uni_id","program_name_ar","program_name_en","level","major_field","language","duration_years"] if c in cp.columns]
            rename = {
                "uni_id":"الجامعة","program_name_ar":"البرنامج (عربي)","program_name_en":"البرنامج (إنجليزي)",
                "level":"المرحلة","major_field":"التخصص","language":"اللغة","duration_years":"المدة (سنوات)"
            }
            df = cp[show].rename(columns=rename)
            if "الجامعة" in df.columns:
                id_to_ar = dict(zip(unis["uni_id"], unis["name_ar"]))
                df["الجامعة"] = df["الجامعة"].map(id_to_ar).fillna(df["الجامعة"])
            st.dataframe(df, use_container_width=True, hide_index=True)

    # AI comparison
    divider()
    section("الذكاء الاصطناعي", "المقارنة الذكية", tight=True)
    profile_txt = st.text_input(
        "", placeholder="ملفك الأكاديمي (اختياري) — مثال: طالب هندسة، IELTS 6.5، يفضل المنح",
        key="comp_profile", label_visibility="collapsed"
    )
    if st.button("اطلب مقارنة ذكية", use_container_width=True):
        unis_data = [comp[comp["uni_id"]==uid].iloc[0].to_dict() for uid in selected if uid in comp["uni_id"].values]
        with st.spinner("جاري التحليل..."):
            result = compare_unis_ai(unis_data, profile_txt)
        ai_box("المقارنة الذكية", result)


# ══════════════════════════════════════════════
# 4. رُشد
# ══════════════════════════════════════════════
def page_rushd(unis_raw, progs_raw):
    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    section("المستشار الأكاديمي الذكي", "رُشد")
    st.markdown('<p style="color:#6B7280;font-size:14px;margin:-14px 0 24px;">تحدّث بالعربية بشكل طبيعي — رُشد يفهم ملفك ويرشّح لك الجامعات المناسبة</p>', unsafe_allow_html=True)

    if unis.empty:
        st.error("ملف universities.csv غير موجود.")
        return

    if "unis_context" not in st.session_state:
        with st.spinner("جاري تحضير قاعدة البيانات..."):
            st.session_state.unis_context = build_unis_context(unis, progs)

    # Quick match
    section("", "التحليل السريع", tight=True)
    c1, c2, c3 = st.columns(3)
    countries_list = sorted([x for x in unis["country"].unique() if str(x).strip()])
    qm_country = c1.selectbox("الدولة المفضلة", ["الكل"] + countries_list, key="qm_country")
    qm_major   = c2.text_input("التخصص المطلوب", placeholder="مثال: هندسة الحاسب", key="qm_major")
    qm_ielts   = c3.text_input("درجة IELTS",      placeholder="مثال: 6.5",           key="qm_ielts")

    if st.button("حلّل بسرعة", use_container_width=True, key="btn_quick"):
        if not qm_major.strip():
            st.warning("يرجى إدخال التخصص المطلوب.")
        else:
            with st.spinner("جاري التحليل..."):
                res = quick_match(
                    {"country": qm_country, "major": qm_major, "ielts": qm_ielts or "غير محدد"},
                    st.session_state.unis_context
                )
            top3    = res.get("top_3", [])
            advice  = res.get("advice", "")
            missing = res.get("missing", [])

            if top3:
                qr_cols = st.columns(len(top3))
                for i, item in enumerate(top3[:3]):
                    uid     = item.get("uni_id", "")
                    row_df  = unis[unis["uni_id"] == uid]
                    city_c  = ""
                    sch_tag = ""
                    if not row_df.empty:
                        r = row_df.iloc[0]
                        city_c = f"{r.get('city','')}، {r.get('country','')}"
                        if uni_has_sch(str(r.get("scholarship",""))):
                            sch_tag = '<span class="baw-tag baw-tag-sch">منحة دراسية</span>'
                    with qr_cols[i]:
                        st.markdown(f"""
<div class="baw-uni-card" style="flex-direction:column;align-items:flex-start;border-top:3px solid #2EC4B6;padding:18px 18px 14px;">
  <div class="baw-uni-name">{item.get('name_ar', uid)}</div>
  <div class="baw-uni-sub">{city_c}</div>
  <div style="color:#6B7280;font-size:12px;margin:8px 0;line-height:1.7;">{item.get('reason','')}</div>
  <div class="baw-tags">{sch_tag}<span class="baw-tag baw-tag-gov">{item.get('fit','مناسب')}</span></div>
</div>""", unsafe_allow_html=True)

            if advice:
                ai_box("نصيحة رُشد", advice)
            if missing:
                m_html = " ".join([f'<span class="baw-tag baw-tag-sch">{m}</span>' for m in missing])
                st.markdown(f'<div style="margin-top:10px;font-size:12px;color:#6B7280;">قد تحتاج إلى: {m_html}</div>', unsafe_allow_html=True)

    divider()
    section("", "المحادثة", tight=True)

    if "rushd_messages" not in st.session_state:
        st.session_state.rushd_messages = [{"role":"assistant","content":
            "مرحباً، أنا رُشد.\n\nأخبرني عن نفسك:\n- التخصص الذي تريده\n- الدولة المفضلة\n- معدلك التقريبي\n- هل عندك IELTS وكم درجتك؟\n\nوسأرشّح لك الجامعات المناسبة."}]

    for msg in st.session_state.rushd_messages:
        with st.chat_message(msg["role"], avatar="🧭" if msg["role"]=="assistant" else "🎓"):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اكتب رسالتك..."):
        st.session_state.rushd_messages.append({"role":"user","content":user_input})
        with st.chat_message("user", avatar="🎓"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🧭"):
            with st.spinner(""):
                history = [m for m in st.session_state.rushd_messages
                           if not(m["role"]=="assistant" and "مرحباً" in m["content"])]
                reply = chat_rushd(history, st.session_state.unis_context)
            st.markdown(reply)
            st.session_state.rushd_messages.append({"role":"assistant","content":reply})

    if len(st.session_state.rushd_messages) > 1:
        if st.button("محادثة جديدة", key="new_chat"):
            st.session_state.rushd_messages = []
            st.rerun()


# ══════════════════════════════════════════════
# 5. البيانات
# ══════════════════════════════════════════════
def page_data(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY):
    unis  = unis_raw.copy()
    progs = progs_raw.copy()

    section("الإحصاء والتحليل", "لوحة البيانات")

    if unis.empty:
        st.error("لا تتوفر بيانات.")
        return

    by_country = unis["country"].value_counts().to_dict()
    by_type    = unis["type"].value_counts().to_dict()
    with_sch   = int(unis["scholarship"].apply(uni_has_sch).sum())
    top_fields = progs["major_field"].value_counts().head(8).to_dict() if not progs.empty else {}
    by_lang    = progs["language"].value_counts().to_dict() if not progs.empty else {}

    # Metric cards
    m1, m2, m3, m4 = st.columns(4)
    with m1: metric_card(N_UNIS,     "إجمالي الجامعات")
    with m2: metric_card(N_PROGS,    "إجمالي البرامج")
    with m3: metric_card(with_sch,   "جامعة تقدم منحاً")
    with m4: metric_card(N_CTRY,     "دولة خليجية")

    st.write("")

    T = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans Arabic", color="#6B7280"),
        margin=dict(l=10, r=10, t=36, b=10), height=260,
    )
    PALETTE = ["#2EC4B6", "#1B4F4A", "#3AAFA9", "#DEF2F1"]

    ch1, ch2 = st.columns(2)
    with ch1:
        fig = px.bar(
            x=list(by_country.values()), y=list(by_country.keys()),
            orientation="h", title="الجامعات حسب الدولة",
            color_discrete_sequence=[PALETTE[0]]
        )
        fig.update_layout(**T); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        fig = px.pie(
            values=list(by_type.values()), names=list(by_type.keys()),
            title="حكومية / خاصة", hole=0.55,
            color_discrete_sequence=PALETTE
        )
        fig.update_layout(**T); fig.update_traces(textfont_color="white")
        st.plotly_chart(fig, use_container_width=True)

    if top_fields:
        fig = px.bar(
            x=list(top_fields.keys()), y=list(top_fields.values()),
            title="أبرز التخصصات", color_discrete_sequence=[PALETTE[1]]
        )
        fig.update_layout(**T, xaxis_tickangle=-30)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    if by_lang:
        fig = px.bar(
            x=list(by_lang.keys()), y=list(by_lang.values()),
            title="لغات الدراسة", color_discrete_sequence=[PALETTE[2]]
        )
        fig.update_layout(**T); fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Scholarship stacked bar
    if not unis.empty and "scholarship" in unis.columns:
        divider()
        section("المنح الدراسية", "توزيع المنح حسب الدولة", tight=True)
        sch_data = []
        for _, row in unis.iterrows():
            ctry = str(row.get("country","")).strip()
            sch  = str(row.get("scholarship","")).strip()
            if not ctry or ctry == "nan": continue
            for cat in ["Local", "GCC", "International"]:
                sch_data.append({"الدولة": ctry, "نوع المنحة": cat, "عدد": 1 if cat in sch else 0})
        sch_df = pd.DataFrame(sch_data).groupby(["الدولة","نوع المنحة"], as_index=False)["عدد"].sum()
        sch_df = sch_df[sch_df["عدد"] > 0]
        if not sch_df.empty:
            fig_sch = px.bar(
                sch_df, x="عدد", y="الدولة", color="نوع المنحة",
                orientation="h", barmode="stack",
                color_discrete_map={"Local": PALETTE[0], "GCC": PALETTE[1], "International": PALETTE[2]}
            )
            fig_sch.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="IBM Plex Sans Arabic", color="#6B7280"),
                margin=dict(l=10,r=10,t=30,b=10), height=300,
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#6B7280"))
            )
            fig_sch.update_traces(marker_line_width=0)
            st.plotly_chart(fig_sch, use_container_width=True)

    divider()
    col_r, col_g = st.columns(2)
    with col_r:
        section("", "التقرير التحليلي الذكي", tight=True)
        st.markdown('<p style="font-size:13px;color:#6B7280;margin:-8px 0 14px;">الذكاء الاصطناعي يحلل إحصاءات قاعدة البيانات ويكتب تقريراً شاملاً</p>', unsafe_allow_html=True)
        if st.button("اطلب التقرير", use_container_width=True):
            with st.spinner("جاري كتابة التقرير..."):
                report = generate_dashboard_report({
                    "total_unis": len(unis), "by_country": by_country,
                    "by_type": by_type, "top_fields": top_fields,
                    "by_language": by_lang, "with_scholarships": with_sch,
                    "total_progs": len(progs)
                })
            ai_box("التقرير التحليلي", report)
    with col_g:
        section("", "تحليل الفجوات التعليمية", tight=True)
        st.markdown('<p style="font-size:13px;color:#6B7280;margin:-8px 0 14px;">رؤى إحصائية عن الفجوات في منظومة التعليم العالي الخليجي</p>', unsafe_allow_html=True)
        if st.button("اكشف الفجوات", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                gaps = analyze_gaps(unis, progs)
            ai_box("الفجوات التعليمية", gaps, variant="gold")


# ══════════════════════════════════════════════
# 6. من نحن
# ══════════════════════════════════════════════
def page_about():
    section("هويتنا", "من نحن")

    st.markdown("""
<div style="font-size:15px;color:#6B7280;line-height:2;margin-bottom:32px;">
  <p style="color:#111827;font-size:16px;font-weight:600;margin-bottom:14px;">
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
    section("قيمنا", "ما يحركنا")
    st.markdown("""<div class="baw-values-grid">
  <div class="baw-val-card"><div class="baw-val-title">الوضوح</div><div class="baw-val-body">تبسيط القرار التعليمي</div></div>
  <div class="baw-val-card"><div class="baw-val-title">العدالة</div><div class="baw-val-body">عرض الخيارات دون تحيّز</div></div>
  <div class="baw-val-card"><div class="baw-val-title">التمكين</div><div class="baw-val-body">فهم الذات قبل التخصص</div></div>
  <div class="baw-val-card"><div class="baw-val-title">الابتكار</div><div class="baw-val-body">AI في خدمة التعليم</div></div>
</div>""", unsafe_allow_html=True)

    divider()
    section("تواصل", "تواصل معنا")
    ca, cb = st.columns(2)
    with ca:
        st.text_input("الاسم",              placeholder="اكتب اسمك")
        st.text_input("البريد الإلكتروني", placeholder="example@email.com")
    with cb:
        st.text_area("رسالتك", placeholder="اكتب رسالتك هنا...", height=116)
    if st.button("إرسال", use_container_width=True):
        st.success("تم الاستلام. شكراً لتواصلك.")
    st.caption("للتعاون والشراكات مع الجهات التعليمية والمبادرات المجتمعية.")
