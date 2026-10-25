# CitySentinel
### Evidence-driven Agentic AI for safer, smarter future cities

CitySentinel is a hackathon-ready prototype that demonstrates a human-supervised multi-agent workflow for urban incident management: **detect → investigate → assess risk → plan → verify**.

> **Prototype scope:** This repository uses clearly labelled synthetic/simulated city incidents. It is not connected to real emergency infrastructure and must not be used for operational emergency decisions.

## Features
- Responsive city-operations dashboard with incident queue, severity, evidence, and suggested responses.
- Multi-agent workflow simulated by a Python API: Data Analysis, Investigation, Risk Assessment, Planning, and Verification.
- Human approval gate for critical actions.
- Audit-friendly incident analysis response with evidence and reasoning summaries.
- Synthetic seed data; no API keys or paid AI service required.
- Optional API integration point for future LLM/tool-calling support.

## Stack
- Frontend: React, Vite, Lucide React, Recharts
- Backend: Python, FastAPI, Pydantic
- Data: synthetic JSON seed data

## Run locally
### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

### 2. Frontend
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite. The frontend expects the API at `http://localhost:8000` by default; set `VITE_API_URL` if needed.

## API endpoints
- `GET /health` — service status
- `GET /api/incidents` — synthetic incident feed
- `POST /api/analyze/{incident_id}` — run the multi-agent analysis pipeline
- `POST /api/incidents/{incident_id}/approve` — record human approval for a recommended action

## GitHub upload
Create a new repository named `citysentinel` on GitHub, then from this folder run:
```bash
git init
git add .
git commit -m "Build CitySentinel urban intelligence prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/citysentinel.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. Do not commit secrets, `.env` files, virtual environments, or API keys.

## Next steps
1. Replace synthetic data with a documented public dataset or approved city data feed.
2. Add authentication and role-based access control before storing real user data.
3. Add tests, rate limits, structured logging, and deployment configuration.
4. If adding an LLM, require evidence citations, bounded tool access, and human approval for consequential actions.

## Team
Team TS — ChronoForge | Agentic AI track
