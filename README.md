# PathPilot

PathPilot turns a career goal into a scheduled learning roadmap with progress tracking, selected-day streaks, reminders, XP, achievements, and weekly analytics.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload --port 8001
```

Open `http://127.0.0.1:8001/frontend/index.html`. The frontend reads `window.PATHPILOT_API` when supplied and uses the local API automatically during development.

## Deploy

The included `Dockerfile` runs the FastAPI service on port `8000`. `render.yaml` can be used to deploy it on Render. SQLite is suitable for local use; use a persistent disk or a hosted database before production use.

## GitHub

```powershell
git init
git add .
git commit -m "Build PathPilot learning planner"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```