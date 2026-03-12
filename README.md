# AI Energy Anomaly & Forecasting Dashboard 🚀

Welcome to my AI Energy Anomaly Detection project! I built this to solve a real-world problem: helping facility managers quickly spot "weird" energy usage in buildings without having to stare at spreadsheets all day.

This is a full-stack application that uses Machine Learning to automatically flag spikes and even predict what the usage might look like for the next few days.

## ✨ Key Features
*   **Smart Upload:** Just drop in a CSV or Excel file of energy readings.
*   **Anomaly Detection:** Uses an **Isolation Forest** model to find outliers (spikes/drops) that look suspicious.
*   **Predictive Forecasting:** Uses **Linear Regression** to trend out the next 3 points of data, helping plan for future usage.
*   **Interactive UI:** A clean, dark-mode dashboard with charts that highlight problems in red and forecasts in green.
*   **Cloud Ready:** Built with a decoupled architecture (FastAPI backend + React frontend), making it easy to host on platforms like Render or AWS.

## 🛠️ Tech Stack
*   **Frontend:** React.js, Vite, Recharts (for the cool graphs), Lucide-React (icons).
*   **Backend:** Python, FastAPI (super fast web framework).
*   **ML/Data:** Scikit-Learn (the "brains"), Pandas (data crunching), Openpyxl (Excel support).

## 🚀 How to Run It Locally

### 1. Setup the Backend
Open your terminal and go to the backend folder:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Setup the Frontend
Open a *second* terminal and go to the frontend folder:
```bash
cd frontend
npm install
npm run dev
```
Now just open `http://localhost:5173` in your browser!

---

## ☁️ Deployment Note
This project is currently configured to run with a live backend on Render. If you want to run it purely on your own computer, just change the `API_URL` to `http://localhost:8000` in `frontend/src/App.jsx`.

## 📂 Project Structure
*   `backend/`: FastAPI server and ML models.
*   `frontend/`: React dashboard and UI components.
*   `render.yaml`: Configuration for automated cloud deployment.

---
Built with curiosity to understand how buildings can become more autonomous and energy-efficient! 🏢🌲
