# API Reference

Base URL:

`http://127.0.0.1:8000`

## Health

### `GET /health`

Returns service status.

Response:

```json
{
  "status": "ok"
}
```

## Single URL Analysis

### `POST /api/analyze`

Request:

```json
{
  "url": "https://example.com"
}
```

Response fields include:

- `seo_score`
- `keyword_density`
- `audit_breakdown`
- `issues`
- `suggestions`
- `scraped_data`

## Bulk URL Analysis

### `POST /api/bulk-analyze`

Request:

```json
{
  "urls": ["https://example.com", "https://example.org"]
}
```

Response:

- `total`
- `results[]` with `success` or `error` entries

## Rewrite Content

### `POST /api/rewrite`

Request:

```json
{
  "content": "Your content here...",
  "focus_keyword": "seo automation",
  "tone": "professional"
}
```

Response:

```json
{
  "rewritten_content": "..."
}
```

## Keyword Generation

### `POST /api/keywords`

Request:

```json
{
  "topic": "technical seo",
  "seed_keywords": ["site audit", "core web vitals"]
}
```

Response:

```json
{
  "keywords": ["...", "..."]
}
```

## Blog Generation

### `POST /api/blog`

Request:

```json
{
  "topic": "AI SEO workflow",
  "target_keyword": "ai seo automation",
  "audience": "business owners"
}
```

Response:

```json
{
  "blog_content": "..."
}
```

## PDF Export

### `POST /api/export/pdf`

Request body: send a full audit response object (or equivalent structure).

Response: binary PDF (`application/pdf`)

