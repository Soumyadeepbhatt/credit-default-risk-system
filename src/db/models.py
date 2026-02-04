from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Applicant Inputs
    no_of_dependents = Column(Integer)
    education = Column(String)
    self_employed = Column(String)
    income_annum = Column(Integer)
    loan_amount = Column(Integer)
    loan_term = Column(Integer)
    cibil_score = Column(Integer)
    residential_assets_value = Column(Integer)
    commercial_assets_value = Column(Integer)
    luxury_assets_value = Column(Integer)
    bank_asset_value = Column(Integer)
    
    # Model Outputs
    default_probability = Column(Float)
    risk_score = Column(Integer) # scaled 0-100 or simply Risk Category Logic
    risk_category = Column(String) # Low, Medium, High
    decision = Column(String) # Approve, Reject

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
