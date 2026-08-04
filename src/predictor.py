import os
import joblib
import pandas as pd


class AttritionPredictor:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.model = joblib.load(os.path.join(base_dir, "models", "random_forest.pkl"))
        self.features = joblib.load(os.path.join(base_dir, "models", "features.pkl"))
        self.scaler = joblib.load(os.path.join(base_dir, "models", "scaler.pkl"))
        self.numerical_cols = joblib.load(os.path.join(base_dir, "models", "numerical_cols.pkl"))

    def preprocess(self, employee):

        df = pd.DataFrame([employee])

    # Remove unused columns
        drop_cols = [
            "EmployeeCount",
            "EmployeeNumber",
            "Over18",
            "StandardHours",
            "Attrition",
    ]

        for col in drop_cols:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

    # Binary encoding
        df["Gender"] = 1 if employee.get("Gender") == "Male" else 0
        df["OverTime"] = 1 if employee.get("OverTime") == "Yes" else 0

    # ---------- Create ALL model features ----------
        X = pd.DataFrame(0, index=[0], columns=self.features)

    # Numerical columns
        for col in self.numerical_cols:
            if col in employee:
                X.at[0, col] = employee[col]

    # Binary columns
        X.at[0, "Gender"] = df.at[0, "Gender"]
        X.at[0, "OverTime"] = df.at[0, "OverTime"]

    # One-hot encoded columns
        bt = f"BusinessTravel_{employee.get('BusinessTravel')}"
        if bt in X.columns:
            X.at[0, bt] = 1

        dep = f"Department_{employee.get('Department')}"
        if dep in X.columns:
            X.at[0, dep] = 1

        edu = f"EducationField_{employee.get('EducationField')}"
        if edu in X.columns:
            X.at[0, edu] = 1

        job = f"JobRole_{employee.get('JobRole')}"
        if job in X.columns:
            X.at[0, job] = 1

        mar = f"MaritalStatus_{employee.get('MaritalStatus')}"
        if mar in X.columns:
            X.at[0, mar] = 1

        # Scale all columns
        X = pd.DataFrame(self.scaler.transform(X), columns=self.features)

        return X

    def predict(self, employee):

        X = self.preprocess(employee)

        prediction = self.model.predict(X)[0]

        probability = self.model.predict_proba(X)[0][1]

        return int(prediction), float(probability)

    def predict_batch(self, employees_df):

        predictions = []
        probabilities = []
        risks = []

        for _, row in employees_df.iterrows():

            pred, prob = self.predict(row.to_dict())

            predictions.append(pred)
            probabilities.append(prob)

            if prob < 0.30:
                risks.append("LOW")
            elif prob < 0.60:
                risks.append("MEDIUM")
            else:
                risks.append("HIGH")

        result = employees_df.copy()

        result["prediction"] = predictions
        result["probability"] = probabilities
        result["risk_level"] = risks

        return result