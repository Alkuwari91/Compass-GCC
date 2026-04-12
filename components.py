"""
components.py — مكونات واجهة بوصلة القابلة لإعادة الاستخدام
"""
import streamlit as st


# ─────────────────────────────────────────────
# Design Tokens
# ─────────────────────────────────────────────
COLORS = {
    "primary":   "#1B4F4A",   # أخضر بترولي داكن
    "teal":      "#2EC4B6",   # فيروزي
    "teal_soft": "rgba(46,196,182,.10)",
    "teal_border":"rgba(46,196,182,.25)",
    "ink":       "#111827",
    "muted":     "#6B7280",
    "pale":      "#F0FAFA",
    "white":     "#FFFFFF",
    "border":    "#E5E7EB",
    "bg":        "#F8FAFB",
    "gold":      "#B45309",
    "gold_bg":   "#FFFBEB",
    "gold_border":"#FDE68A",
}

RADIUS = "14px"
SHADOW = "0 1px 3px rgba(0,0,0,.06), 0 4px 12px rgba(0,0,0,.04)"


# ─────────────────────────────────────────────
# inject_global_css — يُستدعى مرة واحدة فقط
# ─────────────────────────────────────────────
def inject_global_css():
    st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Reset & Base ─────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"] {{
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  background: {COLORS["bg"]} !important;
  color: {COLORS["ink"]} !important;
  direction: rtl !important;
}}

/* ── Hide Streamlit chrome ────────────────── */
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
button[kind="header"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer, #MainMenu {{ display: none !important; }}

[data-testid="stAppViewContainer"] {{ background: {COLORS["bg"]} !important; }}
[data-testid="stMain"] {{ background: transparent !important; padding-top: 0 !important; }}

/* ── Page container ───────────────────────── */
[data-testid="stMainBlockContainer"] {{
  max-width: 960px !important;
  margin: 0 auto !important;
  padding: 0 0 80px !important;
  background: {COLORS["white"]} !important;
  border-left:  1px solid {COLORS["border"]} !important;
  border-right: 1px solid {COLORS["border"]} !important;
  min-height: 100vh !important;
}}

/* ── RTL enforcement ──────────────────────── */
input, textarea, [role="textbox"] {{
  direction: rtl !important;
  text-align: right !important;
}}
div[data-baseweb="select"] * {{ direction: rtl !important; }}
label {{
  direction: rtl !important;
  text-align: right !important;
  color: {COLORS["muted"]} !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}}

/* ── Typography helpers ───────────────────── */
.baw-overline {{
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: {COLORS["teal"]};
  margin-bottom: 8px;
  display: block;
}}
.baw-h1 {{
  font-family: 'Syne', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: {COLORS["ink"]};
  letter-spacing: -.5px;
  margin-bottom: 6px;
}}
.baw-h2 {{
  font-family: 'Syne', sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: {COLORS["ink"]};
  letter-spacing: -.3px;
  margin-bottom: 14px;
}}
.baw-body {{
  font-size: 14px;
  color: {COLORS["muted"]};
  line-height: 1.85;
}}
.baw-divider {{
  height: 1px;
  background: {COLORS["border"]};
  margin: 36px 0;
  border: none;
}}
.baw-chip {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: {COLORS["teal_soft"]};
  border: 1px solid {COLORS["teal_border"]};
  border-radius: 100px;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 700;
  color: {COLORS["primary"]};
  margin-bottom: 14px;
}}

/* ── Cards ────────────────────────────────── */
.baw-card {{
  background: {COLORS["white"]};
  border: 1px solid {COLORS["border"]};
  border-radius: {RADIUS};
  padding: 24px;
  transition: border-color .18s, box-shadow .18s;
  height: 100%;
}}
.baw-card:hover {{
  border-color: {COLORS["teal"]};
  box-shadow: 0 4px 20px rgba(46,196,182,.10);
}}
.baw-feat-grid {{
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 16px;
  margin-bottom: 40px;
  align-items: stretch;
}}
.baw-feat-card {{
  background: {COLORS["white"]};
  border: 1px solid {COLORS["border"]};
  border-radius: {RADIUS};
  padding: 26px 22px;
  display: flex;
  flex-direction: column;
  transition: border-color .18s, transform .18s, box-shadow .18s;
}}
.baw-feat-card:hover {{
  border-color: {COLORS["teal"]};
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(46,196,182,.09);
}}
.baw-feat-num {{
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  color: {COLORS["teal"]};
  margin-bottom: 14px;
  display: block;
}}
.baw-feat-title {{
  font-family: 'Syne', sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: {COLORS["ink"]};
  margin-bottom: 8px;
}}
.baw-feat-body {{
  font-size: 13px;
  color: {COLORS["muted"]};
  line-height: 1.8;
  flex: 1;
}}

/* ── Uni list cards ───────────────────────── */
.baw-uni-card {{
  background: {COLORS["white"]};
  border: 1px solid {COLORS["border"]};
  border-radius: {RADIUS};
  padding: 16px 20px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  transition: border-color .15s;
}}
.baw-uni-card:hover {{ border-color: {COLORS["teal"]}; }}
.baw-uni-name {{ font-size: 14px; font-weight: 700; color: {COLORS["ink"]}; margin-bottom: 3px; }}
.baw-uni-sub  {{ font-size: 12px; color: #9CA3AF; }}
.baw-uni-right {{ display: flex; gap: 8px; flex-shrink: 0; }}
.baw-uni-link {{
  font-size: 11px; font-weight: 600; color: {COLORS["teal"]};
  text-decoration: none; padding: 4px 10px;
  border: 1px solid {COLORS["teal_border"]};
  border-radius: 7px; background: {COLORS["teal_soft"]};
  white-space: nowrap; transition: all .15s;
}}
.baw-uni-link:hover {{ background: {COLORS["teal"]}; color: #17252A; border-color: {COLORS["teal"]}; }}

/* ── Tags ─────────────────────────────────── */
.baw-tags {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 7px; }}
.baw-tag {{ padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 600; }}
.baw-tag-gov  {{ background: rgba(46,196,182,.1); color: #1B4F4A; border: 1px solid rgba(46,196,182,.22); }}
.baw-tag-priv {{ background: #F3F4F6; color: #374151; border: 1px solid #E5E7EB; }}
.baw-tag-sch  {{ background: {COLORS["gold_bg"]}; color: {COLORS["gold"]}; border: 1px solid {COLORS["gold_border"]}; }}
.baw-tag-lang {{ background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }}

/* ── Comparison cards ─────────────────────── */
.baw-comp-card {{ background: {COLORS["white"]}; border: 1px solid {COLORS["border"]}; border-radius: {RADIUS}; padding: 20px; }}
.baw-comp-head {{ font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 800; color: {COLORS["ink"]}; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid {COLORS["border"]}; }}
.baw-comp-row  {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #F9FAFB; }}
.baw-comp-label {{ font-size: 12px; color: #9CA3AF; }}
.baw-comp-val   {{ font-size: 12px; color: {COLORS["ink"]}; font-weight: 600; text-align: left; max-width: 55%; overflow: hidden; text-overflow: ellipsis; }}

/* ── AI result boxes ──────────────────────── */
.baw-ai-box {{
  background: {COLORS["pale"]};
  border: 1px solid {COLORS["teal_border"]};
  border-radius: {RADIUS};
  padding: 22px 24px;
  margin-top: 14px;
  line-height: 1.9;
  color: {COLORS["ink"]};
}}
.baw-ai-label {{
  font-size: 10px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: {COLORS["teal"]};
  margin-bottom: 10px; display: block;
}}
.baw-gap-box {{
  background: {COLORS["gold_bg"]};
  border: 1px solid {COLORS["gold_border"]};
  border-radius: {RADIUS};
  padding: 22px 24px; margin-top: 14px;
  line-height: 1.9; color: {COLORS["ink"]};
}}

/* ── Values grid ──────────────────────────── */
.baw-values-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; }}
.baw-val-card {{ background: {COLORS["pale"]}; border-radius: {RADIUS}; padding: 18px 12px; text-align: center; border: 1px solid rgba(46,196,182,.15); }}
.baw-val-title {{ font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 800; color: #17252A; margin-bottom: 4px; }}
.baw-val-body  {{ font-size: 11px; color: {COLORS["muted"]}; }}

/* ── Stat bar ─────────────────────────────── */
.baw-stats-bar {{
  display: flex;
  justify-content: center;
  border: 1px solid {COLORS["border"]};
  border-radius: {RADIUS};
  overflow: hidden;
  margin: 0 auto 44px;
  max-width: 480px;
}}
.baw-stat-item {{
  flex: 1;
  padding: 16px 12px;
  text-align: center;
  border-left: 1px solid {COLORS["border"]};
}}
.baw-stat-item:last-child {{ border-left: none; }}
.baw-stat-n {{ font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; color: {COLORS["ink"]}; }}
.baw-stat-l {{ font-size: 11px; color: #9CA3AF; margin-top: 3px; }}

/* ── Form inputs ──────────────────────────── */
.stTextInput > div > div {{
  background: {COLORS["white"]} !important;
  border: 1px solid {COLORS["border"]} !important;
  border-radius: 10px !important;
}}
.stTextInput > div > div:focus-within {{
  border-color: {COLORS["teal"]} !important;
  box-shadow: 0 0 0 3px rgba(46,196,182,.10) !important;
}}
.stTextInput > div > div > input {{
  color: {COLORS["ink"]} !important;
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
}}
input::placeholder, textarea::placeholder {{
  color: #9CA3AF !important; opacity: 1 !important;
}}
.stTextArea > div > div {{
  background: {COLORS["white"]} !important;
  border: 1px solid {COLORS["border"]} !important;
  border-radius: 10px !important;
}}
.stTextArea > div > div > textarea {{ color: {COLORS["ink"]} !important; }}

/* ── Selects ──────────────────────────────── */
div[data-baseweb="select"] > div {{
  background: {COLORS["white"]} !important;
  border: 1px solid {COLORS["border"]} !important;
  border-radius: 10px !important;
  color: {COLORS["ink"]} !important;
}}
div[data-baseweb="select"] * {{ color: {COLORS["ink"]} !important; }}
div[data-baseweb="popover"] li {{ background: {COLORS["white"]} !important; color: {COLORS["ink"]} !important; }}
div[data-baseweb="popover"] li:hover {{ background: {COLORS["pale"]} !important; color: {COLORS["teal"]} !important; }}

/* ── Buttons ──────────────────────────────── */
.stButton > button {{
  background: {COLORS["white"]} !important;
  border: 1px solid {COLORS["border"]} !important;
  color: {COLORS["ink"]} !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  font-size: 13px !important;
  transition: all .15s !important;
}}
.stButton > button:hover {{
  background: {COLORS["pale"]} !important;
  border-color: {COLORS["teal"]} !important;
  color: {COLORS["teal"]} !important;
}}
.stLinkButton a {{
  background: {COLORS["teal_soft"]} !important;
  border: 1px solid {COLORS["teal_border"]} !important;
  color: {COLORS["primary"]} !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 12px !important;
}}
.stLinkButton a:hover {{
  background: {COLORS["teal"]} !important;
  color: #17252A !important;
}}

/* ── Expanders ────────────────────────────── */
div[data-testid="stExpander"] {{
  background: {COLORS["white"]} !important;
  border: 1px solid {COLORS["border"]} !important;
  border-radius: {RADIUS} !important;
  margin-bottom: 6px !important;
  overflow: hidden !important;
}}
div[data-testid="stExpander"] details > summary p {{
  font-weight: 600 !important;
  color: {COLORS["ink"]} !important;
  font-size: 14px !important;
}}
div[data-testid="stExpander"] details > div {{
  color: {COLORS["muted"]} !important;
  line-height: 1.8 !important;
  font-size: 14px !important;
}}

/* ── Chat messages ────────────────────────── */
[data-testid="stChatMessage"] {{
  background: {COLORS["white"]} !important;
  border: 1px solid {COLORS["border"]} !important;
  border-radius: {RADIUS} !important;
  direction: rtl !important;
  margin-bottom: 8px !important;
}}

/* ── Tabs (Streamlit native override) ────── */
div[data-testid="stTabs"] {{ margin-top: 0 !important; }}
button[data-baseweb="tab"] {{
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: {COLORS["muted"]} !important;
  padding: 10px 18px !important;
  border-radius: 0 !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  color: {COLORS["primary"]} !important;
  font-weight: 700 !important;
  border-bottom: 2px solid {COLORS["teal"]} !important;
}}
div[role="tablist"] {{
  border-bottom: 1px solid {COLORS["border"]} !important;
  padding: 0 32px !important;
  background: {COLORS["white"]} !important;
  gap: 0 !important;
}}
div[data-testid="stTabs"] > div:nth-child(2) {{
  padding: 28px 32px 0 !important;
}}

/* ── Scrollbar ────────────────────────────── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-thumb {{ background: rgba(46,196,182,.3); border-radius: 4px; }}
</style>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
def render_header():
    """Header الموقع — الشعار فقط، التابات تحته من st.tabs"""
    st.markdown("""
<div style="
  background: #FFFFFF;
  border-bottom: 1px solid #E5E7EB;
  padding: 20px 32px 16px;
  text-align: center;
">
  <div style="
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #1B4F4A;
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 4px;
  ">بوصلة</div>
  <div style="
    font-size: 12px;
    color: #9CA3AF;
    font-weight: 500;
    letter-spacing: .5px;
  ">الدليل الذكي للتعليم العالي في دول مجلس التعاون الخليجي</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Section wrapper
# ─────────────────────────────────────────────
def section(overline: str = "", title: str = "", tight: bool = False):
    """يعرض overline + عنوان قسم"""
    mb = "margin-bottom:16px;" if tight else "margin-bottom:24px;"
    html = ""
    if overline:
        html += f'<div class="baw-overline">{overline}</div>'
    if title:
        html += f'<div class="baw-h1" style="{mb}">{title}</div>'
    if html:
        st.markdown(html, unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="baw-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Stat items (hero)
# ─────────────────────────────────────────────
def stat_bar(items: list):
    """
    items = [("80+", "جامعة"), ("6", "دولة"), ...]
    """
    cells = ""
    for i, (val, label) in enumerate(items):
        border = "border-left:1px solid #E5E7EB;" if i < len(items)-1 else ""
        cells += f"""
<div class="baw-stat-item" style="{border}">
  <div class="baw-stat-n">{val}</div>
  <div class="baw-stat-l">{label}</div>
</div>"""
    st.markdown(f'<div class="baw-stats-bar">{cells}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Feature card (used in home page grid)
# ─────────────────────────────────────────────
def feat_cards(cards: list):
    """
    cards = [
      {"num":"01","overline":"...","title":"...","body":"...","svg":"..."},
      ...
    ]
    """
    inner = ""
    for c in cards:
        inner += f"""
<div class="baw-feat-card">
  {c.get("svg","")}
  <span class="baw-feat-num">{c["num"]} — {c["overline"]}</span>
  <div class="baw-feat-title">{c["title"]}</div>
  <div class="baw-feat-body">{c["body"]}</div>
</div>"""
    st.markdown(f'<div class="baw-feat-grid">{inner}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Uni card
# ─────────────────────────────────────────────
def uni_card(name_ar, name_en, city, country, uni_type, scholarship, langs, website, admissions_url, uni_has_sch_fn):
    is_pub   = str(uni_type).strip().lower() in ["public", "حكومية"]
    type_tag = '<span class="baw-tag baw-tag-gov">حكومية</span>' if is_pub else '<span class="baw-tag baw-tag-priv">خاصة</span>'
    sch_tag  = '<span class="baw-tag baw-tag-sch">منحة</span>' if uni_has_sch_fn(str(scholarship)) else ""
    lang_html = "".join([f'<span class="baw-tag baw-tag-lang">{lg}</span>' for lg in langs[:2]])
    links = ""
    if str(website).strip():
        links += f'<a href="{website}" target="_blank" class="baw-uni-link">الموقع</a>'
    if str(admissions_url).strip():
        links += f'<a href="{admissions_url}" target="_blank" class="baw-uni-link">القبول</a>'

    st.markdown(f"""
<div class="baw-uni-card">
  <div>
    <div class="baw-uni-name">{name_ar}
      <span style="font-weight:400;color:#9CA3AF;font-size:11px;"> — {name_en}</span>
    </div>
    <div class="baw-uni-sub">{city}، {country}</div>
    <div class="baw-tags">{type_tag}{sch_tag}{lang_html}</div>
  </div>
  <div class="baw-uni-right">{links}</div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Comparison card
# ─────────────────────────────────────────────
def comp_card(row):
    sch  = str(row.get("scholarship","")).strip() or "—"
    rank = (str(row.get("ranking_source","")).strip() + " " +
            str(row.get("ranking_value","")).strip()).strip() or "—"
    return f"""
<div class="baw-comp-card">
  <div class="baw-comp-head">{row['name_ar']}</div>
  <div class="baw-comp-row">
    <span class="baw-comp-label">الدولة</span>
    <span class="baw-comp-val">{row['city']}، {row['country']}</span>
  </div>
  <div class="baw-comp-row">
    <span class="baw-comp-label">النوع</span>
    <span class="baw-comp-val">{row['type']}</span>
  </div>
  <div class="baw-comp-row">
    <span class="baw-comp-label">المنح</span>
    <span class="baw-comp-val">{sch}</span>
  </div>
  <div class="baw-comp-row">
    <span class="baw-comp-label">الترتيب</span>
    <span class="baw-comp-val">{rank}</span>
  </div>
</div>"""


# ─────────────────────────────────────────────
# AI result box
# ─────────────────────────────────────────────
def ai_box(label: str, content: str, variant: str = "primary"):
    css_class = "baw-ai-box" if variant == "primary" else "baw-gap-box"
    st.markdown(f"""
<div class="{css_class}">
  <span class="baw-ai-label">{label}</span>
  {content}
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Empty state
# ─────────────────────────────────────────────
def empty_state(icon: str, title: str, body: str):
    st.markdown(f"""
<div style="text-align:center;padding:52px 24px;color:#9CA3AF;">
  <div style="font-size:36px;margin-bottom:14px;">{icon}</div>
  <div style="font-size:15px;font-weight:700;color:#6B7280;margin-bottom:6px;">{title}</div>
  <div style="font-size:13px;">{body}</div>
</div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Stat metric card (data dashboard)
# ─────────────────────────────────────────────
def metric_card(value, label):
    st.markdown(f"""
<div style="background:#F0FAFA;border:1px solid rgba(46,196,182,.15);border-radius:12px;padding:16px;text-align:center;">
  <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#1B4F4A;">{value}</div>
  <div style="font-size:11px;color:#9CA3AF;margin-top:3px;">{label}</div>
</div>""", unsafe_allow_html=True)
