"""Authenticated administrative review and moderation page."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from admin_auth import (
    is_admin_authenticated,
    sign_in_admin,
    sign_out_admin,
    verify_admin_password,
)
from admin_export import news_to_csv
from database import (
    ALLOWED_SECTIONS,
    DatabaseError,
    count_news_by_status,
    delete_news,
    initialize_database,
    list_news_for_admin,
    update_news_status,
)
from ui import configure_page, format_created_at, render_footer, render_top_navigation, safe_text, text


configure_page("Admin")


def render_login(language: str) -> None:
    st.markdown(
        f"""
        <section class="admin-login">
            <div class="eyebrow">{safe_text(text(language, 'admin_login_eyebrow'))}</div>
            <h1>{safe_text(text(language, 'admin_login_title'))}</h1>
            <p>{safe_text(text(language, 'admin_login_intro'))}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    with st.form("admin_login_form", clear_on_submit=True):
        password = st.text_input(
            text(language, "admin_password"),
            type="password",
            placeholder=text(language, "admin_password_placeholder"),
            key="admin_password",
        )
        submitted = st.form_submit_button(
            text(language, "admin_sign_in"),
            icon=":material/login:",
            type="primary",
            width="stretch",
        )
    if submitted:
        if verify_admin_password(password):
            sign_in_admin()
            st.rerun()
        else:
            st.error(text(language, "admin_invalid_password"), icon="⚠️")


def apply_action(news_id: int, action: str, language: str) -> None:
    """Apply one authenticated moderation action and rerun with a notice."""

    try:
        if action == "hide":
            changed = update_news_status(news_id, "hidden")
            notice_key = "item_hidden"
        elif action == "restore":
            changed = update_news_status(news_id, "published")
            notice_key = "item_restored"
        elif action == "delete":
            changed = delete_news(news_id)
            notice_key = "item_deleted"
        else:
            return
    except DatabaseError:
        st.error(text(language, "database_error"), icon="⚠️")
        return

    if not changed:
        st.error(text(language, "action_failed"), icon="⚠️")
        return

    st.cache_data.clear()
    st.session_state.pop("confirm_delete_id", None)
    st.session_state["admin_notice"] = notice_key
    st.rerun()


def render_admin_workspace(language: str) -> None:
    title_column, logout_column = st.columns([5, 1], vertical_alignment="bottom")
    with title_column:
        st.markdown(
            f"""
            <section class="admin-header">
                <div class="eyebrow">{safe_text(text(language, 'admin_eyebrow'))}</div>
                <h1>{safe_text(text(language, 'admin_title'))}</h1>
                <p>{safe_text(text(language, 'admin_intro'))}</p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with logout_column:
        if st.button(
            text(language, "admin_logout"),
            icon=":material/logout:",
            key="admin_logout",
            width="stretch",
        ):
            sign_out_admin()
            st.rerun()

    if notice_key := st.session_state.pop("admin_notice", None):
        st.success(text(language, str(notice_key)), icon="✅")

    status_labels = {
        text(language, "all_statuses"): None,
        text(language, "status_published"): "published",
        text(language, "status_hidden"): "hidden",
    }
    section_column, status_column, search_column = st.columns([1, 1, 2])
    with section_column:
        all_sections_label = text(language, "all_sections")
        selected_section_label = st.selectbox(
            text(language, "filter_section"),
            (all_sections_label, *ALLOWED_SECTIONS),
            key=f"admin_section_{language}",
        )
    with status_column:
        selected_status_label = st.selectbox(
            text(language, "filter_status"),
            tuple(status_labels),
            key=f"admin_status_{language}",
        )
    with search_column:
        keyword = st.text_input(
            text(language, "admin_search"),
            placeholder=text(language, "admin_search_placeholder"),
            key=f"admin_search_{language}",
        )

    section = None if selected_section_label == all_sections_label else selected_section_label
    status = status_labels[selected_status_label]
    try:
        total, published, hidden = count_news_by_status()
        records = list_news_for_admin(section=section, status=status, keyword=keyword)
    except DatabaseError:
        st.error(text(language, "database_error"), icon="⚠️")
        return

    total_column, published_column, hidden_column = st.columns(3)
    total_column.metric(text(language, "admin_metric_total"), total)
    published_column.metric(text(language, "admin_metric_published"), published)
    hidden_column.metric(text(language, "admin_metric_hidden"), hidden)

    st.download_button(
        text(language, "download_csv"),
        data=news_to_csv(records),
        file_name=f"news-board-{datetime.now().strftime('%Y%m%d-%H%M')}.csv",
        mime="text/csv",
        icon=":material/download:",
        key="download_admin_csv",
    )

    if not records:
        st.info(text(language, "admin_empty"))
        render_footer(language)
        return

    for item in records:
        with st.container(border=True, key=f"admin_record_{item.id}"):
            status_key = f"status_{item.status}"
            st.markdown(
                f"""
                <span class="section-pill">{safe_text(item.section)}</span>
                <span class="status-pill status-{safe_text(item.status)}">{safe_text(text(language, status_key))}</span>
                """,
                unsafe_allow_html=True,
            )
            st.caption(f"Record #{item.id}")
            identity_column, time_column = st.columns(2)
            identity_column.markdown(
                f"**{text(language, 'full_student_id')}**  \n`{safe_text(item.student_id)}`"
            )
            time_column.markdown(
                f"**{text(language, 'created_at')}**  \n{format_created_at(item.created_at, language)}"
            )
            st.write(item.news_summary)
            st.caption(item.source_uri)
            if item.moderated_at:
                st.caption(
                    f"{text(language, 'moderated_at')}: "
                    f"{format_created_at(item.moderated_at, language)}"
                )
            else:
                st.caption(text(language, "not_moderated"))

            source_column, moderation_column, delete_column = st.columns(3)
            source_column.link_button(
                text(language, "read_source"),
                item.source_uri,
                icon=":material/open_in_new:",
                key=f"admin_source_{item.id}",
                width="stretch",
            )
            moderation_action = "hide" if item.status == "published" else "restore"
            moderation_label = "hide_item" if item.status == "published" else "restore_item"
            if moderation_column.button(
                text(language, moderation_label),
                icon=":material/visibility_off:" if item.status == "published" else ":material/publish:",
                key=f"moderate_{item.id}",
                width="stretch",
            ):
                apply_action(item.id, moderation_action, language)
            if delete_column.button(
                text(language, "delete_item"),
                icon=":material/delete:",
                key=f"delete_{item.id}",
                width="stretch",
            ):
                st.session_state["confirm_delete_id"] = item.id
                st.rerun()

            if st.session_state.get("confirm_delete_id") == item.id:
                st.warning(text(language, "confirm_delete"), icon="⚠️")
                confirm_column, cancel_column = st.columns(2)
                if confirm_column.button(
                    text(language, "confirm_delete_action"),
                    type="primary",
                    key=f"confirm_delete_{item.id}",
                    width="stretch",
                ):
                    apply_action(item.id, "delete", language)
                if cancel_column.button(
                    text(language, "cancel"),
                    key=f"cancel_delete_{item.id}",
                    width="stretch",
                ):
                    st.session_state.pop("confirm_delete_id", None)
                    st.rerun()

    render_footer(language)


def main() -> None:
    try:
        initialize_database()
    except DatabaseError:
        st.error(text("en", "database_error"), icon="⚠️")
        st.stop()

    language = render_top_navigation(destination="dashboard")
    if not is_admin_authenticated():
        render_login(language)
        render_footer(language)
        return
    render_admin_workspace(language)


if __name__ == "__main__":
    main()
