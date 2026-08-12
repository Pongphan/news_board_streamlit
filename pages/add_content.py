"""Add-content form page."""

from __future__ import annotations

import streamlit as st

from database import ALLOWED_SECTIONS, DatabaseError, create_news, initialize_database
from ui import configure_page, render_brand, render_footer
from validation import validate_news


configure_page("เพิ่มเนื้อหา")


def render_form() -> None:
    render_brand()

    if st.button("กลับหน้าบอร์ดข่าว", icon=":material/arrow_back:"):
        st.switch_page("app.py")

    st.markdown(
        """
        <section class="form-intro">
            <div class="eyebrow">Contribute to the board</div>
            <h1>เพิ่มเนื้อหาใหม่</h1>
            <p>กรอกข้อมูลให้ครบถ้วน ระบบจะตรวจสอบก่อนบันทึกและพากลับไปยังบอร์ดข่าวโดยอัตโนมัติ</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="content_form_shell"):
        with st.form("add_content_form", clear_on_submit=False):
            section = st.selectbox(
                "Section *",
                ALLOWED_SECTIONS,
                help="เลือก Section ของผู้ส่งข่าว",
            )
            student_id = st.text_input(
                "Student ID *",
                placeholder="ตัวอย่าง 6612345678",
                max_chars=20,
                help="ใช้ตัวอักษร ตัวเลข _ หรือ - จำนวน 4–20 ตัว",
            )
            news_summary = st.text_area(
                "News Summary *",
                placeholder="สรุปใจความสำคัญของข่าว (10–2,000 ตัวอักษร)",
                height=190,
                max_chars=2000,
            )
            source_uri = st.text_input(
                "Source URI *",
                placeholder="https://example.com/news",
                help="รองรับเฉพาะลิงก์ http:// และ https://",
            )
            submitted = st.form_submit_button(
                "Save",
                icon=":material/save:",
                type="primary",
                width="stretch",
            )

    if not submitted:
        render_footer()
        return

    errors, cleaned = validate_news(section, student_id, news_summary, source_uri)
    if errors:
        st.error("กรุณาตรวจสอบข้อมูลก่อนบันทึก", icon="⚠️")
        for message in errors.values():
            st.write(f"- {message}")
        render_footer()
        return

    try:
        create_news(**cleaned)
    except DatabaseError as exc:
        st.error(str(exc), icon="⚠️")
        render_footer()
        return

    # Invalidate dashboard reads, keep a one-time message, then navigate home.
    st.cache_data.clear()
    st.session_state["save_success"] = "บันทึกเนื้อหาเรียบร้อยแล้ว และอัปเดตบอร์ดข่าวล่าสุดให้แล้ว"
    st.switch_page("app.py")


def main() -> None:
    try:
        initialize_database()
    except DatabaseError as exc:
        st.error(str(exc), icon="⚠️")
        st.stop()
    render_form()


if __name__ == "__main__":
    main()
