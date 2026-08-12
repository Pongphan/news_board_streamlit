"""Bilingual add-content form page."""

from __future__ import annotations

import streamlit as st

from database import ALLOWED_SECTIONS, DatabaseError, create_news, initialize_database
from ui import configure_page, render_footer, render_top_navigation, safe_text, text
from validation import validate_news


configure_page("Add Content")


def render_form() -> None:
    language = render_top_navigation()

    if st.button(text(language, "back_dashboard"), icon=":material/arrow_back:"):
        st.switch_page("app.py")

    st.markdown(
        f"""
        <section class="form-intro">
            <div class="eyebrow">{safe_text(text(language, 'form_eyebrow'))}</div>
            <h1>{safe_text(text(language, 'form_title'))}</h1>
            <p>{safe_text(text(language, 'form_intro'))}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="content_form_shell"):
        with st.form("add_content_form", clear_on_submit=False):
            section = st.selectbox(
                f"{text(language, 'section')} *",
                ALLOWED_SECTIONS,
                key="form_section",
                help=text(language, "section_help"),
            )
            student_id = st.text_input(
                f"{text(language, 'student_id')} *",
                placeholder=text(language, "student_placeholder"),
                max_chars=20,
                key="form_student_id",
                help=text(language, "student_help"),
            )
            news_summary = st.text_area(
                f"{text(language, 'news_summary')} *",
                placeholder=text(language, "summary_placeholder"),
                height=190,
                max_chars=2000,
                key="form_news_summary",
            )
            source_uri = st.text_input(
                f"{text(language, 'source_uri')} *",
                placeholder=text(language, "source_placeholder"),
                key="form_source_uri",
                help=text(language, "source_help"),
            )
            submitted = st.form_submit_button(
                text(language, "save"),
                icon=":material/save:",
                type="primary",
                width="stretch",
            )

    if not submitted:
        render_footer(language)
        return

    errors, cleaned = validate_news(section, student_id, news_summary, source_uri)
    if errors:
        st.error(text(language, "form_invalid"), icon="⚠️")
        for message_key in errors.values():
            st.write(f"- {text(language, message_key)}")
        render_footer(language)
        return

    try:
        create_news(**cleaned)
    except DatabaseError:
        st.error(text(language, "database_error"), icon="⚠️")
        render_footer(language)
        return

    st.cache_data.clear()
    st.session_state["save_success"] = "content_saved"
    st.switch_page("app.py")


def main() -> None:
    try:
        initialize_database()
    except DatabaseError:
        st.error(text("en", "database_error"), icon="⚠️")
        st.stop()
    render_form()


if __name__ == "__main__":
    main()
