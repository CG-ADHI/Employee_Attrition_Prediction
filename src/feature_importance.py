import os
import sys
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_feature_importance():
    """
    Generate feature importance analysis from Random Forest
    and Logistic Regression coefficient analysis.
    """

    # Load model and data
    rf_model = joblib.load("models/random_forest.pkl")
    lr_model = joblib.load("models/logistic_regression.pkl")
    features = joblib.load("models/features.pkl")

    # ── Random Forest Feature Importance ──────────────────────
    rf_imp = pd.DataFrame({
        "Feature": features,
        "Importance": rf_model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE — RANDOM FOREST")
    print("=" * 60)
    print(rf_imp.head(15).to_string(index=False))

    # ── Logistic Regression Coefficients ──────────────────────
    lr_coef = pd.DataFrame({
        "Feature": features,
        "Coefficient": lr_model.coef_[0],
    }).sort_values("Coefficient", ascending=False)

    print("\n" + "=" * 60)
    print("LOGISTIC REGRESSION COEFFICIENTS")
    print("=" * 60)
    print("Positive = increases attrition risk")
    print("Negative = decreases attrition risk")
    print(lr_coef.to_string(index=False))

    # ── Save chart ────────────────────────────────────────────
    os.makedirs("reports/figures", exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    top10 = rf_imp.head(10)
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 10))
    ax.barh(top10["Feature"][::-1], top10["Importance"][::-1], color=colors[::-1])
    ax.set_title("Top 10 Feature Importances (Random Forest)", fontweight="bold", fontsize=13)
    ax.set_xlabel("Importance")
    plt.tight_layout()
    fig.savefig("reports/figures/16_feature_importance.png", dpi=150)
    plt.close(fig)

    print("\nFeature importance chart saved.")

    return rf_imp, lr_coef


if __name__ == "__main__":
    generate_feature_importance()