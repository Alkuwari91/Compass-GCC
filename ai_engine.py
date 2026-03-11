"""
ai_engine.py — محرك الذكاء الاصطناعي لبوصلة
"""
import json
import os
import streamlit as st
from openai import OpenAI


# ─────────────────────────────────────────────
# Client
# ─────────────────────────────────────────────
def _get_client() -> OpenAI:
    key = st.secrets.get("openai_api_key", os.environ.get("OPENAI_API_KEY", ""))
    return OpenAI(api_key=key)


# ─────────────────────────────────────────────
# Build context strings from dataframes
# ─────────────────────────────────────────────
def build_unis_context(unis_df, progs_df) -> str:
    """تحويل قاعدة البيانات إلى نص مضغوط يُرسل للنموذج"""
    if unis_df is None or unis_df.empty:
        return "لا توجد بيانات جامعات."

    lines = []
    for _, row in unis_df.iterrows():
        uid = str(row.get("uni_id", "")).strip()
        if not uid or uid == "nan":
            continue

        name_ar  = str(row.get("name_ar", "")).strip()
        name_en  = str(row.get("name_en", "")).strip()
        country  = str(row.get("country", "")).strip()
        city     = str(row.get("city", "")).strip()
        utype    = str(row.get("type", "")).strip()
        sch      = str(row.get("scholarship", "Unknown")).strip()

        # برامج مختصرة
        progs_str = ""
        if progs_df is not None and not progs_df.empty and "uni_id" in progs_df.columns:
            sub = progs_df[progs_df["uni_id"] == uid]
            progs = []
            for _, p in sub.head(6).iterrows():
                pn = str(p.get("program_name_ar") or p.get("program_name_en", "")).strip()
                lv = str(p.get("level", "")).strip()
                lg = str(p.get("language", "")).strip()
                if pn:
                    progs.append(f"{pn}({lv},{lg})")
            progs_str = " | ".join(progs)

        lines.append(
            f"[{uid}] {name_ar} / {name_en} | {country},{city} | {utype} | منح:{sch} | {progs_str}"
        )

    return "\n".join(lines[:70])


# ─────────────────────────────────────────────
# 1. رُشد — محادثة عربية طبيعية
# ─────────────────────────────────────────────
RUSHD_SYSTEM = """أنت رُشد، مستشار أكاديمي ذكي متخصص في التعليم العالي بدول مجلس التعاون الخليجي.
تتحدث بالعربية دائماً. أسلوبك ودود، مختصر، وعملي.

قاعدة بيانات الجامعات المتاحة:
{context}

مهمتك:
١. اسمع الطالب وافهم ملفه (المعدل، التخصص، الدولة، اللغة، IELTS، الميزانية، المنح).
٢. رشّح أفضل ٣ جامعات من القاعدة أعلاه مع سبب كل توصية.
٣. اذكر متطلبات القبول المتوقعة.
٤. إذا سأل عن جامعة بعينها اعطِه تفاصيلها.

قواعد صارمة:
- لا تذكر جامعات غير موجودة في القاعدة.
- إذا لم تعرف معلومة قل ذلك صراحةً.
- اسأل إذا احتجت معلومات ناقصة عن الطالب.
- الرد لا يتجاوز ٢٠٠ كلمة إلا إذا طُلب التفصيل.
"""


def chat_rushd(messages: list, unis_context: str) -> str:
    """يرسل محادثة كاملة لـ GPT ويعيد الرد"""
    system = RUSHD_SYSTEM.format(context=unis_context)
    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=700,
            temperature=0.5,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ خطأ في الاتصال: {e}"


# ─────────────────────────────────────────────
# 2. تقرير لوحة البيانات
# ─────────────────────────────────────────────
def generate_dashboard_report(stats: dict) -> str:
    """يولّد تقريراً تحليلياً عربياً من إحصاءات قاعدة البيانات"""
    prompt = f"""أنت محلل بيانات متخصص في التعليم العالي الخليجي.
بناءً على الإحصاءات التالية اكتب تقريراً تحليلياً باللغة العربية (١٥٠-٢٠٠ كلمة).
أبرز فيه: أهم الأرقام، الفجوات، والتوصيات.

الإحصاءات:
- إجمالي الجامعات: {stats.get('total_unis', 0)}
- توزيع حسب الدولة: {json.dumps(stats.get('by_country', {}), ensure_ascii=False)}
- حكومية/خاصة: {json.dumps(stats.get('by_type', {}), ensure_ascii=False)}
- أبرز التخصصات: {json.dumps(stats.get('top_fields', {}), ensure_ascii=False)}
- لغات الدراسة: {json.dumps(stats.get('by_language', {}), ensure_ascii=False)}
- جامعات تقدم منحاً: {stats.get('with_scholarships', 0)} من أصل {stats.get('total_unis', 0)}
- إجمالي البرامج: {stats.get('total_progs', 0)}

اكتب فقرات متماسكة، واذكر أرقاماً محددة من الإحصاءات أعلاه."""

    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.65,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ تعذّر توليد التقرير: {e}"


# ─────────────────────────────────────────────
# 3. شرح المطابقة الذكية
# ─────────────────────────────────────────────
def explain_matches(profile: dict, matches: list) -> str:
    """يكتب شرحاً ذكياً لأسباب توصية الجامعات"""
    if not matches:
        return ""

    matches_text = "\n".join([
        f"- {m.get('name_ar', '')} ({m.get('country', '')}, {m.get('city', '')}) "
        f"| نقاط: {m.get('score', 0)} | {m.get('reasons', '')}"
        for m in matches[:3]
    ])

    prompt = f"""ملف الطالب:
- الدولة المفضلة: {profile.get('country', 'غير محدد')}
- التخصص: {profile.get('major', 'غير محدد')}
- المستوى: {profile.get('level', 'غير محدد')}
- المعدل: {profile.get('gpa', 0) or 'لم يُدخل'}
- IELTS: {profile.get('ielts', 0) or 'لم يُدخل'}
- المنح مهمة: {profile.get('scholarship', 'لا')}

الجامعات المقترحة:
{matches_text}

اكتب تحليلاً مختصراً (٨٠-١٠٠ كلمة) باللغة العربية يشرح لماذا هذه الجامعات مناسبة لهذا الطالب تحديداً.
كن عملياً واذكر نقاط القوة وأي تحفظات مهمة."""

    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.6,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return ""


# ─────────────────────────────────────────────
# 4. تحليل فجوات تعليمية
# ─────────────────────────────────────────────
def analyze_gaps(unis_df, progs_df) -> str:
    """يحلل فجوات في منظومة التعليم الخليجي"""
    if unis_df is None or unis_df.empty:
        return "لا تتوفر بيانات كافية."

    # إحصاءات سريعة
    by_country = unis_df["country"].value_counts().to_dict() if "country" in unis_df.columns else {}
    by_type = unis_df["type"].value_counts().to_dict() if "type" in unis_df.columns else {}

    fields_by_country = {}
    if progs_df is not None and not progs_df.empty and "major_field" in progs_df.columns and "uni_id" in progs_df.columns:
        merged = progs_df.merge(unis_df[["uni_id", "country"]], on="uni_id", how="left")
        if "country" in merged.columns:
            fields_by_country = merged.groupby("country")["major_field"].nunique().to_dict()

    prompt = f"""أنت خبير تحليل بيانات التعليم العالي الخليجي.
بناءً على البيانات التالية، حدّد ٣-٥ فجوات أو ملاحظات لافتة في منظومة التعليم العالي بدول الخليج:

- توزيع الجامعات حسب الدولة: {json.dumps(by_country, ensure_ascii=False)}
- توزيع حسب النوع: {json.dumps(by_type, ensure_ascii=False)}
- تنوع التخصصات حسب الدولة: {json.dumps(fields_by_country, ensure_ascii=False)}

اكتب كل فجوة في سطر مع رمز ◈ في البداية، واذكر أرقاماً من البيانات.
الهدف: رؤى تحليلية حقيقية مبنية على الأرقام."""

    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.6,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ تعذّر التحليل: {e}"
