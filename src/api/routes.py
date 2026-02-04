from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from .schemas import ApplicantData, PredictionResponse, UserCreate, Token
from ..db.database import get_db
from ..db.models import LoanApplication, User
from ..ml.model import CreditRiskModel
from ..ml.preprocess import DataPreprocessor
from ..ml.explain import ModelExplainer
from .auth import get_password_hash, verify_password, create_access_token, get_current_user
from datetime import timedelta
import numpy as np
import os

router = APIRouter()

# --- Auth Routes ---
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Initialize Singletons

# Initialize Singletons
model_wrapper = CreditRiskModel()
preprocessor = DataPreprocessor()
explainer = ModelExplainer(model_wrapper.model)

def calculate_risk_level(prob: float):
    if prob < 0.3:
        return "Low Risk", "Approved", int(prob * 100)
    elif prob < 0.6:
        return "Medium Risk", "Manual Review", int(prob * 100)
    else:
        return "High Risk", "Rejected", int(prob * 100)

@router.post("/predict", response_model=PredictionResponse)
def predict_loan_risk(data: ApplicantData, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # 1. Preprocess
        raw_dict = data.dict()
        features = preprocessor.preprocess(raw_dict)
        
        # 2. Predict
        prob = model_wrapper.predict_probability(features)
        
        # 3. Business Logic
        risk_category, decision, risk_score = calculate_risk_level(prob)
        
        # 4. Explainability
        explanation = explainer.explain_local(features, preprocessor.get_feature_names())
        
        # 5. DB Logging
        db_entry = LoanApplication(
            **raw_dict,
            default_probability=prob,
            risk_category=risk_category,
            risk_score=risk_score,
            decision=decision
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        
        return {
            "default_probability": prob,
            "risk_category": risk_category,
            "decision": decision,
            "risk_score": risk_score,
            "messsage": explanation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        total = db.query(LoanApplication).count()
        approved = db.query(LoanApplication).filter(LoanApplication.decision == "Approved").count()
        high_risk = db.query(LoanApplication).filter(LoanApplication.risk_category == "High Risk").count()
        
        # Get recent 5 applications (Ascending order)
        recents = db.query(LoanApplication).order_by(LoanApplication.id.asc()).limit(5).all()
        
        return {
            "total_applications": total,
            "approved_count": approved,
            "high_risk_count": high_risk,
            "approval_rate": round((approved / total * 100), 1) if total > 0 else 0,
            "recent_applications": recents,
            
            # Graph 1: Risk Distribution
            "risk_distribution": {
                "Low": db.query(LoanApplication).filter(LoanApplication.risk_category == "Low Risk").count(),
                "Medium": db.query(LoanApplication).filter(LoanApplication.risk_category == "Medium Risk").count(),
                "High": high_risk
            },
            
            # Graph 2: Decisions
            "decisions": {
                "Approved": approved,
                "Rejected": db.query(LoanApplication).filter(LoanApplication.decision == "Rejected").count(),
                "Review": db.query(LoanApplication).filter(LoanApplication.decision == "Manual Review").count()
            },
            
            # Graph 3: Scatter Data (Income vs Loan Amount for High Risk)
            "high_risk_scatter": [
                {"x": r.income_annum, "y": r.loan_amount} 
                for r in db.query(LoanApplication).filter(LoanApplication.risk_category == "High Risk").limit(50).all()
            ],
            
            # Graph 4: Avg Score by Education
            "score_by_edu": {
                "Graduate": int(db.query(func.avg(LoanApplication.risk_score)).filter(LoanApplication.education == "Graduate").scalar() or 0),
                "Not Graduate": int(db.query(func.avg(LoanApplication.risk_score)).filter(LoanApplication.education == "Not Graduate").scalar() or 0)
            }
        }
    except Exception as e:
        print(f"ERROR IN STATS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/applications")
def get_applications(page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        skip = (page - 1) * limit
        total_records = db.query(LoanApplication).count()
        applications = db.query(LoanApplication)\
            .order_by(LoanApplication.id.asc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        return {
            "data": applications,
            "total": total_records,
            "page": page,
            "limit": limit,
            "total_pages": (total_records + limit - 1) // limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
