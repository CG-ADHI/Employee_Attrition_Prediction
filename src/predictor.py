import joblib
import pandas as pd
import numpy as np
import os


class AttritionPredictor:
    """
    Handles preprocessing and prediction for new employee data.
    Uses the trained Random Forest model with proper feature alignment.
    """

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model = joblib.load(os.path.join(base_dir, "models", "random_forest.pkl"))
        self.features = joblib.load(os.path.join(base_dir, "models", "features.pkl"))
        self.scaler = joblib.load(os.path.join(base_dir, "models", "scaler.pkl"))
        self.numerical_cols = joblib.load(os.path.join(base_dir, "models", "numerical_cols.pkl"))

    def preprocess(self, employee):
        """
        Transform a dict of raw employee data into model-ready features.
        """
        df = pd.DataFrame([employee])

        # Drop columns the model doesn't use
        for col in ["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours", "Attrition"]:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

        # Label-encode binary columns
        if "Gender" in df.columns:
            df["Gender"] = df["Gender"].map({"Female": 0, "Male": 1})
        if "OverTime" in df.columns:
            df["OverTime"] = df["OverTime"].map({"No": 0, "Yes": 1})

        # One-hot encode categoricals
        categorical = [
            "BusinessTravel", "Department", "EducationField",
            "JobRole", "MaritalStatus",
        ]
        existing_cats = [c for c in categorical if c in df.columns]
        if existing_cats:
            df = pd.get_dummies(df, columns=existing_cats, drop_first=True)
            # Convert bool to int
            bool_cols = df.select_dtypes(include=["bool"]).columns
            df[bool_cols] = df[bool_cols].astype(int)

        # Align columns with training features
        for col in self.features:
            if col not in df.columns:
                df[col] = 0
        df = df[self.features]

        # Scale numerical features
        num_cols_present = [c for c in self.numerical_cols if c in df.columns]
        if num_cols_present:
            df[num_cols_present] = self.scaler.transform(df[num_cols_present])

        return df

    def predict(self, employee):
        """
        Returns (prediction, probability) for a single employee.
        prediction: 0 (stay) or 1 (leave)
        probability: float 0-1 representing attrition risk
        """
        data = self.preprocess(employee)
        prediction = self.model.predict(data)[0]
        probability = self.model.predict_proba(data)[0][1]
        return int(prediction), float(probability)

    def predict_batch(self, employees_df):
        """
        Score a DataFrame of employees. Returns the DataFrame with risk columns added.
        """
        results = []
        for _, row in employees_df.iterrows():
            pred, prob = self.predict(row.to_dict())
            results.append({"prediction": pred, "probability": prob})
        result_df = pd.DataFrame(results)
        result_df["risk_level"] = pd.cut(
            result_df["probability"],
            bins=[0, 0.3, 0.6, 1.0],
            labels=["LOW", "MEDIUM", "HIGH"],
        )
        return pd.concat([employees_df.reset_index(drop=True), result_df], axis=1)