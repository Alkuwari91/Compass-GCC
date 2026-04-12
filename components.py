"""
components.py — Design System لبوصلة
"""
import streamlit as st

# ─── Design Tokens ────────────────────────────
C = {
    "primary":      "#1B4F4A",
    "teal":         "#2EC4B6",
    "teal_soft":    "rgba(46,196,182,.10)",
    "teal_border":  "rgba(46,196,182,.28)",
    "ink":          "#0F1923",
    "ink2":         "#374151",
    "muted":        "#6B7280",
    "pale":         "#F0FAFA",
    "white":        "#FFFFFF",
    "bg":           "#F8FAFB",
    "border":       "#E5E7EB",
    "border2":      "#D1D5DB",
    "gold":         "#92400E",
    "gold_bg":      "#FFFBEB",
    "gold_border":  "#FDE68A",
}

def inject_global_css():
    st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Reset ───────────────────────────────── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ── Base ────────────────────────────────── */
html, body, [class*="css"] {{
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  background: {C["bg"]} !important;
  color: {C["ink"]} !important;
  direction: rtl !important;
  font-size: 16px !important;
}}

/* ── Hide Streamlit chrome ───────────────── */
[data-testid="stSidebar"], [data-testid="stSidebarNav"],
button[kind="header"], [data-testid="collapsedControl"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
footer, #MainMenu {{ display: none !important; }}

[data-testid="stAppViewContainer"] {{ background: {C["bg"]} !important; }}
[data-testid="stMain"] {{ background: transparent !important; padding-top: 0 !important; }}

/* ── Page container ──────────────────────── */
[data-testid="stMainBlockContainer"] {{
  max-width: 980px !important;
  margin: 0 auto !important;
  padding: 0 0 80px !important;
  background: {C["white"]} !important;
  border-inline: 1px solid {C["border"]} !important;
  min-height: 100vh !important;
}}

/* ── RTL base ────────────────────────────── */
input, textarea, [role="textbox"] {{
  direction: rtl !important;
  text-align: right !important;
}}
div[data-baseweb="select"] * {{ direction: rtl !important; text-align: right !important; }}
label {{
  direction: rtl !important;
  text-align: right !important;
  color: {C["muted"]} !important;
  font-size: 15px !important;
  font-weight: 600 !important;
}}

/* ── Typography ──────────────────────────── */
.t-overline {{
  font-size: 17px;
  font-weight: 700;
  letter-spacing: .5px;
  color: {C["teal"]};
  display: block;
  text-align: center !important;
  margin-bottom: 10px;
  margin-top: 4px;
}}
.t-h1 {{
  font-family: 'Syne', sans-serif;
  font-size: 30px;
  font-weight: 800;
  color: {C["ink"]};
  letter-spacing: -.5px;
  line-height: 1.2;
  margin-bottom: 8px;
}}
.t-h2 {{
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: {C["ink"]};
  letter-spacing: -.3px;
  margin-bottom: 14px;
}}
.t-body {{
  font-size: 15px;
  color: {C["muted"]};
  line-height: 1.85;
}}
.t-small {{
  font-size: 13px;
  color: {C["muted"]};
  line-height: 1.7;
}}
.t-caption {{
  font-size: 12px;
  color: #9CA3AF;
}}
.baw-divider {{
  height: 1px;
  background: {C["border"]};
  margin: 40px 0;
  border: none;
}}

/* ── Chip / Badge ────────────────────────── */
.baw-chip {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: {C["teal_soft"]};
  border: 1px solid {C["teal_border"]};
  border-radius: 100px;
  padding: 5px 14px;
  font-size: 13px;
  font-weight: 700;
  color: {C["primary"]};
  margin-bottom: 16px;
}}

/* ── Feature grid ────────────────────────── */
.baw-feat-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-bottom: 44px;
  align-items: stretch;
}}
.baw-feat-card {{
  background: {C["white"]};
  border: 1px solid {C["border"]};
  border-radius: 14px;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  transition: border-color .18s, transform .18s, box-shadow .18s;
  height: 100%;
}}
.baw-feat-card:hover {{
  border-color: {C["teal"]};
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(46,196,182,.09);
}}
.baw-feat-num {{
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: {C["teal"]};
  margin-bottom: 16px;
  display: block;
  text-transform: uppercase;
}}
.baw-feat-title {{
  font-family: 'Syne', sans-serif;
  font-size: 18px;
  font-weight: 800;
  color: {C["ink"]};
  margin-bottom: 10px;
}}
.baw-feat-body {{
  font-size: 14px;
  color: {C["muted"]};
  line-height: 1.85;
  flex: 1;
}}

/* ── Uni cards ───────────────────────────── */
.baw-uni-card {{
  background: {C["white"]};
  border: 1px solid {C["border"]};
  border-radius: 14px;
  padding: 18px 22px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  transition: border-color .15s, box-shadow .15s;
}}
.baw-uni-card:hover {{
  border-color: {C["teal"]};
  box-shadow: 0 2px 12px rgba(46,196,182,.08);
}}
.baw-uni-name {{
  font-size: 15px;
  font-weight: 700;
  color: {C["ink"]};
  margin-bottom: 4px;
  line-height: 1.4;
}}
.baw-uni-en {{
  font-weight: 400;
  color: #9CA3AF;
  font-size: 13px;
}}
.baw-uni-sub {{ font-size: 13px; color: #9CA3AF; margin-bottom: 6px; }}
.baw-uni-right {{ display: flex; gap: 8px; flex-shrink: 0; align-items: center; }}
.baw-uni-link {{
  font-size: 13px;
  font-weight: 600;
  color: {C["teal"]};
  text-decoration: none;
  padding: 5px 12px;
  border: 1px solid {C["teal_border"]};
  border-radius: 8px;
  background: {C["teal_soft"]};
  white-space: nowrap;
  transition: all .15s;
}}
.baw-uni-link:hover {{ background: {C["teal"]}; color: #17252A; border-color: {C["teal"]}; }}

/* ── Tags ────────────────────────────────── */
.baw-tags {{ display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }}
.baw-tag {{
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}}
.baw-tag-gov  {{ background: rgba(46,196,182,.1); color: #1B4F4A; border: 1px solid rgba(46,196,182,.2); }}
.baw-tag-priv {{ background: #F3F4F6; color: #374151; border: 1px solid #E5E7EB; }}
.baw-tag-sch  {{ background: {C["gold_bg"]}; color: {C["gold"]}; border: 1px solid {C["gold_border"]}; }}
.baw-tag-lang {{ background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }}

/* ── Comparison cards ────────────────────── */
.baw-comp-card {{
  background: {C["white"]};
  border: 1px solid {C["border"]};
  border-radius: 14px;
  padding: 20px 18px;
  height: 100%;
}}
.baw-comp-head {{
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: {C["ink"]};
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid {C["border"]};
  line-height: 1.3;
}}
.baw-comp-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  padding: 9px 0;
  border-bottom: 1px solid #F9FAFB;
}}
.baw-comp-label {{ font-size: 13px; color: #9CA3AF; font-weight: 500; flex-shrink: 0; }}
.baw-comp-val   {{
  font-size: 13px;
  color: {C["ink"]};
  font-weight: 600;
  text-align: start;
  word-break: break-word;
}}

/* ── AI boxes ────────────────────────────── */
.baw-ai-box {{
  background: {C["pale"]};
  border: 1px solid {C["teal_border"]};
  border-radius: 14px;
  padding: 24px 26px;
  margin-top: 16px;
  line-height: 1.95;
  color: {C["ink"]};
  font-size: 15px;
}}
.baw-ai-label {{
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: {C["teal"]};
  margin-bottom: 12px;
  display: block;
}}
.baw-gap-box {{
  background: {C["gold_bg"]};
  border: 1px solid {C["gold_border"]};
  border-radius: 14px;
  padding: 24px 26px;
  margin-top: 16px;
  line-height: 1.95;
  color: {C["ink"]};
  font-size: 15px;
}}

/* ── Values grid ─────────────────────────── */
.baw-values-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 8px;
}}
.baw-val-card {{
  background: {C["pale"]};
  border-radius: 12px;
  padding: 20px 14px;
  text-align: center;
  border: 1px solid rgba(46,196,182,.15);
}}
.baw-val-title {{
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: {C["primary"]};
  margin-bottom: 6px;
}}
.baw-val-body {{ font-size: 13px; color: {C["muted"]}; }}

/* ── Stats bar ───────────────────────────── */
.baw-stats-bar {{
  display: flex;
  justify-content: center;
  border: 1px solid {C["border"]};
  border-radius: 14px;
  overflow: hidden;
  max-width: 520px;
  margin: 0 auto 44px;
}}
.baw-stat-item {{
  flex: 1;
  padding: 18px 12px;
  text-align: center;
}}
.baw-stat-item + .baw-stat-item {{ border-inline-start: 1px solid {C["border"]}; }}
.baw-stat-n {{
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 800;
  color: {C["ink"]};
  line-height: 1;
}}
.baw-stat-l {{ font-size: 12px; color: #9CA3AF; margin-top: 4px; font-weight: 500; }}

/* ── Metric card (dashboard) ─────────────── */
.baw-metric {{
  background: {C["pale"]};
  border: 1px solid rgba(46,196,182,.18);
  border-radius: 12px;
  padding: 18px 14px;
  text-align: center;
}}
.baw-metric-n {{
  font-family: 'Syne', sans-serif;
  font-size: 24px;
  font-weight: 800;
  color: {C["primary"]};
  line-height: 1;
  margin-bottom: 5px;
}}
.baw-metric-l {{ font-size: 13px; color: {C["muted"]}; font-weight: 500; }}

/* ── Section wrapper ─────────────────────── */
.baw-section {{
  padding-inline: 36px;
}}

/* ── Form inputs ─────────────────────────── */
.stTextInput > div > div {{
  background: {C["white"]} !important;
  border: 1.5px solid {C["border"]} !important;
  border-radius: 10px !important;
  font-size: 15px !important;
}}
.stTextInput > div > div:focus-within {{
  border-color: {C["teal"]} !important;
  box-shadow: 0 0 0 3px rgba(46,196,182,.10) !important;
}}
.stTextInput > div > div > input {{
  color: {C["ink"]} !important;
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  font-size: 15px !important;
}}
input::placeholder, textarea::placeholder {{
  color: #9CA3AF !important;
  opacity: 1 !important;
  font-size: 14px !important;
}}
.stTextArea > div > div {{
  background: {C["white"]} !important;
  border: 1.5px solid {C["border"]} !important;
  border-radius: 10px !important;
}}
.stTextArea > div > div > textarea {{
  color: {C["ink"]} !important;
  font-size: 15px !important;
}}

/* ── Selects ─────────────────────────────── */
div[data-baseweb="select"] > div {{
  background: {C["white"]} !important;
  border: 1.5px solid {C["border"]} !important;
  border-radius: 10px !important;
  color: {C["ink"]} !important;
  font-size: 14px !important;
}}
div[data-baseweb="select"] * {{ color: {C["ink"]} !important; font-size: 14px !important; }}
div[data-baseweb="popover"] li {{
  background: {C["white"]} !important;
  color: {C["ink"]} !important;
  font-size: 14px !important;
}}
div[data-baseweb="popover"] li:hover {{
  background: {C["pale"]} !important;
  color: {C["teal"]} !important;
}}

/* ── Buttons ─────────────────────────────── */
.stButton > button {{
  background: {C["white"]} !important;
  border: 1.5px solid {C["border2"]} !important;
  color: {C["ink2"]} !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  font-size: 14px !important;
  padding: 10px 20px !important;
  transition: all .15s !important;
}}
.stButton > button:hover {{
  background: {C["pale"]} !important;
  border-color: {C["teal"]} !important;
  color: {C["teal"]} !important;
}}
.stLinkButton a {{
  background: {C["teal_soft"]} !important;
  border: 1px solid {C["teal_border"]} !important;
  color: {C["primary"]} !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  padding: 6px 14px !important;
}}
.stLinkButton a:hover {{
  background: {C["teal"]} !important;
  color: #17252A !important;
}}

/* ══════════════════════════════════════════
   RTL TEXT ALIGNMENT — COMPREHENSIVE FIX
   يُصحح كل النصوص العربية داخل Streamlit
   ══════════════════════════════════════════ */

/* 1. كل الـ markdown containers — RTL right-aligned للفقرات */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] *,
.stMarkdown,
.stMarkdown * {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 2. الفقرات والنصوص في كل مكان */
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] li,
[data-testid="stMainBlockContainer"] span:not(.baw-tag):not(.baw-chip):not(.t-overline),
[data-testid="stMainBlockContainer"] div:not([class*="plot"]):not([class*="js-"]) > p {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 3. element-container wrapper */
.element-container,
.element-container > div {{
  direction: rtl !important;
}}

/* 4. نصوص داخل الـ tab panels — فقرات RTL */
div[data-testid="stTabsContent"] p,
div[data-testid="stTabsContent"] li,
div[data-testid="stTabsContent"] [data-testid="stMarkdownContainer"] p {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 5. النصوص داخل stVerticalBlock — فقرات RTL */
[data-testid="stVerticalBlock"] p,
[data-testid="stVerticalBlock"] [data-testid="stMarkdownContainer"] p,
[data-testid="stVerticalBlock"] [data-testid="stMarkdownContainer"] li {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 6. نصوص داخل columns — فقرات RTL */
[data-testid="column"] p,
[data-testid="column"] [data-testid="stMarkdownContainer"] p {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 7. chat messages */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 8. success / info / warning / error messages */
[data-testid="stAlert"] p,
[data-testid="stAlert"] {{
  direction: rtl !important;
  text-align: right !important;
}}

/* 9. captions */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
  direction: rtl !important;
  text-align: right !important;
}}

/* ══════════════════════════════════════════
   CENTERED HEADINGS — استثناءات العناوين
   تتغلب على قواعد RTL العامة أعلاه
   ══════════════════════════════════════════ */

/* العنوان الأخضر الصغير — centered دائماً */
.t-overline,
[data-testid="stMarkdownContainer"] .t-overline,
[data-testid="stVerticalBlock"] .t-overline {{
  text-align: center !important;
  direction: rtl !important;
}}

/* العنوان الكبير h1 — centered دائماً */
.t-h1,
[data-testid="stMarkdownContainer"] .t-h1,
[data-testid="stVerticalBlock"] .t-h1,
[data-testid="stTabsContent"] .t-h1 {{
  text-align: center !important;
  direction: rtl !important;
}}

/* العنوان المتوسط h2 — centered دائماً */
.t-h2,
[data-testid="stMarkdownContainer"] .t-h2,
[data-testid="stVerticalBlock"] .t-h2,
[data-testid="stTabsContent"] .t-h2 {{
  text-align: center !important;
  direction: rtl !important;
}}

/* ── Section wrapper: متوازن بصرياً ─────── */
.baw-section-wrap {{
  max-width: 680px;
  margin-inline: auto;
  padding-inline: 0;
}}

/* ── Headings inside stMarkdown: centered override ── */
[data-testid="stMarkdownContainer"] div.t-h1,
[data-testid="stMarkdownContainer"] div.t-h2,
[data-testid="stMarkdownContainer"] div.t-overline {{
  text-align: center !important;
}}

/* ── Expanders ───────────────────────────── */
div[data-testid="stExpander"] {{
  background: {C["white"]} !important;
  border: 1.5px solid {C["border"]} !important;
  border-radius: 12px !important;
  margin-bottom: 8px !important;
  overflow: hidden !important;
  direction: rtl !important;
}}
div[data-testid="stExpander"] details > summary,
div[data-testid="stExpander"] details > summary p {{
  font-weight: 700 !important;
  color: {C["ink"]} !important;
  font-size: 15px !important;
  direction: rtl !important;
  text-align: right !important;
}}
div[data-testid="stExpander"] details > div {{
  color: {C["muted"]} !important;
  line-height: 1.85 !important;
  font-size: 15px !important;
  padding: 4px 0 8px !important;
  direction: rtl !important;
  text-align: right !important;
}}
div[data-testid="stExpander"] details > div p,
div[data-testid="stExpander"] details > div li,
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"],
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li {{
  direction: rtl !important;
  text-align: right !important;
  color: {C["muted"]} !important;
  font-size: 15px !important;
  line-height: 1.85 !important;
}}

/* ── Chat ────────────────────────────────── */
[data-testid="stChatMessage"] {{
  background: {C["white"]} !important;
  border: 1px solid {C["border"]} !important;
  border-radius: 12px !important;
  direction: rtl !important;
  margin-bottom: 10px !important;
  font-size: 15px !important;
}}
[data-testid="stChatInput"] textarea {{
  font-size: 15px !important;
}}

/* ── Tabs ────────────────────────────────── */
div[data-testid="stTabs"] {{ margin-top: 0 !important; }}
div[role="tablist"] {{
  border-bottom: 2px solid {C["border"]} !important;
  padding: 0 36px !important;
  background: {C["white"]} !important;
  gap: 0 !important;
  direction: rtl !important;
}}
button[data-baseweb="tab"] {{
  font-family: 'IBM Plex Sans Arabic', sans-serif !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  color: {C["muted"]} !important;
  padding: 12px 20px !important;
  border-radius: 0 !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -2px !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
  color: {C["primary"]} !important;
  font-weight: 700 !important;
  border-bottom: 2px solid {C["teal"]} !important;
}}
div[data-testid="stTabs"] > div:nth-child(2) {{
  padding: 32px 36px 0 !important;
}}

/* ── Dataframe ───────────────────────────── */
[data-testid="stDataFrame"] {{
  border: 1px solid {C["border"]} !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  font-size: 14px !important;
}}

/* ── Scrollbar ───────────────────────────── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-thumb {{ background: rgba(46,196,182,.3); border-radius: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}

/* ── Plotly charts ───────────────────────── */
.js-plotly-plot .plotly {{ direction: ltr !important; }}
</style>""", unsafe_allow_html=True)


# ─── Components ───────────────────────────────

def render_header():
    st.markdown(f"""
<div style="
  background:{C['white']};
  border-bottom:2px solid {C['border']};
  padding:32px 36px 24px;
  text-align:center;
  direction:rtl;
  overflow:visible;
">
  <div style="
    font-family:'Syne',sans-serif;
    font-size:32px;
    font-weight:800;
    color:{C['primary']};
    letter-spacing:-1px;
    line-height:1.3;
    margin-bottom:8px;
    padding-top:4px;
  ">بوصلة</div>
  <div style="
    font-size:14px;
    color:{C['muted']};
    font-weight:500;
    letter-spacing:.3px;
    line-height:1.6;
  ">الدليل الذكي للتعليم العالي في دول مجلس التعاون الخليجي</div>
</div>
""", unsafe_allow_html=True)


def section_header(overline: str = "", title: str = "", subtitle: str = ""):
    """
    عنوان القسم — overline + title في المنتصف دائماً
    subtitle: right-aligned للعربية
    """
    parts = ""
    if overline:
        parts += f'<div class="t-overline">{overline}</div>'
    if title:
        parts += f'<div class="t-h1">{title}</div>'
    if subtitle:
        parts += f'<div class="t-body" style="text-align:right;margin-top:10px;">{subtitle}</div>'

    if parts:
        # wrapper خارجي يضمن التوسيط البصري الحقيقي
        # text-align:center يضمن توسيط الأبناء block
        # ثم كل عنصر عنده class خاص يُطبّق عليه CSS بتغلب على RTL العام
        st.markdown(f"""
<div style="
  text-align:center;
  direction:rtl;
  margin-bottom:24px;
  padding-inline:0;
">
  {parts}
</div>""", unsafe_allow_html=True)


def h2(text: str):
    st.markdown(f'<div class="t-h2" style="text-align:center;">{text}</div>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="baw-divider">', unsafe_allow_html=True)


def stat_bar(items: list):
    cells = ""
    for val, label in items:
        cells += f"""<div class="baw-stat-item">
  <div class="baw-stat-n">{val}</div>
  <div class="baw-stat-l">{label}</div>
</div>"""
    st.markdown(f'<div class="baw-stats-bar">{cells}</div>', unsafe_allow_html=True)


def feat_cards(cards: list):
    items = ""
    for c in cards:
        items += f"""<div class="baw-feat-card">
  {c.get('svg','')}
  <span class="baw-feat-num">{c['num']} — {c['overline']}</span>
  <div class="baw-feat-title">{c['title']}</div>
  <div class="baw-feat-body">{c['body']}</div>
</div>"""
    st.markdown(f'<div class="baw-feat-grid">{items}</div>', unsafe_allow_html=True)


def uni_card_html(name_ar, name_en, city, country, uni_type, scholarship,
                  langs, website, admissions_url, uni_has_sch_fn):
    is_pub   = str(uni_type).strip().lower() in ["public", "حكومية"]
    type_tag = '<span class="baw-tag baw-tag-gov">حكومية</span>' if is_pub else \
               '<span class="baw-tag baw-tag-priv">خاصة</span>'
    sch_tag  = '<span class="baw-tag baw-tag-sch">منحة</span>' \
               if uni_has_sch_fn(str(scholarship)) else ""
    lang_html = "".join(
        f'<span class="baw-tag baw-tag-lang">{lg}</span>'
        for lg in langs[:2]
    )
    links = ""
    if str(website).strip() and str(website).strip() not in ("nan",""):
        links += f'<a href="{website}" target="_blank" class="baw-uni-link">الموقع</a>'
    if str(admissions_url).strip() and str(admissions_url).strip() not in ("nan",""):
        links += f'<a href="{admissions_url}" target="_blank" class="baw-uni-link">القبول</a>'

    st.markdown(f"""<div class="baw-uni-card">
  <div style="flex:1;min-width:0;">
    <div class="baw-uni-name">{name_ar}
      <span class="baw-uni-en"> — {name_en}</span>
    </div>
    <div class="baw-uni-sub">{city}، {country}</div>
    <div class="baw-tags">{type_tag}{sch_tag}{lang_html}</div>
  </div>
  <div class="baw-uni-right">{links}</div>
</div>""", unsafe_allow_html=True)


def comp_card_html(row: dict) -> str:
    sch  = str(row.get("scholarship","")).strip()
    sch  = sch if sch and sch not in ("nan","Unknown","No","") else "—"
    rank_s = str(row.get("ranking_source","")).strip()
    rank_v = str(row.get("ranking_value","")).strip()
    rank = f"{rank_s} {rank_v}".strip() or "—"
    rank = rank if rank not in ("nan","nan nan") else "—"
    return f"""<div class="baw-comp-card">
  <div class="baw-comp-head">{row.get('name_ar','')}</div>
  <div class="baw-comp-row">
    <span class="baw-comp-label">الدولة</span>
    <span class="baw-comp-val">{row.get('city','')}، {row.get('country','')}</span>
  </div>
  <div class="baw-comp-row">
    <span class="baw-comp-label">النوع</span>
    <span class="baw-comp-val">{row.get('type','')}</span>
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


def ai_box(label: str, content: str, variant: str = "primary"):
    css = "baw-ai-box" if variant == "primary" else "baw-gap-box"
    st.markdown(f"""<div class="{css}">
  <span class="baw-ai-label">{label}</span>
  {content}
</div>""", unsafe_allow_html=True)


def empty_state(icon: str, title: str, body: str):
    st.markdown(f"""<div style="
  text-align:center;
  padding:56px 24px;
  color:#9CA3AF;
  direction:rtl;
">
  <div style="font-size:40px;margin-bottom:16px;">{icon}</div>
  <div style="font-size:17px;font-weight:700;color:#6B7280;margin-bottom:8px;">{title}</div>
  <div style="font-size:14px;">{body}</div>
</div>""", unsafe_allow_html=True)


def metric_card(value, label: str):
    st.markdown(f"""<div class="baw-metric">
  <div class="baw-metric-n">{value}</div>
  <div class="baw-metric-l">{label}</div>
</div>""", unsafe_allow_html=True)
