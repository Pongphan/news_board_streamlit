"""Reusable presentation helpers for both Streamlit pages."""

from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone

import streamlit as st


APP_TITLE = "Campus News Board"


def configure_page(page_title: str) -> None:
    """Set shared metadata and inject the responsive visual system."""

    st.set_page_config(
        page_title=f"{page_title} · {APP_TITLE}",
        page_icon="📣",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        :root {
            --ink: #16233b;
            --muted: #62708a;
            --paper: #fbfcff;
            --line: #dfe6f1;
            --brand: #4f46e5;
            --brand-dark: #3730a3;
            --mint: #dff8ef;
            --amber: #fff1c7;
        }
        html, body, [class*="css"] {
            font-family: "Noto Sans Thai", "Leelawadee UI", Tahoma, sans-serif;
        }
        .stApp {
            background:
                radial-gradient(circle at 8% 3%, rgba(129, 140, 248, .14), transparent 24rem),
                radial-gradient(circle at 95% 18%, rgba(45, 212, 191, .10), transparent 22rem),
                var(--paper);
            color: var(--ink);
        }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] { display: none; }
        .block-container {
            max-width: 1120px;
            padding-top: 2.2rem;
            padding-bottom: 7rem;
        }
        .brand-row {
            display: flex;
            align-items: center;
            gap: .75rem;
            margin-bottom: 1.4rem;
            color: var(--ink);
            font-weight: 800;
            letter-spacing: -.01em;
        }
        .brand-mark {
            display: grid;
            place-items: center;
            width: 2.35rem;
            height: 2.35rem;
            border-radius: .85rem;
            color: white;
            background: linear-gradient(135deg, var(--brand), #7c3aed);
            box-shadow: 0 8px 22px rgba(79, 70, 229, .24);
        }
        .hero {
            position: relative;
            overflow: hidden;
            padding: clamp(2rem, 5vw, 4rem);
            border: 1px solid rgba(255, 255, 255, .5);
            border-radius: 2rem;
            color: white;
            background: linear-gradient(120deg, #172554 0%, #3730a3 52%, #5b21b6 100%);
            box-shadow: 0 24px 60px rgba(37, 42, 94, .18);
        }
        .hero::after {
            content: "";
            position: absolute;
            width: 18rem;
            height: 18rem;
            right: -5rem;
            top: -6rem;
            border-radius: 50%;
            background: rgba(255, 255, 255, .08);
            box-shadow: -10rem 15rem 0 rgba(45, 212, 191, .08);
        }
        .eyebrow {
            position: relative;
            z-index: 1;
            margin-bottom: .8rem;
            font-size: .76rem;
            font-weight: 800;
            letter-spacing: .15em;
            text-transform: uppercase;
            opacity: .78;
        }
        .hero h1 {
            position: relative;
            z-index: 1;
            max-width: 780px;
            margin: 0 0 1rem;
            font-size: clamp(2.2rem, 6vw, 4.7rem);
            line-height: 1.08;
            letter-spacing: -.055em;
        }
        .hero p {
            position: relative;
            z-index: 1;
            max-width: 680px;
            margin: 0;
            color: rgba(255, 255, 255, .78);
            font-size: 1.04rem;
            line-height: 1.75;
        }
        .section-heading { margin: 3.2rem 0 1.1rem; }
        .section-heading h2 {
            margin: .15rem 0;
            color: var(--ink);
            font-size: clamp(1.7rem, 4vw, 2.5rem);
            letter-spacing: -.035em;
        }
        .section-heading p { margin: 0; color: var(--muted); }
        [class*="st-key-news_card_"] {
            min-height: 100%;
            padding: .25rem;
        }
        [class*="st-key-news_card_"] [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line);
            border-radius: 1.25rem;
            background: rgba(255, 255, 255, .86);
            box-shadow: 0 10px 30px rgba(38, 51, 77, .06);
        }
        .section-pill {
            display: inline-flex;
            padding: .35rem .7rem;
            border-radius: 999px;
            color: var(--brand-dark);
            background: #eeecff;
            font-size: .76rem;
            font-weight: 800;
        }
        .news-meta { color: var(--muted); font-size: .82rem; }
        .form-shell {
            padding: 1.5rem 1.7rem;
            border: 1px solid var(--line);
            border-radius: 1.5rem;
            background: rgba(255, 255, 255, .9);
            box-shadow: 0 18px 50px rgba(38, 51, 77, .07);
        }
        .st-key-content_form_shell [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 1.5rem 1.7rem;
            border: 1px solid var(--line);
            border-radius: 1.5rem;
            background: rgba(255, 255, 255, .9);
            box-shadow: 0 18px 50px rgba(38, 51, 77, .07);
        }
        .form-intro {
            padding: 2rem;
            margin-bottom: 1.4rem;
            border-radius: 1.5rem;
            background: linear-gradient(135deg, #eef2ff, #f5f3ff 55%, #e6fffb);
            border: 1px solid #dcdffd;
        }
        .form-intro h1 {
            margin: .25rem 0 .6rem;
            color: var(--ink);
            font-size: clamp(2rem, 5vw, 3.35rem);
            letter-spacing: -.045em;
        }
        .form-intro p { margin: 0; color: var(--muted); line-height: 1.7; }
        .stButton > button, .stLinkButton > a {
            border-radius: .85rem;
            font-weight: 700;
        }
        .st-key-floating_add_content {
            position: fixed;
            left: 1.35rem;
            bottom: 1.35rem;
            z-index: 999;
            width: auto;
            padding: .35rem;
            border-radius: 1.05rem;
            background: rgba(255, 255, 255, .9);
            box-shadow: 0 14px 36px rgba(27, 34, 73, .24);
            backdrop-filter: blur(12px);
        }
        .st-key-floating_add_content button {
            min-height: 3.2rem;
            padding-inline: 1.15rem;
            border: 0;
            color: white;
            background: linear-gradient(135deg, var(--brand), #7c3aed);
        }
        .footer {
            margin-top: 3.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: .82rem;
        }
        @media (max-width: 640px) {
            .block-container { padding: 1rem .9rem 6.5rem; }
            .hero { padding: 2rem 1.35rem; border-radius: 1.45rem; }
            .st-key-floating_add_content { left: 1rem; bottom: 1rem; }
            .st-key-content_form_shell [data-testid="stVerticalBlockBorderWrapper"] {
                padding: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand() -> None:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-mark">✦</div>
            <div>Campus News Board</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_text(value: str) -> str:
    return html.escape(value, quote=True)


def mask_student_id(student_id: str) -> str:
    """Avoid exposing the full student ID on the public dashboard."""

    if len(student_id) <= 4:
        return "•" * len(student_id)
    return f"{student_id[:2]}{'•' * max(3, len(student_id) - 4)}{student_id[-2:]}"


def format_created_at(value: str) -> str:
    """Display the stored UTC timestamp in Thailand time (UTC+7)."""

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        thailand_time = parsed.astimezone(timezone(timedelta(hours=7)))
        return thailand_time.strftime("%d/%m/%Y · %H:%M น.")
    except (TypeError, ValueError):
        return "ไม่ทราบเวลา"


def render_footer() -> None:
    st.markdown(
        '<div class="footer">Campus News Board · ข่าวทุกชิ้นเชื่อมโยงกลับไปยังแหล่งข้อมูลต้นทาง</div>',
        unsafe_allow_html=True,
    )
