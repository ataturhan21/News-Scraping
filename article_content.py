"""Bounded article downloads for the research notebook."""

from bs4 import BeautifulSoup


def extract_article_text(content):
    soup = BeautifulSoup(content, "html.parser")
    article = soup.select_one("div.news-content.readingTime")
    if article is None:
        article = soup.select_one("div.news-detail-text")
    if article is None:
        return ""
    return "\n".join(paragraph.get_text(" ", strip=True) for paragraph in article.find_all("p"))


def fetch_article_text(url, headers=None, session=None, timeout=30):
    if not isinstance(url, str) or not url.strip().startswith(("http://", "https://")):
        raise ValueError("Article URL must use http or https")
    if session is None:
        import requests
        session = requests
    response = session.get(url.strip(), headers=headers, timeout=timeout)
    response.raise_for_status()
    return extract_article_text(response.content)
