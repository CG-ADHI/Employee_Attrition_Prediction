import os
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
)

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import load_and_preprocess_data


def train_models():
    """
    Train Logistic Regression, Random Forest, and Decision Tree classifiers.
    Applies StandardScaler to all features before training.
    Uses class-weight balancing due to imbalanced target (16% attrition).
    Saves models, scaler, and feature list to models/.
    """

    df = load_and_preprocess_data()

    # ── Features & Target ─────────────────────────────────────────
    X = df.drop("Attrition", axis=1)
    y = df["Attrition"]

    feature_names = X.columns.tolist()

    # ── Scale features ────────────────────────────────────────────
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=feature_names)

    # ── Train / Test Split ────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("=" * 60)
    print("MODEL TRAINING")
    print("=" * 60)
    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print(f"Attrition rate   : {y.mean():.2%}")
    print(f"Features         : {len(feature_names)}")

    # ── Define models ─────────────────────────────────────────────
    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            class_weight="balanced",
            random_state=42,
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=8,
            class_weight="balanced",
            random_state=42,
        ),
    }

    results = {}

    for name, model in models.items():
        print(f"\n{'=' * 60}")
        print(f"{name.upper()}")
        print("=" * 60)

        model.fit(X_train, y_train)

        pred = model.predict(X_test)
        prob = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, pred)
        prec = precision_score(y_test, pred)
        rec = recall_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        auc = roc_auc_score(y_test, prob)

        results[name] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "roc_auc": auc,
        }

        print(f"Accuracy  : {acc:.4f}")
        print(f"Precision : {prec:.4f}")
        print(f"Recall    : {rec:.4f}")
        print(f"F1 Score  : {f1:.4f}")
        print(f"ROC AUC   : {auc:.4f}")
        print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, pred)}")
        print(f"\n{classification_report(y_test, pred)}")

    # ── Save models ───────────────────────────────────────────────
    os.makedirs("models", exist_ok=True)

    joblib.dump(models["Logistic Regression"], "models/logistic_regression.pkl")
    joblib.dump(models["Random Forest"], "models/random_forest.pkl")
    joblib.dump(models["Decision Tree"], "models/decision_tree.pkl")
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(feature_names, "models/features.pkl")
    joblib.dump(results, "models/metrics.pkl")

    print("\nAll models saved to models/")

    # ── ROC Curve ─────────────────────────────────────────────────
    os.makedirs("reports/figures", exist_ok=True)

    plt.figure(figsize=(8, 6))
    for name, model in models.items():
        prob = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, prob)
        auc_val = results[name]["roc_auc"]
        plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})", linewidth=2)

    plt.plot([0, 1], [0, 1], "k--", alpha=0.4, linewidth=1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve — Model Comparison")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("reports/figures/17_roc_curve.png", dpi=150)
    plt.close()
    print("ROC curve saved to reports/figures/17_roc_curve.png")

    # ── Feature Importance ────────────────────────────────────────
    rf_model = models["Random Forest"]
    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": rf_model.feature_importances_,
    }).sort_values("Importance", ascending=False)

    print("\nTop 10 Important Features (Random Forest):")
    print(importance.head(10).to_string(index=False))

    plt.figure(figsize=(10, 6))
    top10 = importance.head(10)
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 10))
    plt.barh(top10["Feature"][::-1], top10["Importance"][::-1], color=colors[::-1])
    plt.title("Top 10 Feature Importances (Random Forest)")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig("reports/figures/16_feature_importance.png", dpi=150)
    plt.close()
    print("Feature importance chart saved.")

    # ── At-Risk Watch List ────────────────────────────────────────
    raw_df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    probs_all = rf_model.predict_proba(scaler.transform(
        df.drop("Attrition", axis=1)
    ))[:, 1]

    watchlist = raw_df[["Age", "Department", "JobRole", "MonthlyIncome",
                        "YearsAtCompany", "OverTime", "JobSatisfaction"]].copy()
    watchlist["Attrition_Probability"] = np.round(probs_all, 4)
    watchlist["Risk_Level"] = pd.cut(
        probs_all,
        bins=[0, 0.3, 0.6, 1.0],
        labels=["LOW", "MEDIUM", "HIGH"],
    )
    watchlist = watchlist.sort_values("Attrition_Probability", ascending=False)
    watchlist.to_csv("reports/at_risk_employees.csv", index=False)

    high_risk = (watchlist["Risk_Level"] == "HIGH").sum()
    medium_risk = (watchlist["Risk_Level"] == "MEDIUM").sum()
    low_risk = (watchlist["Risk_Level"] == "LOW").sum()

    print(f"\nAt-Risk Employee Watch List saved to reports/at_risk_employees.csv")
    print(f"  HIGH risk   : {high_risk}")
    print(f"  MEDIUM risk : {medium_risk}")
    print(f"  LOW risk    : {low_risk}")

    return models, scaler, results


if __name__ == "__main__":
    train_models()