# -*- mode: python ; coding: utf-8 -*-
"""
bawsala.spec — ملف بناء PyInstaller لبوصلة
شغّليه بـ: pyinstaller bawsala.spec
"""
import sys
from pathlib import Path

block_cipher = None

# ─── جمع ملفات البيانات ─────────────────────────
added_files = [
    ("app.py",           "."),
    ("ui.py",            "."),
    ("components.py",    "."),
    ("ai_engine.py",     "."),
    ("llm.py",           "."),
    ("prompts.py",       "."),
    ("recommender.py",   "."),
    ("universities.csv", "."),
    ("programs.csv",     "."),
    ("config.toml",      "."),
    (".env",             "."),
]

# ─── Streamlit static files ──────────────────────
import streamlit
ST_PATH = Path(streamlit.__file__).parent
added_files += [
    (str(ST_PATH / "static"),   "streamlit/static"),
    (str(ST_PATH / "runtime"),  "streamlit/runtime"),
]

a = Analysis(
    ["launcher.py"],
    pathex=["."],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        "streamlit",
        "streamlit.web.cli",
        "streamlit.web.bootstrap",
        "streamlit.runtime.scriptrunner",
        "openai",
        "pandas",
        "plotly",
        "plotly.express",
        "plotly.graph_objects",
        "rank_bm25",
        "pydantic",
        "dotenv",
        "altair",
        "pyarrow",
        "tornado",
        "click",
        "rich",
        "validators",
        "tzdata",
        "charset_normalizer",
        "httpx",
        "anyio",
        "sniffio",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zlib, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="بوصلة",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,      # لا نافذة CMD
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,          # ضعي مسار أيقونة .ico هنا إن أردتِ
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="بوصلة",
)
