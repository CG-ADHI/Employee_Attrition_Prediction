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

        # -----------------------------
        # Binary Encoding
        # -----------------------------
        if "Gender" in df.columns:
            df["Gender"] = df["Gender"].map({
                "Female": 0,
                "Male": 1
            })

        if "OverTime" in df.columns:
            df["OverTime"] = df["OverTime"].map({
                "No": 0,
                "Yes": 1
            })

        # -----------------------------
        # Add Missing Numerical Columns
        # -----------------------------
        for col in self.numerical_cols:
            if col not in df.columns:
                df[col] = 0

        # -----------------------------
        # Manual One-Hot Encoding
        # -----------------------------

        mapping = {

            "BusinessTravel": [
                "Travel_Frequently",
                "Travel_Rarely"
            ],

            "Department": [
                "Research & Development",
                "Sales"
            ],

            "EducationField": [
                "Life Sciences",
                "Marketing",
                "Medical",
                "Other",
                "Technical Degree"
            ],

            "JobRole": [
                "Human Resources",
                "Laboratory Technician",
                "Manager",
                "Manufacturing Director",
                "Research Director",
                "Research Scientist",
                "Sales Executive",
                "Sales Representative"
            ],

            "MaritalStatus": [
                "Married",
                "Single"
            ]
        }

        for column, categories in mapping.items():

            value = ""

            if column in df.columns:
                value = str(df.loc[0, column])

            for cat in categories:
                df[f"{column}_{cat}"] = 1 if value == cat else 0

            if column in df.columns:
                df.drop(columns=[column], inplace=True)

        # -----------------------------
        # Ensure every training feature exists
        # -----------------------------
        for col in self.features:
            if col not in df.columns:
                df[col] = 0

        # Remove unwanted columns
        df = df[self.features]

        # -----------------------------
        # Scale Numerical Features
        # -----------------------------
        numerical = [c for c in self.numerical_cols if c in df.columns]

        if numerical:
            df[numerical] = self.scaler.transform(df[numerical])

        return df

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