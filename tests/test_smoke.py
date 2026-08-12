from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_DIR = Path(__file__).resolve().parents[1]


def test_dashboard_starts_without_exception(monkeypatch, tmp_path):
    """Use a temporary DB by patching the module constant before running the app."""

    import database

    monkeypatch.setattr(database, "DEFAULT_DATABASE_PATH", tmp_path / "smoke.db")
    app = AppTest.from_file(PROJECT_DIR / "app.py", default_timeout=10)
    app.run()

    assert not app.exception
    assert app.selectbox[0].label == "กรองตาม Section"
    assert any(button.label == "เพิ่มเนื้อหา" for button in app.button)


def test_add_content_page_starts_without_exception(monkeypatch, tmp_path):
    import database

    monkeypatch.setattr(database, "DEFAULT_DATABASE_PATH", tmp_path / "form-smoke.db")
    app = AppTest.from_file(PROJECT_DIR / "pages" / "add_content.py", default_timeout=10)
    app.run()

    assert not app.exception
    assert app.selectbox[0].label == "Section *"
    assert app.text_input[0].label == "Student ID *"
    assert app.text_area[0].label == "News Summary *"
