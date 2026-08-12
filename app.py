"""Main dashboard page for the Streamlit news board."""

from __future__ import annotations

import streamlit as st

from database import ALLOWED_SECTIONS, DatabaseError, count_news, initialize_database, list_news
from ui import (
    configure_page,
    format_created_at,
    mask_student_id,
    render_brand,
    render_footer,
    safe_text,
)


configure_page("บอร์ดข่าวสาร")


@st.cache_data(ttl=15, show_spinner=False)
def get_news(section: str | None, keyword: str):
    """Cache short-lived reads; the add page clears this cache after writing."""

    return list_news(section=section, keyword=keyword)


@st.cache_data(ttl=15, show_spinner=False)
def get_stats() -> tuple[int, int]:
    return count_news()


def render_dashboard() -> None:
    render_brand()
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Community updates · ข่าวสารล่าสุด</div>
            <h1>เรื่องราวที่ควรรู้<br>ในที่เดียว</h1>
            <p>พื้นที่รวบรวมข่าวสารจากนักศึกษา แยกตาม Section พร้อมลิงก์ต้นทางที่ตรวจสอบย้อนกลับได้</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if message := st.session_state.pop("save_success", None):
        st.success(message, icon="✅")

    st.markdown(
        """
        <div class="section-heading">
            <div class="eyebrow">News collection</div>
            <h2>บอร์ดข่าวสาร</h2>
            <p>ค้นหาและกรองข่าวล่าสุดจากทุก Section</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        selected_label = st.selectbox(
            "กรองตาม Section",
            ("ทุก Section", *ALLOWED_SECTIONS),
        )
    with search_col:
        keyword = st.text_input(
            "ค้นหาในสรุปข่าว",
            placeholder="เช่น เทคโนโลยี การศึกษา กิจกรรม...",
        )

    selected_section = None if selected_label == "ทุก Section" else selected_label

    try:
        total_count, represented_sections = get_stats()
        news_items = get_news(selected_section, keyword.strip())
    except DatabaseError as exc:
        st.error(str(exc), icon="⚠️")
        return

    total_col, result_col, section_col = st.columns(3)
    total_col.metric("ข่าวทั้งหมด", total_count)
    result_col.metric("ผลลัพธ์ที่พบ", len(news_items))
    section_col.metric("Section ที่มีข่าว", represented_sections)

    if not news_items:
        if total_count:
            st.info("ยังไม่พบข่าวที่ตรงกับตัวกรอง ลองเปลี่ยน Section หรือคำค้นหา")
        else:
            st.info("ยังไม่มีข่าวในระบบ เริ่มต้นด้วยปุ่ม “เพิ่มเนื้อหา” ด้านซ้ายล่าง")
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
                        f"นักศึกษา {mask_student_id(item.student_id)} · "
                        f"{format_created_at(item.created_at)}"
                    )
                    # st.write escapes user content; do not render the summary as raw HTML.
                    st.write(item.news_summary)
                    st.link_button(
                        "อ่านข่าวต้นทาง",
                        item.source_uri,
                        icon=":material/open_in_new:",
                        width="stretch",
                    )

    # The keyed container gives the button a stable CSS hook for bottom-left positioning.
    with st.container(key="floating_add_content"):
        if st.button(
            "เพิ่มเนื้อหา",
            icon=":material/add:",
            type="primary",
            key="open_add_content",
        ):
            st.switch_page("pages/add_content.py")

    render_footer()


def main() -> None:
    try:
        initialize_database()
    except DatabaseError as exc:
        st.error(str(exc), icon="⚠️")
        st.stop()
    render_dashboard()


if __name__ == "__main__":
    main()
