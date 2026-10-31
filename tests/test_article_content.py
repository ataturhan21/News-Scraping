import unittest
from unittest.mock import Mock

from article_content import extract_article_text, fetch_article_text


class ArticleContentTests(unittest.TestCase):
    def test_primary_selector_preserves_paragraphs(self):
        html = '<div class="news-content readingTime"><p>First <b>paragraph</b></p><p>İkinci</p></div>'
        self.assertEqual(extract_article_text(html), "First paragraph\nİkinci")

    def test_fallback_selector(self):
        self.assertEqual(extract_article_text('<div class="news-detail-text"><p>Text</p></div>'), "Text")

    def test_missing_content_is_empty(self):
        self.assertEqual(extract_article_text('<html><p>Navigation</p></html>'), "")

    def test_download_has_timeout_and_checks_status(self):
        response = Mock(content=b'<div class="news-detail-text"><p>Text</p></div>')
        session = Mock()
        session.get.return_value = response
        self.assertEqual(fetch_article_text(" https://example.com/article ", session=session), "Text")
        session.get.assert_called_once_with("https://example.com/article", headers=None, timeout=30)
        response.raise_for_status.assert_called_once()

    def test_http_error_is_not_parsed_as_news(self):
        response = Mock()
        response.raise_for_status.side_effect = RuntimeError("HTTP failure")
        session = Mock()
        session.get.return_value = response
        with self.assertRaisesRegex(RuntimeError, "HTTP failure"):
            fetch_article_text("https://example.com/article", session=session)

    def test_invalid_url_never_requests(self):
        session = Mock()
        with self.assertRaises(ValueError):
            fetch_article_text("file:///example", session=session)
        session.get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
