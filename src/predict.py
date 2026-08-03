import joblib
import pandas as pd

model = joblib.load("models/random_forest.pkl")

df = pd.read_csv("data/processed_attrition.csv")

sample = df.drop("Attrition", axis=1).iloc[[0]]

prediction = model.predict(sample)[0]
probability = model.predict_proba(sample)[0][1]

print("=" * 50)

if prediction == 1:
    print("Prediction : Employee likely to Leave")
else:
    print("Prediction : Employee likely to Stay")

print(f"Attrition Probability : {probability:.2%}")

print("=" * 50)