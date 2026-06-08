# ModelGuard AI

AI Control Tower for CIO, CFO, and CISO teams.

## What is included

- FastAPI backend
- SQLite database
- AI gateway endpoint
- Policy engine
- Risk scoring
- Cost tracking
- Audit logs
- Dashboard APIs
- React dashboard
- Docker Compose setup
- Demo seed data

## Run locally with Docker

```bash
cd modelguard-ai
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- Backend docs: http://localhost:8000/docs

## Run without Docker

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Seed demo data:

```bash
cd backend
python seed_demo.py
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Main API

POST `/v1/ai/chat`

```json
{
  "user_email": "analyst@company.com",
  "department": "Finance",
  "role": "employee",
  "app_name": "Budget Bot",
  "provider": "openai",
  "model": "gpt-4o-mini",
  "prompt": "Analyze this internal data",
  "data_classification": "internal"
}
```

## Policy examples

- Restricted data cannot go to public models.
- Confidential data requires approved roles.
- Secrets, emails, SSNs, and credit card-like patterns increase risk.
- High-risk requests are blocked.

## Next production upgrades

1. Replace mock provider calls in `backend/app/services/provider_router.py` with real SDK calls.
2. Add Okta or Azure AD SSO.
3. Move from SQLite to PostgreSQL.
4. Move audit events to ClickHouse or BigQuery.
5. Add real DLP integration like Microsoft Purview, BigID, Nightfall, or custom regex/entity detection.
6. Add Slack, Teams, or email alerts.
7. Add department budgets and chargeback reports.
8. Add model routing rules to recommend cheaper models.
