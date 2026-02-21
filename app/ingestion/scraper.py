import hashlib
import logging
import re
from urllib.parse import urlparse
from xml.etree import ElementTree

import httpx
import trafilatura

logger = logging.getLogger(__name__)


def scrape_url(url: str) -> str:
    """Fetch a URL and extract clean plaintext using trafilatura."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError(f"Failed to fetch URL: {url}")
    text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
    if not text:
        raise ValueError(f"Failed to extract text from URL: {url}")
    return text


def hash_text(text: str) -> str:
    """Return a short SHA-256 hash of text for deduplication."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def is_publication_url(url: str) -> bool:
    """Check if URL points to a publication root rather than a single article.

    Returns True for:
    - Substack roots (*.substack.com with no article path)
    - Any URL with no meaningful path (bare domain) — we'll try feed discovery
    """
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    # Substack: explicit detection
    if "substack.com" in parsed.netloc:
        return path == "" or path in ("/archive", "/about")

    # Generic: bare domain or common publication paths → try as publication
    if path in ("", "/archive", "/blog", "/articles", "/posts", "/writing"):
        return True

    return False


def discover_articles(url: str, max_articles: int = 20) -> list[dict]:
    """Discover article URLs from a publication. Returns list of {url, title}.

    Tries RSS feed first (works for Substack and most blogs).
    """
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    # Try RSS feed
    feed_urls = [
        f"{base}/feed",
        f"{base}/rss",
        f"{base}/feed.xml",
        f"{base}/atom.xml",
    ]

    for feed_url in feed_urls:
        articles = _parse_feed(feed_url, max_articles)
        if articles:
            logger.info("Found %d articles from feed: %s", len(articles), feed_url)
            return articles

    # Fallback: try Substack API
    if "substack.com" in parsed.netloc:
        articles = _substack_api(base, max_articles)
        if articles:
            return articles

    raise ValueError(
        f"Could not discover articles from {url}. "
        "Try pasting a direct article URL instead."
    )


def _parse_feed(feed_url: str, max_articles: int) -> list[dict]:
    """Parse an RSS/Atom feed and return article URLs + titles."""
    try:
        resp = httpx.get(feed_url, timeout=15, follow_redirects=True)
        resp.raise_for_status()
    except (httpx.HTTPError, httpx.TimeoutException):
        return []

    try:
        root = ElementTree.fromstring(resp.text)
    except ElementTree.ParseError:
        return []

    articles = []

    # RSS 2.0: <channel><item><title>...<link>...
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        if link_el is not None and link_el.text:
            articles.append({
                "url": link_el.text.strip(),
                "title": title_el.text.strip() if title_el is not None and title_el.text else "",
            })
        if len(articles) >= max_articles:
            break

    if articles:
        return articles

    # Atom: <entry><title>...<link href="...">
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link[@rel='alternate']", ns)
        if link_el is None:
            link_el = entry.find("atom:link", ns)
        if link_el is not None:
            href = link_el.get("href", "")
            if href:
                articles.append({
                    "url": href,
                    "title": title_el.text.strip() if title_el is not None and title_el.text else "",
                })
        if len(articles) >= max_articles:
            break

    return articles


def _substack_api(base_url: str, max_articles: int) -> list[dict]:
    """Fetch articles from Substack's API endpoint."""
    try:
        resp = httpx.get(
            f"{base_url}/api/v1/posts",
            params={"limit": max_articles},
            timeout=15,
            follow_redirects=True,
        )
        resp.raise_for_status()
        posts = resp.json()
    except (httpx.HTTPError, httpx.TimeoutException, ValueError):
        return []

    return [
        {"url": p.get("canonical_url", ""), "title": p.get("title", "")}
        for p in posts
        if p.get("canonical_url")
    ][:max_articles]
