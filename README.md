# AI Energy Anomaly Detection System

A full-stack application to upload telemetry data (CSV), process it, and detect anomalies using Isolation Forest.

## Project Structure
```
ASI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints.py
│   │   ├── model/
│   │   │   └── anomaly_detector.py
│   │   ├── services/
│   │   │   └── data_processing.py
│   │   └── __init__.py
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Running Locally

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Deployment (Optional)

This project is built to be cloud-ready. While it currently runs locally, it can be easily deployed to modern cloud providers:

* **Backend (FastAPI):** Can be deployed as a Web Service on platforms like Render, Railway, or AWS EC2.
* **Frontend (React/Vite):** Can be deployed as a static site on Vercel, Netlify, or AWS S3. 
* **Database (Future expansion):** Can be connected to a PostgreSQL database on Supabase or Neon to store historical anomaly alerts.

To prep for deployment, ensure the `API_URL` in `src/App.jsx` points to the production backend URL rather than `localhost:8000`.
