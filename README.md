# 🏦 End-to-End Credit Default Risk Prediction System

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Soumyadeepbhatt/credit-default-risk-system)

An industry-level, modular Machine Learning application designed to assess loan default risk for banking professionals. It features a modern web interface, REST API, explainable AI (SHAP), and a persistent database.

## 🚀 Key Features

*   **Role-Based Interface**: Simple form for Loan Officers to input applicant data.
*   **Real-Time Scoring**: Immediate Risk Score (0-100), Probability, and Decision (Approved/Rejected).
*   **Explainable AI**: SHAP-powered explanations for *why* a loan was rejected (e.g., "High Loan Amount increases risk").
*   **Analytics Dashboard**: Track approval rates and recent volume.
*   **Database Logging**: All decisions are audited in a local SQLite database.
*   **Modular Architecture**: Separated concerns (ML, API, DB) for maintainability.

## 🛠️ Tech Stack

*   **Backend**: FastAPI (Python)
*   **ML Engine**: XGBoost + Scikit-Learn
*   **Database**: SQLite + SQLAlchemy
*   **Frontend**: HTML5 + Bootstrap (Jinja2 Templates)
*   **Explainability**: SHAP (SHapley Additive exPlanations)

## 📂 Project Structure

```
credit-default-risk-system/
├── models/                     # Trained ML Models (credit_risk_model.pkl)
├── src/
│   ├── api/                    # API Endpoints & Business Logic
│   ├── db/                     # Database Models & Connection
│   ├── ml/                     # Inference & Preprocessing Logic
│   └── frontend/templates/     # HTML User Interface
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## ⚡ How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Application**:
    ```bash
    uvicorn src.api.main:app --reload
    ```

3.  **Access the System**:
    *   **Loan Form**: [http://localhost:8000](http://localhost:8000)
    *   **Dashboard**: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
    *   **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Testing the API

You can test the prediction endpoint via curl:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "no_of_dependents": 2,
  "education": "Graduate",
  "self_employed": "No",
  "income_annum": 5000000,
  "loan_amount": 10000000,
  "loan_term": 10,
  "cibil_score": 750,
  "residential_assets_value": 2000000,
  "commercial_assets_value": 0,
  "luxury_assets_value": 500000,
  "bank_asset_value": 500000
}'
```

---
*Created for Production-Grade ML Engineering.*
