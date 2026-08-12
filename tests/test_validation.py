from validation import normalize_uri, validate_news


def test_valid_news_is_normalized():
    errors, cleaned = validate_news(
        " Section 1 ",
        " 6612345678 ",
        "  ข่าวกิจกรรมทดสอบที่มีรายละเอียดครบถ้วน  ",
        " HTTPS://example.com/news?q=campus ",
    )

    assert errors == {}
    assert cleaned == {
        "section": "Section 1",
        "student_id": "6612345678",
        "news_summary": "ข่าวกิจกรรมทดสอบที่มีรายละเอียดครบถ้วน",
        "source_uri": "https://example.com/news?q=campus",
    }


def test_invalid_news_reports_every_field():
    errors, _ = validate_news("Section 9", "12", "สั้น", "javascript:alert(1)")
    assert set(errors) == {"section", "student_id", "news_summary", "source_uri"}


def test_uri_rejects_non_http_and_invalid_port():
    assert normalize_uri("ftp://example.com/file") == ""
    assert normalize_uri("https://example.com:abc/news") == ""
    assert normalize_uri("https://example.com/news") == "https://example.com/news"
