"""
app.py — المتحكم الرئيسي لبوصلة
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from pathlib import Path

from components import inject_global_css, render_header
from ui import page_home, page_search, page_compare, page_rushd, page_data, page_about

# ─── Config ───────────────────────────────────
st.set_page_config(
    page_title="بوصلة — التعليم العالي الخليجي",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_global_css()

# ─── Paths ────────────────────────────────────
ROOT       = Path(__file__).resolve().parent
UNIS_PATH  = ROOT / "universities.csv"
PROGS_PATH = ROOT / "programs.csv"


# ─── Data loaders (complete, no row loss) ─────
@st.cache_data(show_spinner=False)
def load_unis(path: Path) -> pd.DataFrame:
    """
    يقرأ universities.csv كاملاً.
    - لا يحذف أي صف إلا إذا كان uni_id فارغاً تماماً
    - يُصحح NaN في scholarship
    - لا يوجد head() أو deduplication مفرط
    """
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        df = pd.read_csv(
            path, encoding="utf-8", engine="python", on_bad_lines="skip"
        )
        # إزالة صف header مكرر إن وجد
        if "uni_id" in df.columns:
            first = str(df.iloc[0].get("uni_id","")).lower().strip()
            if first == "uni_id":
                df = df.iloc[1:].reset_index(drop=True)
        # تأكد من وجود الأعمدة المطلوبة
        needed = [
            "uni_id","name_ar","name_en","country","city","type",
            "website","admissions_url","programs_url",
            "ranking_source","ranking_value","accreditation_notes",
            "scholarship","sch_notes","sch_url",
        ]
        for c in needed:
            if c not in df.columns:
                df[c] = ""
        # نظّف scholarship بدون حذف الصفوف
        df["scholarship"] = (
            df["scholarship"]
            .fillna("")
            .astype(str)
            .str.strip()
            .replace({"nan": "", "NaN": ""})
        )
        # احتفظ فقط بالصفوف التي عندها uni_id حقيقي
        df = df[df["uni_id"].notna() & (df["uni_id"].astype(str).str.strip() != "")]
        # أزل duplicates بناءً على uni_id فقط (keep first)
        df = df.drop_duplicates(subset=["uni_id"], keep="first")
        return df[needed].reset_index(drop=True)
    except Exception as e:
        st.warning(f"خطأ في قراءة الجامعات: {e}")
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_progs(path: Path) -> pd.DataFrame:
    """
    يقرأ programs.csv كاملاً — جميع الـ 119 برنامج
    - لا يحذف أي صف
    - لا يوجد head() أو filtering
    """
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        df = pd.read_csv(
            path, encoding="utf-8", engine="python", on_bad_lines="skip"
        )
        # تأكد من وجود الأعمدة الأساسية
        base = [
            "program_id","uni_id","level","degree_type","major_field",
            "program_name_en","program_name_ar","city","language",
            "duration_years","tuition_notes","admissions_requirements","url",
        ]
        for c in base:
            if c not in df.columns:
                df[c] = ""
        # احتفظ بجميع الأعمدة الأصلية أيضاً
        return df.reset_index(drop=True)
    except Exception as e:
        st.warning(f"خطأ في قراءة البرامج: {e}")
        return pd.DataFrame()


# ─── Load data ────────────────────────────────
unis_raw  = load_unis(UNIS_PATH)
progs_raw = load_progs(PROGS_PATH)
N_UNIS    = len(unis_raw)
N_PROGS   = len(progs_raw)
N_CTRY    = unis_raw["country"].nunique() if not unis_raw.empty else 0

# ─── Header ───────────────────────────────────
render_header()

# ─── Navigation Tabs ──────────────────────────
tabs = st.tabs([
    "الرئيسية",
    "بحث الجامعات",
    "المقارنة",
    "رُشد",
    "لوحة البيانات",
    "من نحن",
])

with tabs[0]: page_home(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY)
with tabs[1]: page_search(unis_raw, progs_raw)
with tabs[2]: page_compare(unis_raw, progs_raw)
with tabs[3]: page_rushd(unis_raw, progs_raw)
with tabs[4]: page_data(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY)
with tabs[5]: page_about()
