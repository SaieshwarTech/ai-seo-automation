# Deployment Guide

## Prerequisites

- Python `3.13` recommended
- Node.js `18+`
- npm `9+`

## Backend Deployment (FastAPI)

1. Install dependencies:

```bash
cd backend
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:

```bash
set OPENAI_API_KEY=your_openai_api_key_here
set OPENAI_MODEL=gpt-4.1-mini
```

3. Run service:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Frontend Deployment (Vite Build)

1. Install and build:

```bash
cd frontend
npm install
npm run build
```

2. Preview production build:

```bash
npm run preview
```

3. Deploy `frontend/dist` to your static hosting platform.

## Production Recommendations

- Restrict CORS to trusted frontend domains.
- Add API rate limiting.
- Add request logging and monitoring.
- Add retries for network-based scraping.
- Use HTTPS and secure environment variable management.

