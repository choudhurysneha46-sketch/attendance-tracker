# 📋 Attendance Tracker

A full-stack web app to log your classes and instantly see your attendance percentage — built with a JavaScript frontend and a Python (Flask) backend.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Database:** SQLite
- **Deployment:** Frontend on Vercel, Backend on Render

## Features
- Add subjects
- Mark a class as Present / Absent
- See live attendance % per subject
- Delete subjects
- Visual warning if attendance drops below 75%

## Project Structure
```
attendance-tracker/
├── backend/
│   ├── app.py            # Flask API
│   ├── requirements.txt
│   └── render.yaml
└── frontend/
    ├── index.html
    ├── style.css
    ├── config.js          # holds backend API URL
    └── script.js
```

## Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Runs on `http://127.0.0.1:5000`

### Frontend
Just open `frontend/index.html` in your browser (or use VS Code's Live Server extension).

## Deployment

### Backend → Render
1. Push this repo to GitHub
2. On Render, create a new **Web Service**, connect this repo, set root directory to `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`

### Frontend → Vercel
1. On Vercel, import this repo, set root directory to `frontend`
2. Deploy
3. After backend is deployed, update `frontend/config.js` with your live Render URL, then redeploy frontend

## Author
Sneha Choudhury
