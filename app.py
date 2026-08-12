"""Bilingual main dashboard page for the Streamlit academic news board."""

from __future__ import annotations

import streamlit as st

from database import ALLOWED_SECTIONS, DatabaseError, count_news, initialize_database, list_news
from ui import (
    configure_page,
    format_created_at,
    mask_student_id,
    render_footer,
    render_top_navigation,
    safe_text,
    text,
)


configure_page("News Board")


@st.cache_data(ttl=15, show_spinner=False)
def get_news(section: str | None, keyword: str):
    """Cache short-lived reads; the add page clears this cache after writing."""

    return list_news(section=section, keyword=keyword)


@st.cache_data(ttl=15, show_spinner=False)
def get_stats() -> tuple[int, int]:
    return count_news()


def render_dashboard() -> None:
    language = render_top_navigation()

    hero_title = safe_text(text(language, "hero_title"))
    st.markdown(
        f"""
        <section class="hero">
            <div class="signal-chip"><span class="signal-dot"></span>{safe_text(text(language, 'hero_eyebrow'))}</div>
            <h1>{hero_title}</h1>
            <p>{safe_text(text(language, 'hero_intro'))}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if message_key := st.session_state.pop("save_success", None):
        st.success(text(language, str(message_key)), icon="✅")

    st.markdown(
        f"""
        <div class="section-heading">
            <div class="eyebrow">{safe_text(text(language, 'collection_eyebrow'))}</div>
            <h2>{safe_text(text(language, 'collection_title'))}</h2>
            <p>{safe_text(text(language, 'collection_intro'))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filter_column, search_column = st.columns([1, 2])
    all_sections_label = text(language, "all_sections")
    with filter_column:
        selected_label = st.selectbox(
            text(language, "filter_section"),
            (all_sections_label, *ALLOWED_SECTIONS),
            key=f"section_filter_{language}",
        )
    with search_column:
        keyword = st.text_input(
            text(language, "search_summary"),
            placeholder=text(language, "search_placeholder"),
            key=f"summary_search_{language}",
        )

    selected_section = None if selected_label == all_sections_label else selected_label

    try:
        total_count, represented_sections = get_stats()
        news_items = get_news(selected_section, keyword.strip())
    except DatabaseError:
        st.error(text(language, "database_error"), icon="⚠️")
        return

    total_column, result_column, section_column = st.columns(3)
    total_column.metric(text(language, "metric_all"), total_count)
    result_column.metric(text(language, "metric_found"), len(news_items))
    section_column.metric(text(language, "metric_sections"), represented_sections)

    if not news_items:
        empty_key = "empty_filtered" if total_count else "empty_all"
        st.info(text(language, empty_key))
    else:
        card_columns = st.columns(2)
        for index, item in enumerate(news_items):
            with card_columns[index % 2]:
                with st.container(border=True, key=f"news_card_{item.id}"):
                    st.markdown(
                        f'<span class="section-pill">{safe_text(item.section)}</span>',
                        unsafe_allow_html=True,
                    )
                    st.caption(
                        f"{text(language, 'student')} {mask_student_id(item.student_id)} · "
                        f"{format_created_at(item.created_at, language)}"
                    )
                    # st.write escapes user content; never render the summary as raw HTML.
                    st.write(item.news_summary)
                    st.link_button(
                        text(language, "read_source"),
                        item.source_uri,
                        key=f"source_link_{item.id}",
                        icon=":material/open_in_new:",
                        width="stretch",
                    )

    with st.container(key="floating_add_content"):
        if st.button(
            text(language, "add_content"),
            icon=":material/add:",
            type="primary",
            key="open_add_content",
        ):
            st.switch_page("pages/add_content.py")

    render_footer(language)


def main() -> None:
    try:
        initialize_database()
    except DatabaseError:
        st.error(text("en", "database_error"), icon="⚠️")
        st.stop()
    render_dashboard()


if __name__ == "__main__":
    main()
