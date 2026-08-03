import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import pandas as pd

# Add the parent directory to sys.path so we can import from src
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from src.predictor import AttritionPredictor

app = FastAPI(title="Employee Attrition API", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Predictor
try:
    predictor = AttritionPredictor()
except Exception as e:
    print(f"Error loading model: {e}")
    predictor = None

# Pydantic model for request validation
class EmployeeData(BaseModel):
    Age: int = Field(..., ge=18, le=100)
    BusinessTravel: str
    Department: str
    DistanceFromHome: int = Field(..., ge=0)
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int
    # Features from EDA missing in above might need default 0 in frontend, 
    # but let's assume we capture what's on the streamlit form plus standard features.
    
    class Config:
        extra = "allow" # allow extra fields to pass through without error, in case some are missing in the model but present in data

@app.get("/")
def read_root():
    return {"message": "Welcome to the Employee Attrition Prediction API"}

@app.get("/api/dashboard")
def get_dashboard_metrics():
    # Load dataset to get metrics
    try:
        df = pd.read_csv(os.path.join(parent_dir, "data", "processed_attrition.csv"))
        total_employees = len(df)
        features = len(df.columns) - 1 # excluding target
        return {
            "total_employees": total_employees,
            "features": features,
            "models_deployed": 1
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/predict")
def predict_attrition(employee: dict):
    if predictor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    try:
        prediction, probability = predictor.predict(employee)
        return {
            "prediction": int(prediction),
            "probability": float(probability),
            "risk_level": "LOW" if probability < 0.3 else "MEDIUM" if probability < 0.6 else "HIGH"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
