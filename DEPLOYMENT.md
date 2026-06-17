# Deploying the Journal App on Render

This guide walks you through deploying the Flask journal app to [Render](https://render.com).

## Prerequisites

- A [Render](https://render.com) account (free tier works)
- A [GitHub](https://github.com) account
- Git installed locally

## Project files for Render

| File | Purpose |
|------|---------|
| `main.py` | Flask app (`app` object used by Gunicorn) |
| `requirements.txt` | Python dependencies (Flask + Gunicorn) |
| `render.yaml` | Render Blueprint — defines build and start commands |
| `templates/` | HTML templates |
| `static/` | CSS and other static assets |
| `.gitignore` | Keeps secrets, caches, and local data out of Git |

## 1. Prepare locally

Install dependencies and confirm the app runs:

```bash
pip install -r requirements.txt
python main.py
```

Open http://127.0.0.1:5000 and test Add, View, and Search.

To simulate production locally:

```bash
gunicorn main:app --bind 0.0.0.0:5000
```

## 2. Push to GitHub

From the project root:

```bash
git init
git add .
git commit -m "Prepare journal app for Render deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/journal-app.git
git push -u origin main
```

Replace `YOUR_USERNAME/journal-app` with your repository URL.

`journal.txt` is listed in `.gitignore` so local entries are not pushed. The app creates the file on the server when the first entry is saved.

## 3. Deploy on Render

### Option A — Blueprint (recommended)

Uses `render.yaml` in this repo.

1. Log in to the [Render Dashboard](https://dashboard.render.com).
2. Click **New** → **Blueprint**.
3. Connect your GitHub account and select the `journal-app` repository.
4. Render reads `render.yaml` and creates the web service.
5. Click **Apply** to deploy.

### Option B — Manual web service

1. Click **New** → **Web Service**.
2. Connect the GitHub repository.
3. Set these values:

   | Setting | Value |
   |---------|-------|
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn main:app --bind 0.0.0.0:$PORT` |

4. Choose the **Free** plan (optional).
5. Click **Create Web Service**.

Render assigns a public URL like `https://journal-app-xxxx.onrender.com`.

## 4. Verify deployment

1. Open your Render service URL in a browser.
2. Add a journal entry on the **Add Entry** page.
3. Confirm it appears on **View Entries**.
4. Search for a keyword on **Search Entries**.

In the Render dashboard, check **Logs** if the service fails to start.

## How Render runs the app

1. **Build** — `pip install -r requirements.txt` installs Flask and Gunicorn.
2. **Start** — Gunicorn loads `main:app` and listens on the port Render provides via `$PORT`.
3. **Requests** — Render routes HTTP traffic to your Gunicorn worker.

Local development uses Flask’s built-in server (`python main.py`). Production on Render uses Gunicorn, which is the standard WSGI server for Flask.

## Important: data persistence

On Render’s free web services, the filesystem is **ephemeral**. `journal.txt` is stored on the instance disk, so entries may be **lost** when:

- The service redeploys after a Git push
- Render restarts the instance (common on the free tier after inactivity)

For a production journal app, use persistent storage (for example a Render PostgreSQL database or another managed database). The current setup is fine for learning and demos.

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| Build fails | Render logs; confirm `requirements.txt` is valid |
| 502 / service won’t start | Start command must be `gunicorn main:app --bind 0.0.0.0:$PORT` |
| App loads but styles missing | Confirm `static/style.css` is committed and pushed |
| Templates error | Confirm the `templates/` folder is committed and pushed |

## Updating the live app

Push changes to the `main` branch on GitHub. Render redeploys automatically if auto-deploy is enabled (default).

```bash
git add .
git commit -m "Describe your change"
git push
```
