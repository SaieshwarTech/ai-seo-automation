from __future__ import annotations

import asyncio
from io import BytesIO

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .ai_service import AIService
from .models import (
    AnalyzeRequest,
    AnalyzeResponse,
    BlogRequest,
    BulkAnalyzeRequest,
    KeywordRequest,
    RewriteRequest,
)
from .report_service import build_pdf_report
from .scraper import scrape_website
from .seo_audit import run_seo_audit

app = FastAPI(title="AI SEO Automation API", version="1.0.0")
ai_service = AIService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _analyze_url(url: str) -> AnalyzeResponse:
    scraped = scrape_website(url)
    audit = run_seo_audit(scraped)
    return AnalyzeResponse(
        url=url,
        seo_score=audit["seo_score"],
        keyword_density=audit["keyword_density"],
        audit_breakdown=audit["audit_breakdown"],
        issues=audit["issues"],
        suggestions=audit["suggestions"],
        scraped_data=scraped,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        return _analyze_url(str(request.url))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to analyze URL: {exc}") from exc


@app.post("/api/bulk-analyze")
async def bulk_analyze(request: BulkAnalyzeRequest) -> dict:
    async def run_one(url: str):
        try:
            result = await asyncio.to_thread(_analyze_url, url)
            return {"status": "success", "result": result.model_dump()}
        except Exception as exc:
            return {"status": "error", "url": url, "error": str(exc)}

    tasks = [run_one(str(url)) for url in request.urls]
    results = await asyncio.gather(*tasks)
    return {"total": len(results), "results": results}


@app.post("/api/rewrite")
def rewrite_content(request: RewriteRequest) -> dict:
    rewritten = ai_service.rewrite_content(request.content, request.focus_keyword, request.tone)
    return {"rewritten_content": rewritten}


@app.post("/api/keywords")
def generate_keywords(request: KeywordRequest) -> dict:
    keywords = ai_service.generate_keywords(request.topic, request.seed_keywords)
    return {"keywords": keywords}


@app.post("/api/blog")
def generate_blog(request: BlogRequest) -> dict:
    blog = ai_service.generate_blog(request.topic, request.target_keyword, request.audience)
    return {"blog_content": blog}


@app.post("/api/export/pdf")
def export_pdf(report: dict):
    try:
        pdf_bytes = build_pdf_report(report)
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": 'attachment; filename="seo-report.pdf"'},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {exc}") from exc

