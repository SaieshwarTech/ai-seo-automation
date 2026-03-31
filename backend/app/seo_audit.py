from __future__ import annotations

import re
from collections import Counter

from .models import ScrapedData, SeoIssue

STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "is",
    "it",
    "this",
    "that",
    "you",
    "your",
    "are",
    "as",
    "be",
    "at",
    "from",
}


def run_seo_audit(scraped: ScrapedData) -> dict:
    content = " ".join(scraped.paragraphs + sum(scraped.headings.values(), []))
    words = _tokenize_words(content)
    word_count = len(words) if words else 1

    frequency = Counter(words)
    top_keywords = []
    for word, count in frequency.most_common(15):
        if word in STOPWORDS or len(word) <= 2:
            continue
        density = round((count / word_count) * 100, 2)
        top_keywords.append({"keyword": word, "count": count, "density_percent": density})
        if len(top_keywords) >= 10:
            break

    issues: list[SeoIssue] = []
    scores = {
        "keyword_density": _score_keyword_density(top_keywords, issues),
        "meta_tags": _score_meta_tags(scraped, issues),
        "heading_structure": _score_headings(scraped, issues),
        "internal_linking": _score_internal_links(scraped, issues),
    }

    weights = {
        "keyword_density": 0.25,
        "meta_tags": 0.30,
        "heading_structure": 0.25,
        "internal_linking": 0.20,
    }
    seo_score = round(sum(scores[key] * weights[key] for key in scores), 2)

    suggestions = [issue.recommendation for issue in issues]
    if not suggestions:
        suggestions.append("Strong baseline SEO detected. Maintain consistency and monitor performance.")

    return {
        "seo_score": seo_score,
        "keyword_density": top_keywords,
        "audit_breakdown": scores,
        "issues": issues,
        "suggestions": suggestions,
    }


def _tokenize_words(text: str) -> list[str]:
    clean = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    return [w for w in clean.split() if w.strip()]


def _score_keyword_density(keywords: list[dict], issues: list[SeoIssue]) -> float:
    if not keywords:
        issues.append(
            SeoIssue(
                category="Keyword Density",
                issue="No meaningful keywords detected.",
                recommendation="Add topic-specific terms naturally throughout content.",
                impact="high",
            )
        )
        return 25.0

    highest = max(k["density_percent"] for k in keywords)
    if highest > 4.5:
        issues.append(
            SeoIssue(
                category="Keyword Density",
                issue=f"Potential keyword stuffing detected at {highest}%.",
                recommendation="Reduce repetitive usage and add semantic variants.",
                impact="medium",
            )
        )
        return 60.0
    if highest < 0.8:
        issues.append(
            SeoIssue(
                category="Keyword Density",
                issue=f"Low keyword prominence at {highest}%.",
                recommendation="Increase relevant keyword mentions in key sections.",
                impact="medium",
            )
        )
        return 70.0
    return 92.0


def _score_meta_tags(scraped: ScrapedData, issues: list[SeoIssue]) -> float:
    score = 100.0
    title_len = len(scraped.title.strip())
    desc_len = len(scraped.meta_description.strip())

    if title_len == 0:
        score -= 45
        issues.append(
            SeoIssue(
                category="Meta Tags",
                issue="Missing title tag.",
                recommendation="Add a unique title tag between 30 and 60 characters.",
                impact="high",
            )
        )
    elif title_len < 30 or title_len > 60:
        score -= 18
        issues.append(
            SeoIssue(
                category="Meta Tags",
                issue=f"Title length is {title_len} characters.",
                recommendation="Keep title tags within 30-60 characters for best SERP display.",
                impact="medium",
            )
        )

    if desc_len == 0:
        score -= 40
        issues.append(
            SeoIssue(
                category="Meta Tags",
                issue="Missing meta description.",
                recommendation="Add a compelling meta description between 120 and 160 characters.",
                impact="high",
            )
        )
    elif desc_len < 120 or desc_len > 160:
        score -= 15
        issues.append(
            SeoIssue(
                category="Meta Tags",
                issue=f"Meta description length is {desc_len} characters.",
                recommendation="Keep descriptions within 120-160 characters for clarity and CTR.",
                impact="medium",
            )
        )

    return max(0.0, round(score, 2))


def _score_headings(scraped: ScrapedData, issues: list[SeoIssue]) -> float:
    score = 100.0
    h1_count = len(scraped.headings.get("h1", []))
    if h1_count == 0:
        score -= 45
        issues.append(
            SeoIssue(
                category="Heading Structure",
                issue="No H1 heading found.",
                recommendation="Add one clear, keyword-focused H1 heading.",
                impact="high",
            )
        )
    elif h1_count > 1:
        score -= 18
        issues.append(
            SeoIssue(
                category="Heading Structure",
                issue=f"Multiple H1 headings found ({h1_count}).",
                recommendation="Use one primary H1 and structure the rest with H2-H4.",
                impact="medium",
            )
        )

    levels_present = [int(level[1]) for level, items in scraped.headings.items() if items]
    levels_present.sort()
    for idx in range(1, len(levels_present)):
        if levels_present[idx] - levels_present[idx - 1] > 1:
            score -= 12
            issues.append(
                SeoIssue(
                    category="Heading Structure",
                    issue="Skipped heading levels detected.",
                    recommendation="Follow a logical heading hierarchy without skipping levels.",
                    impact="low",
                )
            )
            break

    return max(0.0, round(score, 2))


def _score_internal_links(scraped: ScrapedData, issues: list[SeoIssue]) -> float:
    link_count = len(scraped.internal_links)
    if link_count == 0:
        issues.append(
            SeoIssue(
                category="Internal Linking",
                issue="No internal links found.",
                recommendation="Add contextual internal links to improve crawl depth and UX.",
                impact="high",
            )
        )
        return 30.0
    if link_count < 3:
        issues.append(
            SeoIssue(
                category="Internal Linking",
                issue=f"Only {link_count} internal links detected.",
                recommendation="Add more relevant internal links between related pages.",
                impact="medium",
            )
        )
        return 72.0
    return 94.0

