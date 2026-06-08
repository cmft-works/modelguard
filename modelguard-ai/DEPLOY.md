# Host ModelGuard AI Online

## Fastest option: Render

This repo now has a production root `Dockerfile` and `render.yaml`. It builds the React dashboard and serves it from the FastAPI backend as one web service.

Steps:

1. Push this folder to GitHub.
2. Go to Render.
3. New → Blueprint or New → Web Service.
4. Select the GitHub repo.
5. Render will detect `render.yaml` or the root `Dockerfile`.
6. Deploy.

After deploy, open your Render URL. The dashboard and API will run on the same domain.

Useful URLs:

- `/` dashboard
- `/docs` backend API docs
- `/v1/dashboard/summary` summary API

## Local production test

```bash
cd modelguard-ai
docker build -t modelguard-ai .
docker run -p 8000:8000 modelguard-ai
```

Open `http://localhost:8000`.

## Demo data

The database initializes automatically. To seed demo traffic locally before deployment:

```bash
cd backend
python seed_demo.py
```

For a real hosted demo, send a few test requests from the dashboard form.
