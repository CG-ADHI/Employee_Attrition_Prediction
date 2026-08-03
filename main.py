import os
import pandas as pd

# Dataset path
DATASET_PATH = "data/WA_Fn-UseC_-HR-Employee-Attrition.csv"

print("=" * 60)
print("EMPLOYEE ATTRITION PREDICTION FOR HR")
print("=" * 60)

# Check dataset
if not os.path.exists(DATASET_PATH):
    print(f"❌ Dataset not found at: {DATASET_PATH}")
    exit()

# Load dataset
df = pd.read_csv(DATASET_PATH)

print("\n✅ Dataset Loaded Successfully!")

print("\nShape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nTarget Variable Distribution:")
print(df["Attrition"].value_counts())