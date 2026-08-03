import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
FIGURES_DIR = "reports/figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Color palette — clean, professional, not garish
PALETTE = {"No": "#4A90D9", "Yes": "#E74C3C"}
SINGLE_COLOR = "#4A90D9"
ACCENT_COLOR = "#E74C3C"

sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "font.family": "sans-serif",
})


def save_fig(fig, name):
    fig.savefig(os.path.join(FIGURES_DIR, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def run_eda():
    """
    Complete Exploratory Data Analysis for the HR Attrition dataset.
    Generates 16+ publication-quality visualizations.
    """
    raw = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # ── 1. Attrition Distribution ─────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5))
    counts = raw["Attrition"].value_counts()
    bars = ax.bar(counts.index, counts.values, color=[PALETTE["No"], PALETTE["Yes"]], width=0.5, edgecolor="white")
    for bar, val in zip(bars, counts.values):
        pct = val / len(raw) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f"{val}\n({pct:.1f}%)", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Employee Attrition Distribution", fontweight="bold", fontsize=13)
    ax.set_ylabel("Count")
    ax.set_ylim(0, counts.max() * 1.2)
    save_fig(fig, "01_attrition_distribution.png")
    print("  [1/16] Attrition distribution")

    # ── 2. Age Distribution by Attrition ──────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, color in PALETTE.items():
        subset = raw[raw["Attrition"] == label]
        ax.hist(subset["Age"], bins=20, alpha=0.65, label=f"Attrition={label}", color=color, edgecolor="white")
    ax.set_title("Age Distribution by Attrition", fontweight="bold", fontsize=13)
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    ax.legend()
    save_fig(fig, "02_age_distribution.png")
    print("  [2/16] Age distribution")

    # ── 3. Monthly Income by Attrition ────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=raw, x="Attrition", y="MonthlyIncome", palette=PALETTE, ax=ax, width=0.4)
    ax.set_title("Monthly Income by Attrition Status", fontweight="bold", fontsize=13)
    save_fig(fig, "03_monthly_income.png")
    print("  [3/16] Monthly income")

    # ── 4. Correlation Heatmap (top correlated with Attrition) ─
    processed = pd.read_csv("data/processed_attrition.csv")
    corr = processed.corr(numeric_only=True)
    # Show top 15 features most correlated with Attrition
    attrition_corr = corr["Attrition"].drop("Attrition").abs().sort_values(ascending=False).head(15)
    top_features = ["Attrition"] + attrition_corr.index.tolist()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(processed[top_features].corr(), annot=True, fmt=".2f",
                cmap="RdBu_r", center=0, ax=ax, square=True,
                linewidths=0.5, cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation Heatmap — Top Features vs Attrition", fontweight="bold", fontsize=13)
    save_fig(fig, "04_correlation_heatmap.png")
    print("  [4/16] Correlation heatmap")

    # ── 5. Department vs Attrition (Rate) ─────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    dept = raw.groupby("Department")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=False)
    bars = ax.bar(dept.index, dept.values, color=[ACCENT_COLOR, SINGLE_COLOR, SINGLE_COLOR],
                  width=0.5, edgecolor="white")
    for bar, val in zip(bars, dept.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Department", fontweight="bold", fontsize=13)
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, dept.max() * 1.3)
    save_fig(fig, "05_department_attrition.png")
    print("  [5/16] Department attrition")

    # ── 6. Gender vs Attrition ────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.countplot(data=raw, x="Gender", hue="Attrition", palette=PALETTE, ax=ax, edgecolor="white")
    ax.set_title("Gender vs Attrition", fontweight="bold", fontsize=13)
    ax.legend(title="Attrition")
    save_fig(fig, "06_gender_attrition.png")
    print("  [6/16] Gender attrition")

    # ── 7. Overtime vs Attrition (Rate) ───────────────────────
    fig, ax = plt.subplots(figsize=(6, 5))
    ot = raw.groupby("OverTime")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=False)
    bars = ax.bar(ot.index, ot.values, color=[ACCENT_COLOR, SINGLE_COLOR], width=0.4, edgecolor="white")
    for bar, val in zip(bars, ot.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by OverTime Status", fontweight="bold", fontsize=13)
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, ot.max() * 1.3)
    save_fig(fig, "07_overtime_attrition.png")
    print("  [7/16] Overtime attrition")

    # ── 8. Job Satisfaction vs Attrition ──────────────────────
    fig, ax = plt.subplots(figsize=(7, 5))
    sat = raw.groupby("JobSatisfaction")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    )
    ax.bar(sat.index.astype(str), sat.values, color=SINGLE_COLOR, width=0.5, edgecolor="white")
    for i, val in enumerate(sat.values):
        ax.text(i, val + 0.5, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Job Satisfaction Level", fontweight="bold", fontsize=13)
    ax.set_xlabel("Job Satisfaction (1=Low, 4=High)")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, sat.max() * 1.3)
    save_fig(fig, "08_job_satisfaction.png")
    print("  [8/16] Job satisfaction")

    # ── 9. Work-Life Balance vs Attrition ─────────────────────
    fig, ax = plt.subplots(figsize=(7, 5))
    wlb = raw.groupby("WorkLifeBalance")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    )
    ax.bar(wlb.index.astype(str), wlb.values, color=SINGLE_COLOR, width=0.5, edgecolor="white")
    for i, val in enumerate(wlb.values):
        ax.text(i, val + 0.5, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Work-Life Balance", fontweight="bold", fontsize=13)
    ax.set_xlabel("Work-Life Balance (1=Low, 4=High)")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, wlb.max() * 1.3)
    save_fig(fig, "09_worklife_balance.png")
    print("  [9/16] Work-life balance")

    # ── 10. Years at Company — Attrition spike analysis ───────
    fig, ax = plt.subplots(figsize=(10, 5))
    bins = [0, 1, 2, 3, 5, 8, 12, 20, 40]
    labels = ["0-1", "1-2", "2-3", "3-5", "5-8", "8-12", "12-20", "20+"]
    raw["YearsGroup"] = pd.cut(raw["YearsAtCompany"], bins=bins, labels=labels, right=True)
    yac = raw.groupby("YearsGroup", observed=True)["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    )
    colors = [ACCENT_COLOR if v > 20 else SINGLE_COLOR for v in yac.values]
    bars = ax.bar(yac.index.astype(str), yac.values, color=colors, edgecolor="white")
    for bar, val in zip(bars, yac.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=10)
    ax.set_title("Attrition Rate by Years at Company", fontweight="bold", fontsize=13)
    ax.set_xlabel("Years at Company")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, yac.max() * 1.3)
    raw.drop(columns=["YearsGroup"], inplace=True)
    save_fig(fig, "10_years_company.png")
    print("  [10/16] Years at company")

    # ── 11. Distance From Home vs Attrition ───────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    bins_dist = [0, 5, 10, 15, 20, 30]
    labels_dist = ["0-5", "5-10", "10-15", "15-20", "20+"]
    raw["DistGroup"] = pd.cut(raw["DistanceFromHome"], bins=bins_dist, labels=labels_dist, right=True)
    dist_rate = raw.groupby("DistGroup", observed=True)["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    )
    ax.bar(dist_rate.index.astype(str), dist_rate.values, color=SINGLE_COLOR, edgecolor="white")
    for i, val in enumerate(dist_rate.values):
        ax.text(i, val + 0.5, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Distance From Home (km)", fontweight="bold", fontsize=13)
    ax.set_xlabel("Distance From Home")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, dist_rate.max() * 1.3)
    raw.drop(columns=["DistGroup"], inplace=True)
    save_fig(fig, "11_distance_home.png")
    print("  [11/16] Distance from home")

    # ── 12. Job Role vs Attrition (Rate) ──────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    jr = raw.groupby("JobRole")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=True)
    colors = [ACCENT_COLOR if v > 20 else SINGLE_COLOR for v in jr.values]
    ax.barh(jr.index, jr.values, color=colors, edgecolor="white")
    for i, val in enumerate(jr.values):
        ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontweight="bold", fontsize=10)
    ax.set_title("Attrition Rate by Job Role", fontweight="bold", fontsize=13)
    ax.set_xlabel("Attrition Rate (%)")
    save_fig(fig, "12_job_role.png")
    print("  [12/16] Job role")

    # ── 13. Marital Status vs Attrition ───────────────────────
    fig, ax = plt.subplots(figsize=(7, 5))
    ms = raw.groupby("MaritalStatus")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=False)
    bars = ax.bar(ms.index, ms.values, color=[ACCENT_COLOR, SINGLE_COLOR, SINGLE_COLOR],
                  width=0.5, edgecolor="white")
    for bar, val in zip(bars, ms.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Marital Status", fontweight="bold", fontsize=13)
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, ms.max() * 1.3)
    save_fig(fig, "13_marital_status.png")
    print("  [13/16] Marital status")

    # ── 14. Business Travel vs Attrition ──────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    bt = raw.groupby("BusinessTravel")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=False)
    colors = [ACCENT_COLOR if v > 20 else SINGLE_COLOR for v in bt.values]
    bars = ax.bar(bt.index, bt.values, color=colors, width=0.5, edgecolor="white")
    for bar, val in zip(bars, bt.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Business Travel", fontweight="bold", fontsize=13)
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, bt.max() * 1.3)
    ax.set_xticklabels(bt.index, rotation=15)
    save_fig(fig, "14_business_travel.png")
    print("  [14/16] Business travel")

    # ── 15. Education Field vs Attrition ──────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    ef = raw.groupby("EducationField")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    ).sort_values(ascending=True)
    colors = [ACCENT_COLOR if v > 20 else SINGLE_COLOR for v in ef.values]
    ax.barh(ef.index, ef.values, color=colors, edgecolor="white")
    for i, val in enumerate(ef.values):
        ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontweight="bold", fontsize=10)
    ax.set_title("Attrition Rate by Education Field", fontweight="bold", fontsize=13)
    ax.set_xlabel("Attrition Rate (%)")
    save_fig(fig, "15_education_field.png")
    print("  [15/16] Education field")

    # ── 16. Environment Satisfaction vs Attrition ─────────────
    fig, ax = plt.subplots(figsize=(7, 5))
    es = raw.groupby("EnvironmentSatisfaction")["Attrition"].apply(
        lambda x: (x == "Yes").mean() * 100
    )
    ax.bar(es.index.astype(str), es.values, color=SINGLE_COLOR, width=0.5, edgecolor="white")
    for i, val in enumerate(es.values):
        ax.text(i, val + 0.5, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Attrition Rate by Environment Satisfaction", fontweight="bold", fontsize=13)
    ax.set_xlabel("Environment Satisfaction (1=Low, 4=High)")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, es.max() * 1.3)
    save_fig(fig, "18_environment_satisfaction.png")
    print("  [16/16] Environment satisfaction")

    print(f"\nEDA completed! {len(os.listdir(FIGURES_DIR))} figures saved to {FIGURES_DIR}/")


if __name__ == "__main__":
    run_eda()