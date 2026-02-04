from pydantic import BaseModel, Field
from typing import Literal

class ApplicantData(BaseModel):
    no_of_dependents: int = Field(..., ge=0, description="Number of dependents")
    education: Literal['Graduate', 'Not Graduate']
    self_employed: Literal['Yes', 'No']
    income_annum: int = Field(..., gt=0)
    loan_amount: int = Field(..., gt=0)
    loan_term: int = Field(..., gt=0)
    cibil_score: int = Field(..., ge=300, le=900)
    residential_assets_value: int = Field(..., ge=0)
    commercial_assets_value: int = Field(..., ge=0)
    luxury_assets_value: int = Field(..., ge=0)
    bank_asset_value: int = Field(..., ge=0)

    class Config:
        schema_extra = {
            "example": {
                "no_of_dependents": 2,
                "education": "Graduate",
                "self_employed": "No",
                "income_annum": 5000000,
                "loan_amount": 15000000,
                "loan_term": 10,
                "cibil_score": 750,
                "residential_assets_value": 2000000,
                "commercial_assets_value": 500000,
                "luxury_assets_value": 5000000,
                "bank_asset_value": 1000000
            }
        }

class PredictionResponse(BaseModel):
    default_probability: float
    risk_category: str
    decision: str
    risk_score: int
    messsage: str

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
