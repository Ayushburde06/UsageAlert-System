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
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── Dockerfile
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

## Deployment on AWS EC2 (Dockerized)

1. Provision an Ubuntu EC2 instance on AWS.
2. Ensure Security Groups allow inbound traffic on ports 80 (Frontend), 8000 (Backend) and 22 (SSH).
3. Connect via SSH: `ssh -i key.pem ubuntu@<your-ec2-ip>`
4. Install Docker and Docker Compose on the instance.
5. Transfer this project folder to the instance (e.g., using `scp` or `git clone`).
6. Navigate to the `backend` folder and build/run:
   ```bash
   docker build -t energy-backend .
   docker run -d -p 8000:8000 energy-backend
   ```
7. Navigate to the `frontend` folder and build/run:
   ```bash
   docker build -t energy-frontend .
   docker run -d -p 80:80 energy-frontend
   ```

*Note: In the frontend `src/App.jsx`, change `API_URL` to point to the EC2 Public IP address (`http://<EC2-IP>:8000`) before building the frontend Docker image.*
