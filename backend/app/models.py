from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class AnalyzeRequest(BaseModel):
    url: HttpUrl


class BulkAnalyzeRequest(BaseModel):
    urls: list[HttpUrl] = Field(..., min_length=1)


class RewriteRequest(BaseModel):
    content: str = Field(..., min_length=30)
    focus_keyword: str = Field(..., min_length=2)
    tone: str = "professional"


class KeywordRequest(BaseModel):
    topic: str = Field(..., min_length=2)
    seed_keywords: list[str] = []


class BlogRequest(BaseModel):
    topic: str = Field(..., min_length=2)
    target_keyword: str = Field(..., min_length=2)
    audience: str = "general"


class ScrapedData(BaseModel):
    url: str
    title: str
    meta_description: str
    meta_keywords: str
    headings: dict[str, list[str]]
    paragraphs: list[str]
    images: list[dict[str, str]]
    internal_links: list[str]
    word_count: int


class SeoIssue(BaseModel):
    category: str
    issue: str
    recommendation: str
    impact: str


class AnalyzeResponse(BaseModel):
    url: str
    seo_score: float
    keyword_density: list[dict[str, Any]]
    audit_breakdown: dict[str, float]
    issues: list[SeoIssue]
    suggestions: list[str]
    scraped_data: ScrapedData

