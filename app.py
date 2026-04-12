"""
app.py — المتحكم الرئيسي لبوصلة
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
from pathlib import Path

from components import inject_global_css, render_header
from ui import (
    page_home, page_search, page_compare,
    page_rushd, page_data, page_about,
)

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="بوصلة — التعليم العالي الخليجي",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Inject global CSS (once)
# ─────────────────────────────────────────────
inject_global_css()

# ─────────────────────────────────────────────
# Data loaders
# ─────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent
UNIS_PATH  = ROOT / "universities.csv"
PROGS_PATH = ROOT / "programs.csv"


@st.cache_data(show_spinner=False)
def load_unis(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    kw = dict(encoding="utf-8", engine="python", on_bad_lines="skip")
    try:
        first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[0].lower()
        df = pd.read_csv(path, **kw) if "uni_id" in first else pd.read_csv(path, header=None, **kw)
        return _normalize_unis(df)
    except:
        return pd.DataFrame()


@st.cache_data(show_spinner=False)
def load_progs(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, encoding="utf-8", engine="python", on_bad_lines="skip")
        return _normalize_progs(df)
    except:
        return pd.DataFrame()


def _normalize_unis(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    legacy_cols = [
        "uni_id","name_ar","name_en","country","city","type",
        "website","admissions_url","programs_url","ranking_source","extra_1","extra_2",
        "scholarship","sch_notes","sch_url",
    ]
    if list(df.columns) == list(range(len(df.columns))):
        df.columns = legacy_cols[:len(df.columns)]
    if "uni_id" in df.columns and str(df.iloc[0].get("uni_id","")).lower().strip() == "uni_id":
        df = df.iloc[1:].copy()
    for c in ["ranking_value","accreditation_notes","scholarship","sch_notes","sch_url",
              "website","admissions_url","programs_url","ranking_source"]:
        if c not in df.columns:
            df[c] = ""
    df["scholarship"] = df["scholarship"].fillna("").astype(str).str.strip().replace({"nan": ""})
    needed = [
        "uni_id","name_ar","name_en","country","city","type",
        "scholarship","sch_notes","sch_url","website","admissions_url","programs_url",
        "ranking_source","ranking_value","accreditation_notes",
    ]
    for c in needed:
        if c not in df.columns:
            df[c] = ""
    return df[needed].dropna(subset=["uni_id"])


def _normalize_progs(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    needed = [
        "program_id","uni_id","level","degree_type","major_field",
        "program_name_en","program_name_ar","city","language",
        "duration_years","tuition_notes","admissions_requirements","url",
    ]
    for c in needed:
        if c not in df.columns:
            df[c] = ""
    return df[needed]


# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
unis_raw  = load_unis(UNIS_PATH)
progs_raw = load_progs(PROGS_PATH)
N_UNIS    = len(unis_raw)
N_PROGS   = len(progs_raw)
N_CTRY    = unis_raw["country"].nunique() if not unis_raw.empty else 0

# ─────────────────────────────────────────────
# Header (شعار الموقع — فوق التابات)
# ─────────────────────────────────────────────
render_header()

# ─────────────────────────────────────────────
# Navigation Tabs
# ─────────────────────────────────────────────
tab_home, tab_search, tab_compare, tab_rushd, tab_data, tab_about = st.tabs([
    "الرئيسية",
    "بحث الجامعات",
    "المقارنة",
    "رُشد",
    "لوحة البيانات",
    "من نحن",
])

with tab_home:
    page_home(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY)

with tab_search:
    page_search(unis_raw, progs_raw)

with tab_compare:
    page_compare(unis_raw, progs_raw)

with tab_rushd:
    page_rushd(unis_raw, progs_raw)

with tab_data:
    page_data(unis_raw, progs_raw, N_UNIS, N_PROGS, N_CTRY)

with tab_about:
    page_about()
