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
            "Attrition"
        ]

        for col in drop_cols:
            if col in df.columns:
                df.drop(columns=col, inplace=True)

        # Binary Encoding
        if "Gender" in df.columns:
            df["Gender"] = df["Gender"].map({
                "Male": 1,
                "Female": 0
            })

        if "OverTime" in df.columns:
            df["OverTime"] = df["OverTime"].map({
                "Yes": 1,
                "No": 0
            })

        # Create missing numerical columns
        for col in self.numerical_cols:
            if col not in df.columns:
                df[col] = 0

        # One Hot Encoding
        categorical_cols = [
            "BusinessTravel",
            "Department",
            "EducationField",
            "JobRole",
            "MaritalStatus"
        ]

        existing = [c for c in categorical_cols if c in df.columns]

        df = pd.get_dummies(
            df,
            columns=existing,
            drop_first=False
        )

        # Convert bool → int
        bool_cols = df.select_dtypes(include=["bool"]).columns
        df[bool_cols] = df[bool_cols].astype(int)

        # Add missing dummy columns
        for col in self.features:
            if col not in df.columns:
                df[col] = 0

        # Keep only training columns
        df = df[self.features]

        # Scale
        num_cols = [c for c in self.numerical_cols if c in df.columns]

        df[num_cols] = self.scaler.transform(df[num_cols])

        return df

    def predict(self, employee):

        X = self.preprocess(employee)

        prediction = self.model.predict(X)[0]

        probability = self.model.predict_proba(X)[0][1]

        return int(prediction), float(probability)

    def predict_batch(self, df):

        preds = []

        probs = []

        risks = []

        for _, row in df.iterrows():

            p, pr = self.predict(row.to_dict())

            preds.append(p)

            probs.append(pr)

            if pr < 0.30:
                risks.append("LOW")
            elif pr < 0.60:
                risks.append("MEDIUM")
            else:
                risks.append("HIGH")

        result = df.copy()

        result["prediction"] = preds
        result["probability"] = probs
        result["risk_level"] = risks

        return result