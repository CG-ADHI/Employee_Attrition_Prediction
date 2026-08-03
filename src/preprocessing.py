import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler


def run_preprocessing():
    """
    Full preprocessing pipeline for the HR Attrition dataset.
    - Drops constant/identifier columns
    - Label-encodes binary categoricals
    - One-hot encodes nominal categoricals
    - Scales numerical features
    - Saves processed dataset and scaler
    """

    DATASET_PATH = "data/WA_Fn-UseC_-HR-Employee-Attrition.csv"
    OUTPUT_PATH = "data/processed_attrition.csv"

    print("=" * 60)
    print("DATA PREPROCESSING")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Load raw dataset
    # --------------------------------------------------
    df = pd.read_csv(DATASET_PATH)
    print(f"\nLoaded dataset: {df.shape[0]} rows x {df.shape[1]} columns")

    # --------------------------------------------------
    # 2. Data quality check
    # --------------------------------------------------
    print(f"\nMissing values : {df.isnull().sum().sum()}")
    print(f"Duplicate rows : {df.duplicated().sum()}")

    # --------------------------------------------------
    # 3. Drop constant / identifier columns
    # --------------------------------------------------
    drop_columns = [
        "EmployeeCount",    # constant = 1 for all rows
        "EmployeeNumber",   # unique identifier, no predictive value
        "Over18",           # constant = 'Y' for all rows
        "StandardHours",    # constant = 80 for all rows
    ]

    df.drop(columns=drop_columns, inplace=True)
    print(f"\nDropped columns: {drop_columns}")

    # --------------------------------------------------
    # 4. Encode target variable
    # --------------------------------------------------
    df["Attrition"] = df["Attrition"].map({"No": 0, "Yes": 1})

    # --------------------------------------------------
    # 5. Label encode binary columns
    # --------------------------------------------------
    binary_columns = ["Gender", "OverTime"]
    le = LabelEncoder()

    for col in binary_columns:
        df[col] = le.fit_transform(df[col])
        print(f"Label encoded: {col}")

    # --------------------------------------------------
    # 6. One-hot encode nominal categoricals
    # --------------------------------------------------
    categorical_columns = [
        "BusinessTravel",
        "Department",
        "EducationField",
        "JobRole",
        "MaritalStatus",
    ]

    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    # Convert bool columns to int (pandas get_dummies produces bool)
    bool_cols = df.select_dtypes(include=["bool"]).columns
    df[bool_cols] = df[bool_cols].astype(int)

    print(f"\nOne-hot encoded: {categorical_columns}")
    print(f"Dataset shape after encoding: {df.shape}")

    # --------------------------------------------------
    # 7. Scale numerical features
    # --------------------------------------------------
    # Identify numerical columns (excluding target and already-encoded binary/dummy cols)
    target_col = "Attrition"
    numerical_cols = [
        "Age", "DailyRate", "DistanceFromHome", "Education",
        "EnvironmentSatisfaction", "HourlyRate", "JobInvolvement",
        "JobLevel", "JobSatisfaction", "MonthlyIncome", "MonthlyRate",
        "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating",
        "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
        "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany",
        "YearsInCurrentRole", "YearsSinceLastPromotion", "YearsWithCurrManager",
    ]

    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # Save scaler for later use in prediction
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(numerical_cols, "models/numerical_cols.pkl")
    print("\nScaler saved to models/scaler.pkl")

    # --------------------------------------------------
    # 8. Save processed dataset
    # --------------------------------------------------
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nProcessed dataset saved to {OUTPUT_PATH}")
    print(f"Final shape: {df.shape}")

    return df


if __name__ == "__main__":
    run_preprocessing()