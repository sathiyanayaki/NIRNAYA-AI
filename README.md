# NIRNAYA AI 🌧️
### Multi-Agent Flood Decision Intelligence & Rainwater Management System

**NIRNAYA AI** is a prototype AI-powered disaster decision-support system that combines flood risk prediction, geospatial vulnerability assessment, route optimization, decision auditing, and rainwater resource management.

Its goal is not just to predict flood risk, but also to support better disaster-response decisions and encourage rainwater conservation.

## 🎯 Problem Statement

Flooding can cause damage to communities, infrastructure, and water resources. Traditional approaches often focus on predicting flood risk without combining multiple decision-support capabilities.

NIRNAYA AI addresses this by integrating multiple specialized agents into one coordinated workflow.

## ✨ Key Features

- **Flood Prediction:** Random Forest machine learning model classifies flood risk.
- **Geospatial Vulnerability:** Evaluates vulnerability using elevation, drainage capacity, and previous flooding.
- **Route Optimization:** Uses NetworkX to identify a minimum distance-risk cost route in a simulated road network.
- **Rainwater Management:** Estimates collectable rainwater, storage, domestic allocation, groundwater recharge, and overflow.
- **Decision Auditor:** Checks consistency between agent outputs and provides warnings and recommendations.
- **Multi-Agent Coordinator:** Combines the outputs of all specialized agents.
- **Interactive Dashboard:** Displays results through a web interface.
- **What-if Simulation:** Compares different rainfall scenarios.
- **Analysis History:** Stores analysis results using SQLite.

## 🏗️ System Architecture

```text
             User Input
                 |
                 v
          FastAPI Backend
                 |
                 v
        Multi-Agent Coordinator
                 |
       +---------+---------+
       |         |         |
       v         v         v
   Prediction  Geospatial  Route
     Agent      Agent     Agent
       |         |         |
       +---------+---------+
                 |
                 v
       Rainwater Management
              Agent
                 |
                 v
          Decision Auditor
                 |
                 v
          Final Decision
                 |
        +--------+--------+
        |                 |
        v                 v
    Dashboard        SQLite History
```

## 🤖 Specialized Agents

| Agent | Responsibility |
|---|---|
| Prediction Agent | Predicts flood risk using Random Forest |
| Geospatial Agent | Evaluates location vulnerability |
| Route Optimization Agent | Finds a minimum-cost route |
| Rainwater Management Agent | Estimates rainwater collection and allocation |
| Decision Auditor | Validates calculations and checks warnings |
| Agent Coordinator | Integrates all agent outputs |

## 🛠️ Technology Stack

**Programming:** Python

**Machine Learning:** Pandas, NumPy, Scikit-learn, Random Forest

**Backend:** FastAPI, Uvicorn

**Frontend:** HTML, CSS, JavaScript, Chart.js

**Database:** SQLite

**Optimization:** NetworkX

**Model Storage:** Joblib

## 📁 Project Structure

```text
NIRNAYA AI/
│
├── agents/
│   ├── prediction_agent.py
│   ├── geospatial_agent.py
│   ├── route_agent.py
│   ├── water_management_agent.py
│   ├── decision_auditor.py
│   ├── coordinator.py
│   └── test_*.py
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── data/
│   ├── generate_dataset.py
│   └── flood_dataset.csv
│
├── database/
│   └── db.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   ├── train_model.py
│   └── flood_model.pkl
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "NIRNAYA AI"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend

From the project root:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 5. Start the frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Open the dashboard:

http://127.0.0.1:5500

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend welcome |
| GET | `/health` | Health check |
| POST | `/predict` | Flood risk prediction |
| POST | `/analyze` | Complete multi-agent analysis |
| GET | `/history` | Retrieve saved analyses |

Interactive API documentation is available at `/docs`.

## 🧪 Testing

Individual agent tests can be executed using:

```bash
python -m agents.test_prediction
python -m agents.test_geospatial
python -m agents.test_route
python -m agents.test_auditor
python -m agents.test_water_management
python -m agents.test_coordinator
```

## 🌧️ Rainwater Management

The rainwater management module estimates:

- Collectable rainwater
- Storage capacity utilization
- Domestic non-potable water allocation
- Groundwater recharge allocation
- Remaining overflow

It also checks water allocation calculations through the Decision Auditor.

## ⚠️ Limitations and Assumptions

- The current training dataset is synthetically generated and does not represent validated real-world Chennai flood observations.
- The reported model accuracy applies to a synthetic held-out test dataset, not real-world flood forecasting.
- The route network is simulated and does not represent verified live road conditions or guaranteed safe evacuation routes.
- Rainwater collection and recharge calculations use prototype assumptions. Actual implementation requires site assessment, filtration, water-quality testing, and soil suitability verification.
- The system is a decision-support prototype and must not replace official disaster-management alerts or professional assessments.
- The agents currently use Python-based logic and tools; they are not autonomous LLM-powered agents.

## 🚀 Future Enhancements

- Integration with real-time rainfall and weather APIs.
- Real-world geographical and elevation datasets.
- Live road-network integration.
- Advanced flood forecasting using validated historical datasets.
- Improved rainwater harvesting and groundwater recharge planning.
- Cloud deployment and scalable data storage.

## 👩‍💻 Project Information

**Project:** NIRNAYA AI

**Domain:** Artificial Intelligence, Machine Learning, Multi-Agent Systems, Disaster Management

**Purpose:** Explainable flood decision support and rainwater conservation planning.

---

*Built as an AI/ML prototype to explore how coordinated intelligent agents can support disaster preparedness and sustainable water management.*