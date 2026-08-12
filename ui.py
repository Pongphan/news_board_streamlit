"""Shared localization and presentation helpers for both Streamlit pages."""

from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone

import streamlit as st


APP_TITLE = "Academic News Board"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "brand_name": "Academic News Board",
        "brand_tagline": "Source-based student briefings",
        "language": "Language",
        "hero_eyebrow": "Academic intelligence · Curated by students",
        "hero_title": "Concise insight.\nVerifiable sources.",
        "hero_intro": (
            "A structured collection of student-curated news, organized by section "
            "and linked to original sources for further academic review."
        ),
        "collection_eyebrow": "Knowledge stream",
        "collection_title": "Latest briefings",
        "collection_intro": "Search or filter concise, source-linked submissions.",
        "filter_section": "Section",
        "all_sections": "All sections",
        "search_summary": "Search summaries",
        "search_placeholder": "Search by topic or keyword",
        "metric_all": "Total briefings",
        "metric_found": "Results",
        "metric_sections": "Active sections",
        "empty_filtered": "No briefings match the selected criteria.",
        "empty_all": "No briefings have been published. Add the first entry below.",
        "student": "Student",
        "read_source": "Open source",
        "add_content": "Add content",
        "content_saved": "Content saved. The board is now up to date.",
        "database_error": "The data service is temporarily unavailable. Please try again.",
        "back_dashboard": "Back to news board",
        "form_eyebrow": "Contribute to the knowledge base",
        "form_title": "Add a briefing",
        "form_intro": (
            "Provide a concise academic summary and a verifiable source. "
            "The entry will appear on the board immediately after validation."
        ),
        "section": "Section",
        "section_help": "Select the contributor's course section.",
        "student_id": "Student ID",
        "student_placeholder": "e.g. 6612345678",
        "student_help": "Use 4–20 letters, numbers, underscores, or hyphens.",
        "news_summary": "News Summary",
        "summary_placeholder": "Summarize the central finding, relevance, or implication (10–2,000 characters).",
        "source_uri": "Source URI",
        "source_placeholder": "https://example.org/article",
        "source_help": "Only HTTP and HTTPS links are accepted.",
        "save": "Save",
        "form_invalid": "Review the following information before saving:",
        "invalid_section": "Select a valid section.",
        "invalid_student_id": "Student ID must contain 4–20 letters, numbers, underscores, or hyphens.",
        "summary_too_short": "The news summary must contain at least 10 characters.",
        "summary_too_long": "The news summary must not exceed 2,000 characters.",
        "invalid_source_uri": "Enter a valid URL beginning with http:// or https://.",
        "unknown_time": "Time unavailable",
        "footer": "Academic News Board · Every briefing links to its original source.",
    },
    "th": {
        "brand_name": "บอร์ดข่าววิชาการ",
        "brand_tagline": "บทสรุปโดยนักศึกษาที่ตรวจสอบแหล่งที่มาได้",
        "language": "ภาษา",
        "hero_eyebrow": "สารสนเทศวิชาการ · คัดสรรโดยนักศึกษา",
        "hero_title": "สาระกระชับ\nแหล่งข้อมูลตรวจสอบได้",
        "hero_intro": (
            "คลังข่าวที่นักศึกษาคัดสรรอย่างเป็นระบบ แบ่งตาม Section "
            "และเชื่อมโยงแหล่งข้อมูลต้นทางเพื่อการศึกษาต่อ"
        ),
        "collection_eyebrow": "คลังองค์ความรู้",
        "collection_title": "บทสรุปล่าสุด",
        "collection_intro": "ค้นหาหรือกรองบทสรุปที่เชื่อมโยงแหล่งข้อมูลต้นทาง",
        "filter_section": "Section",
        "all_sections": "ทุก Section",
        "search_summary": "ค้นหาในบทสรุป",
        "search_placeholder": "ค้นหาตามหัวข้อหรือคำสำคัญ",
        "metric_all": "บทสรุปทั้งหมด",
        "metric_found": "ผลลัพธ์",
        "metric_sections": "Section ที่มีข้อมูล",
        "empty_filtered": "ไม่พบบทสรุปที่ตรงกับเงื่อนไข",
        "empty_all": "ยังไม่มีบทสรุปในระบบ เพิ่มรายการแรกได้จากปุ่มด้านล่าง",
        "student": "นักศึกษา",
        "read_source": "เปิดแหล่งข้อมูล",
        "add_content": "เพิ่มเนื้อหา",
        "content_saved": "บันทึกเนื้อหาแล้ว และปรับปรุงบอร์ดให้เป็นปัจจุบันเรียบร้อย",
        "database_error": "ระบบข้อมูลไม่พร้อมใช้งานชั่วคราว กรุณาลองอีกครั้ง",
        "back_dashboard": "กลับสู่บอร์ดข่าว",
        "form_eyebrow": "ร่วมพัฒนาคลังองค์ความรู้",
        "form_title": "เพิ่มบทสรุปข่าว",
        "form_intro": (
            "จัดทำบทสรุปเชิงวิชาการอย่างกระชับ พร้อมระบุแหล่งข้อมูลที่ตรวจสอบได้ "
            "รายการจะแสดงบนบอร์ดทันทีหลังผ่านการตรวจสอบ"
        ),
        "section": "Section",
        "section_help": "เลือก Section ของผู้ส่งข้อมูล",
        "student_id": "รหัสนักศึกษา",
        "student_placeholder": "ตัวอย่าง 6612345678",
        "student_help": "ใช้ตัวอักษร ตัวเลข _ หรือ - จำนวน 4–20 ตัว",
        "news_summary": "บทสรุปข่าว",
        "summary_placeholder": "สรุปข้อค้นพบ ความสำคัญ หรือผลกระทบหลัก (10–2,000 ตัวอักษร)",
        "source_uri": "แหล่งข้อมูลต้นทาง",
        "source_placeholder": "https://example.org/article",
        "source_help": "รองรับเฉพาะลิงก์ HTTP และ HTTPS",
        "save": "บันทึก",
        "form_invalid": "กรุณาตรวจสอบข้อมูลต่อไปนี้ก่อนบันทึก:",
        "invalid_section": "กรุณาเลือก Section ที่ถูกต้อง",
        "invalid_student_id": "รหัสนักศึกษาต้องมี 4–20 ตัว และใช้ได้เฉพาะตัวอักษร ตัวเลข _ หรือ -",
        "summary_too_short": "บทสรุปข่าวต้องมีอย่างน้อย 10 ตัวอักษร",
        "summary_too_long": "บทสรุปข่าวต้องไม่เกิน 2,000 ตัวอักษร",
        "invalid_source_uri": "กรุณากรอก URL ที่ขึ้นต้นด้วย http:// หรือ https://",
        "unknown_time": "ไม่ทราบเวลา",
        "footer": "บอร์ดข่าววิชาการ · ทุกบทสรุปเชื่อมโยงแหล่งข้อมูลต้นทาง",
    },
}


def text(language: str, key: str) -> str:
    """Return localized copy, falling back to English for missing keys."""

    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))


def configure_page(page_title: str) -> None:
    """Set metadata and inject a responsive pastel glass-tech visual system."""

    st.set_page_config(
        page_title=f"{page_title} · {APP_TITLE}",
        page_icon="📡",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light;
            --ink: #25314a;
            --muted: #67738d;
            --canvas: #f8f7ff;
            --glass: rgba(255, 255, 255, .66);
            --glass-strong: rgba(255, 255, 255, .82);
            --line: rgba(89, 94, 148, .17);
            --brand: #7168df;
            --brand-strong: #554cc4;
            --aqua: #79cfd0;
            --mint: #bfe8d7;
            --lavender: #d8d2ff;
            --shadow: 0 22px 55px rgba(67, 66, 124, .12);
            --grid: rgba(106, 100, 178, .055);
            --hero-a: rgba(243, 239, 255, .88);
            --hero-b: rgba(223, 248, 244, .74);
        }
        @media (prefers-color-scheme: dark) {
            :root {
                color-scheme: dark;
                --ink: #eef1ff;
                --muted: #aab4cc;
                --canvas: #11131e;
                --glass: rgba(28, 32, 48, .66);
                --glass-strong: rgba(31, 35, 54, .84);
                --line: rgba(196, 202, 239, .15);
                --brand: #aca4ff;
                --brand-strong: #c7c2ff;
                --aqua: #72d4d1;
                --mint: #75c5aa;
                --lavender: #8f87dc;
                --shadow: 0 24px 60px rgba(0, 0, 0, .28);
                --grid: rgba(180, 175, 255, .045);
                --hero-a: rgba(42, 39, 73, .80);
                --hero-b: rgba(24, 54, 59, .68);
            }
        }
        html, body, [class*="css"] {
            font-family: "Noto Sans Thai", "Leelawadee UI", Inter, system-ui, sans-serif;
        }
        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 8% 0%, rgba(182, 171, 255, .25), transparent 29rem),
                radial-gradient(circle at 96% 15%, rgba(121, 207, 208, .20), transparent 27rem),
                var(--canvas);
        }
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                linear-gradient(var(--grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid) 1px, transparent 1px);
            background-size: 32px 32px;
            mask-image: linear-gradient(to bottom, black, transparent 82%);
        }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebar"] { display: none; }
        .block-container {
            position: relative;
            z-index: 1;
            max-width: 1180px;
            padding-top: 1.35rem;
            padding-bottom: 7rem;
        }
        .st-key-top_navigation {
            padding: .62rem .72rem;
            margin-bottom: 1.1rem;
            border: 1px solid var(--line);
            border-radius: 1.15rem;
            background: var(--glass);
            box-shadow: 0 12px 32px rgba(55, 58, 104, .07);
            backdrop-filter: blur(20px) saturate(135%);
            -webkit-backdrop-filter: blur(20px) saturate(135%);
        }
        .brand-lockup {
            display: flex;
            align-items: center;
            gap: .72rem;
            min-height: 2.55rem;
        }
        .brand-mark {
            display: grid;
            place-items: center;
            width: 2.45rem;
            height: 2.45rem;
            flex: 0 0 auto;
            border: 1px solid rgba(255, 255, 255, .42);
            border-radius: .85rem;
            color: #ffffff;
            background: linear-gradient(135deg, var(--brand), var(--aqua));
            box-shadow: 0 9px 24px rgba(91, 82, 201, .22);
        }
        .brand-name {
            color: var(--ink);
            font-size: .96rem;
            font-weight: 800;
            letter-spacing: -.015em;
        }
        .brand-tagline { color: var(--muted); font-size: .72rem; }
        .st-key-language_switcher [data-testid="stSegmentedControl"] { justify-content: flex-end; }
        .st-key-language_switcher button { min-height: 2.35rem; font-weight: 800; }
        .hero {
            position: relative;
            isolation: isolate;
            overflow: hidden;
            min-height: 410px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: clamp(2rem, 6vw, 4.8rem);
            border: 1px solid var(--line);
            border-radius: 2rem;
            color: var(--ink);
            background: linear-gradient(125deg, var(--hero-a), var(--hero-b));
            box-shadow: var(--shadow);
            backdrop-filter: blur(24px) saturate(125%);
            -webkit-backdrop-filter: blur(24px) saturate(125%);
        }
        .hero::before {
            content: "";
            position: absolute;
            z-index: -1;
            inset: 0;
            opacity: .52;
            background-image:
                linear-gradient(90deg, transparent 79px, var(--line) 80px),
                linear-gradient(transparent 79px, var(--line) 80px);
            background-size: 80px 80px;
            mask-image: linear-gradient(90deg, transparent 30%, black);
        }
        .hero::after {
            content: "";
            position: absolute;
            z-index: -1;
            width: 22rem;
            height: 22rem;
            right: -5rem;
            top: -7rem;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(170, 159, 255, .46), rgba(109, 217, 202, .26));
            filter: blur(2px);
            box-shadow: -8rem 21rem 0 -4rem rgba(121, 207, 208, .16);
        }
        .signal-chip {
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            align-self: flex-start;
            gap: .42rem;
            padding: .36rem .66rem;
            margin-bottom: 1rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            color: var(--brand-strong);
            background: var(--glass);
            font-size: .68rem;
            font-weight: 850;
            letter-spacing: .12em;
            text-transform: uppercase;
        }
        .signal-dot {
            width: .45rem;
            height: .45rem;
            border-radius: 50%;
            background: var(--aqua);
            box-shadow: 0 0 0 .24rem rgba(121, 207, 208, .14);
        }
        .eyebrow {
            margin-bottom: .45rem;
            color: var(--brand-strong);
            font-size: .71rem;
            font-weight: 850;
            letter-spacing: .14em;
            text-transform: uppercase;
        }
        .hero h1 {
            position: relative;
            z-index: 1;
            max-width: 800px;
            margin: 0 0 1.15rem;
            color: var(--ink);
            font-size: clamp(2.55rem, 7vw, 5.4rem);
            line-height: 1.02;
            letter-spacing: -.065em;
            white-space: pre-line;
        }
        .hero p {
            position: relative;
            z-index: 1;
            max-width: 670px;
            margin: 0;
            color: var(--muted);
            font-size: clamp(.96rem, 2vw, 1.08rem);
            line-height: 1.72;
        }
        .section-heading { margin: 3.4rem 0 1.15rem; }
        .section-heading h2 {
            margin: .05rem 0 .22rem;
            color: var(--ink);
            font-size: clamp(1.85rem, 4vw, 2.7rem);
            letter-spacing: -.045em;
        }
        .section-heading p { margin: 0; color: var(--muted); }
        [data-testid="stMetric"] {
            padding: 1rem 1.1rem;
            border: 1px solid var(--line);
            border-radius: 1.1rem;
            background: var(--glass);
            box-shadow: 0 10px 28px rgba(50, 54, 99, .06);
            backdrop-filter: blur(16px);
        }
        [class*="st-key-news_card_"] { min-height: 100%; padding: .18rem; }
        [class*="st-key-news_card_"] [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line);
            border-radius: 1.3rem;
            background: var(--glass);
            box-shadow: 0 14px 36px rgba(46, 51, 94, .075);
            backdrop-filter: blur(18px) saturate(125%);
            transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
        }
        [class*="st-key-news_card_"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-2px);
            border-color: rgba(122, 111, 240, .34);
            box-shadow: 0 20px 42px rgba(55, 57, 108, .12);
        }
        .section-pill {
            display: inline-flex;
            padding: .34rem .68rem;
            border: 1px solid rgba(113, 104, 223, .15);
            border-radius: 999px;
            color: var(--brand-strong);
            background: rgba(183, 174, 255, .20);
            font-size: .73rem;
            font-weight: 850;
        }
        .form-intro {
            position: relative;
            overflow: hidden;
            padding: clamp(1.6rem, 5vw, 3rem);
            margin: .9rem 0 1.25rem;
            border: 1px solid var(--line);
            border-radius: 1.55rem;
            background: linear-gradient(135deg, var(--hero-a), var(--hero-b));
            box-shadow: var(--shadow);
            backdrop-filter: blur(20px);
        }
        .form-intro::after {
            content: "";
            position: absolute;
            width: 12rem;
            height: 12rem;
            right: -3rem;
            top: -5rem;
            border-radius: 50%;
            background: rgba(169, 157, 255, .22);
        }
        .form-intro h1 {
            position: relative;
            z-index: 1;
            margin: .15rem 0 .55rem;
            color: var(--ink);
            font-size: clamp(2.1rem, 5vw, 3.6rem);
            letter-spacing: -.055em;
        }
        .form-intro p { position: relative; z-index: 1; max-width: 720px; margin: 0; color: var(--muted); line-height: 1.7; }
        .st-key-content_form_shell [data-testid="stVerticalBlockBorderWrapper"] {
            padding: clamp(1rem, 4vw, 1.8rem);
            border: 1px solid var(--line);
            border-radius: 1.5rem;
            background: var(--glass);
            box-shadow: 0 18px 48px rgba(42, 47, 89, .08);
            backdrop-filter: blur(20px) saturate(125%);
        }
        .stButton > button, .stLinkButton > a { border-radius: .82rem; font-weight: 750; }
        .st-key-floating_add_content {
            position: fixed;
            left: max(1rem, calc((100vw - 1180px) / 2));
            bottom: 1.2rem;
            z-index: 999;
            width: auto;
            padding: .35rem;
            border: 1px solid var(--line);
            border-radius: 1.08rem;
            background: var(--glass-strong);
            box-shadow: 0 16px 40px rgba(27, 31, 68, .22);
            backdrop-filter: blur(20px) saturate(140%);
        }
        .st-key-floating_add_content button {
            min-height: 3.15rem;
            padding-inline: 1.15rem;
            border: 0;
            color: #ffffff;
            background: linear-gradient(135deg, #7168df, #777fdc 52%, #64bfc1);
        }
        .footer {
            margin-top: 3.6rem;
            padding-top: 1.2rem;
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: .8rem;
        }
        @media (max-width: 720px) {
            .block-container { padding: .75rem .8rem 6.5rem; }
            .st-key-top_navigation { padding: .45rem .5rem; border-radius: 1rem; }
            .st-key-top_navigation [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; gap: .35rem; }
            .st-key-top_navigation [data-testid="stColumn"]:first-child { width: 66%; flex: 1 1 66%; }
            .st-key-top_navigation [data-testid="stColumn"]:last-child { width: 34%; flex: 0 0 34%; }
            .brand-mark { width: 2.15rem; height: 2.15rem; border-radius: .72rem; }
            .brand-name { font-size: .84rem; }
            .brand-tagline { display: none; }
            .st-key-language_switcher button { min-height: 2.1rem; padding-inline: .52rem; }
            .hero { min-height: 360px; padding: 2rem 1.3rem; border-radius: 1.45rem; }
            .hero h1 { font-size: clamp(2.45rem, 13vw, 3.7rem); }
            .hero::before { background-size: 56px 56px; }
            .section-heading { margin-top: 2.5rem; }
            .st-key-floating_add_content { left: .9rem; bottom: .85rem; }
        }
        @media (max-width: 420px) {
            .brand-name { max-width: 9.5rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .hero { min-height: 335px; }
            .signal-chip { font-size: .58rem; letter-spacing: .09em; }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def current_language() -> str:
    return str(st.session_state.get("ui_language", "EN")).lower()


def render_top_navigation() -> str:
    """Render the glass navigation bar and persistent EN/TH control."""

    language = current_language()
    with st.container(key="top_navigation"):
        brand_column, language_column = st.columns([4.4, 1], vertical_alignment="center")
        with brand_column:
            st.markdown(
                f"""
                <div class="brand-lockup">
                    <div class="brand-mark">⌁</div>
                    <div>
                        <div class="brand-name">{safe_text(text(language, 'brand_name'))}</div>
                        <div class="brand-tagline">{safe_text(text(language, 'brand_tagline'))}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with language_column:
            with st.container(key="language_switcher"):
                selected = st.segmented_control(
                    text(language, "language"),
                    options=("EN", "TH"),
                    default="EN",
                    key="ui_language",
                    label_visibility="collapsed",
                    persist_state="session",
                )
    return str(selected or "EN").lower()


def safe_text(value: str) -> str:
    return html.escape(value, quote=True)


def mask_student_id(student_id: str) -> str:
    """Avoid exposing the full student ID on the public dashboard."""

    if len(student_id) <= 4:
        return "•" * len(student_id)
    return f"{student_id[:2]}{'•' * max(3, len(student_id) - 4)}{student_id[-2:]}"


def format_created_at(value: str, language: str) -> str:
    """Display the stored UTC timestamp in Thailand time (UTC+7)."""

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        thailand_time = parsed.astimezone(timezone(timedelta(hours=7)))
        if language == "th":
            return thailand_time.strftime("%d/%m/%Y · %H:%M น.")
        return thailand_time.strftime("%d %b %Y · %H:%M ICT")
    except (TypeError, ValueError):
        return text(language, "unknown_time")


def render_footer(language: str) -> None:
    st.markdown(
        f'<div class="footer">{safe_text(text(language, "footer"))}</div>',
        unsafe_allow_html=True,
    )
