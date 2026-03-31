# Architecture

## System Design

The project follows a decoupled frontend-backend architecture:

- React client consumes REST APIs.
- FastAPI backend handles scraping, SEO analysis, AI orchestration, and report generation.

## Backend Layers

- `main.py`: API routing and orchestration.
- `scraper.py`: HTML fetch and structural data extraction.
- `seo_audit.py`: rule engine + weighted scoring.
- `ai_service.py`: OpenAI integrations + fallback behavior.
- `report_service.py`: PDF generation.
- `models.py`: request/response schema contracts.

## Frontend Layers

- `App.jsx`: dashboard layout, tab workflows, API integration.
- `styles.css`: shared styling and dark theme background effects.
- Recharts used for visual score analytics.

## Data Flow

1. UI sends request to backend endpoint.
2. Backend processes and returns structured payload.
3. UI renders KPI panels, charts, issue cards, and suggestions.
4. Optional: user triggers AI content workflows and export actions.

## Design Principles

- Simple and extensible module boundaries.
- Fail-soft AI behavior when API keys are unavailable.
- Fast iteration with clear API contracts.

