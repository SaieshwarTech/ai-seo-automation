from __future__ import annotations

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .models import ScrapedData


def scrape_website(url: str) -> ScrapedData:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
    }
    response = requests.get(url, timeout=25, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    parsed_base = urlparse(url)

    title = (soup.title.string or "").strip() if soup.title else ""
    meta_description = _get_meta(soup, "description")
    meta_keywords = _get_meta(soup, "keywords")

    headings = {
        "h1": _extract_texts(soup, "h1"),
        "h2": _extract_texts(soup, "h2"),
        "h3": _extract_texts(soup, "h3"),
        "h4": _extract_texts(soup, "h4"),
        "h5": _extract_texts(soup, "h5"),
        "h6": _extract_texts(soup, "h6"),
    }
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    images = []
    for img in soup.find_all("img"):
        src = (img.get("src") or "").strip()
        if not src:
            continue
        images.append(
            {
                "src": urljoin(url, src),
                "alt": (img.get("alt") or "").strip(),
            }
        )

    internal_links: list[str] = []
    for a in soup.find_all("a"):
        href = (a.get("href") or "").strip()
        if not href or href.startswith("#"):
            continue
        absolute = urljoin(url, href)
        target = urlparse(absolute)
        if target.netloc == parsed_base.netloc:
            internal_links.append(absolute)

    text_blob = " ".join([" ".join(paragraphs), " ".join(sum(headings.values(), []))]).strip()
    word_count = len([w for w in text_blob.split() if w.strip()])

    return ScrapedData(
        url=url,
        title=title,
        meta_description=meta_description,
        meta_keywords=meta_keywords,
        headings=headings,
        paragraphs=paragraphs,
        images=images,
        internal_links=sorted(set(internal_links)),
        word_count=word_count,
    )


def _get_meta(soup: BeautifulSoup, name: str) -> str:
    tag = soup.find("meta", attrs={"name": name})
    if not tag:
        return ""
    return (tag.get("content") or "").strip()


def _extract_texts(soup: BeautifulSoup, tag_name: str) -> list[str]:
    return [tag.get_text(" ", strip=True) for tag in soup.find_all(tag_name)]

