import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


def load_and_preprocess_data():
    """
    Load raw CSV and preprocess for ML training.
    Returns the fully-encoded, scaled DataFrame.
    """

    df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

    # Drop constant / identifier columns
    drop_columns = ["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"]
    df.drop(columns=drop_columns, inplace=True)

    # Encode target
    df["Attrition"] = df["Attrition"].map({"No": 0, "Yes": 1})

    # Label-encode binary columns
    le = LabelEncoder()
    for col in ["Gender", "OverTime"]:
        df[col] = le.fit_transform(df[col])

    # One-hot encode categoricals
    categorical_columns = [
        "BusinessTravel", "Department", "EducationField",
        "JobRole", "MaritalStatus",
    ]
    df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    # Convert bool columns to int
    bool_cols = df.select_dtypes(include=["bool"]).columns
    df[bool_cols] = df[bool_cols].astype(int)

    return df


def load_raw_data():
    """Load the raw (unprocessed) dataset."""
    return pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")