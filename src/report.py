import os
import sys
import pandas as pd
import numpy as np
import joblib
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_report():
    """
    Generate a professional Executive HR Report PDF.
    Includes: Top 3 drivers, department breakdown, recommendations, model metrics.
    """

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Heading1"],
        alignment=TA_CENTER, fontSize=22, spaceAfter=6,
        textColor=HexColor("#1a1a2e"),
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        alignment=TA_CENTER, fontSize=11,
        textColor=HexColor("#666666"), spaceAfter=24,
    )
    heading_style = ParagraphStyle(
        "CustomHeading", parent=styles["Heading2"],
        fontSize=14, textColor=HexColor("#1a1a2e"),
        spaceBefore=16, spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "CustomBody", parent=styles["BodyText"],
        fontSize=10, leading=14, spaceAfter=6,
        textColor=HexColor("#333333"),
    )
    bullet_style = ParagraphStyle(
        "Bullet", parent=body_style,
        leftIndent=20, bulletIndent=10,
    )

    # Load data
    raw = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")
    metrics = joblib.load("models/metrics.pkl")
    rf_model = joblib.load("models/random_forest.pkl")
    features = joblib.load("models/features.pkl")

    # Feature importance
    importance = pd.DataFrame({
        "Feature": features,
        "Importance": rf_model.feature_importances_,
    }).sort_values("Importance", ascending=False)
    top3 = importance.head(3)

    # Department stats
    dept_stats = raw.groupby("Department").agg(
        Total=("Attrition", "count"),
        Left=("Attrition", lambda x: (x == "Yes").sum()),
    )
    dept_stats["Rate"] = (dept_stats["Left"] / dept_stats["Total"] * 100).round(1)

    # Watchlist stats
    watchlist = pd.read_csv("reports/at_risk_employees.csv")
    high_risk = (watchlist["Risk_Level"] == "HIGH").sum()
    medium_risk = (watchlist["Risk_Level"] == "MEDIUM").sum()

    # ── Build Document ────────────────────────────────────────
    doc = SimpleDocTemplate(
        "reports/HR_Report.pdf",
        pagesize=A4,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    story = []

    # Title
    story.append(Spacer(1, 30))
    story.append(Paragraph("Employee Attrition", title_style))
    story.append(Paragraph("Predictive Analytics Report", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Prepared for: HR Leadership Team", subtitle_style))
    story.append(Paragraph("Prepared by: People Analytics Division", subtitle_style))
    story.append(Spacer(1, 30))

    # ── Executive Summary ─────────────────────────────────────
    story.append(Paragraph("Executive Summary", heading_style))
    total = len(raw)
    left = (raw["Attrition"] == "Yes").sum()
    rate = left / total * 100
    story.append(Paragraph(
        f"Analysis of <b>{total}</b> employees reveals an overall attrition rate of "
        f"<b>{rate:.1f}%</b> ({left} employees). Using machine learning models trained "
        f"on 44 workforce features, we identified the key drivers of attrition and "
        f"created a risk-scoring system. Currently <b>{high_risk}</b> employees are "
        f"classified as HIGH risk and <b>{medium_risk}</b> as MEDIUM risk.",
        body_style,
    ))
    story.append(Spacer(1, 12))

    # ── Dataset Overview ──────────────────────────────────────
    story.append(Paragraph("Dataset Overview", heading_style))
    data_table = Table([
        ["Metric", "Value"],
        ["Total Employees", str(total)],
        ["Total Features", "35 (raw) / 44 (engineered)"],
        ["Attrition (Yes)", f"{left} ({rate:.1f}%)"],
        ["Attrition (No)", f"{total - left} ({100 - rate:.1f}%)"],
        ["Missing Values", "0"],
    ], colWidths=[200, 250])
    data_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(data_table)
    story.append(Spacer(1, 16))

    # ── Top 3 Drivers of Attrition ────────────────────────────
    story.append(Paragraph("Top 3 Drivers of Attrition", heading_style))
    story.append(Paragraph(
        "The following features have the highest predictive importance in "
        "determining whether an employee will leave:",
        body_style,
    ))

    driver_map = {
        "MonthlyIncome": (
            "Monthly Income",
            "Lower-income employees are significantly more likely to leave. "
            "Compensation reviews should target employees below the median income in their role."
        ),
        "Age": (
            "Age",
            "Younger employees (under 30) show higher attrition rates. "
            "Early-career engagement and mentoring programs can help retain this demographic."
        ),
        "TotalWorkingYears": (
            "Total Working Years",
            "Employees with fewer total working years are more likely to leave. "
            "This correlates with career-stage transitions and market competitiveness."
        ),
        "OverTime": (
            "OverTime",
            "Employees working overtime leave at 3x the rate of those who don't. "
            "Workload balancing and overtime policies need urgent review."
        ),
        "DailyRate": (
            "Daily Rate",
            "Variation in daily compensation rates correlates with attrition. "
            "Pay equity audits are recommended."
        ),
        "DistanceFromHome": (
            "Distance From Home",
            "Longer commutes correlate with higher attrition. "
            "Remote work or flexible commuting options could improve retention."
        ),
    }

    for i, (_, row) in enumerate(top3.iterrows(), 1):
        feat = row["Feature"]
        imp_val = row["Importance"]
        name, desc = driver_map.get(feat, (feat, "This feature significantly impacts attrition risk."))
        story.append(Paragraph(
            f"<b>{i}. {name}</b> (Importance: {imp_val:.4f})", body_style
        ))
        story.append(Paragraph(desc, bullet_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))

    # ── Department Breakdown ──────────────────────────────────
    story.append(Paragraph("Risk Breakdown by Department", heading_style))

    dept_table_data = [["Department", "Total", "Left", "Attrition Rate"]]
    for dept, row in dept_stats.iterrows():
        dept_table_data.append([dept, str(row["Total"]), str(row["Left"]), f"{row['Rate']}%"])

    dept_table = Table(dept_table_data, colWidths=[160, 80, 80, 100])
    dept_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(dept_table)
    story.append(Spacer(1, 16))

    # ── Model Performance ─────────────────────────────────────
    story.append(Paragraph("Model Performance", heading_style))

    model_table_data = [["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"]]
    for model_name, m in metrics.items():
        model_table_data.append([
            model_name,
            f"{m['accuracy']:.2%}",
            f"{m['precision']:.2%}",
            f"{m['recall']:.2%}",
            f"{m['f1']:.2%}",
            f"{m['roc_auc']:.2%}",
        ])

    model_table = Table(model_table_data, colWidths=[130, 70, 70, 60, 50, 70])
    model_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f8f9fa")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(model_table)
    story.append(Spacer(1, 16))

    # ── Retention Recommendations ─────────────────────────────
    story.append(Paragraph("Retention Strategy Recommendations", heading_style))

    recommendations = [
        ("<b>1. Compensation Review Program</b>",
         "Monthly Income is the strongest predictor of attrition. Conduct a market-rate "
         "salary benchmarking exercise. Prioritize adjustments for employees in the "
         "bottom quartile of their role's pay band."),
        ("<b>2. Overtime Policy Reform</b>",
         "Employees working overtime leave at nearly 3x the rate of non-overtime workers. "
         "Implement strict overtime caps, hire additional staff for high-demand periods, "
         "and introduce compensatory time-off policies."),
        ("<b>3. Early-Career Engagement</b>",
         "Attrition peaks in the first 2 years of employment. Implement structured "
         "onboarding programs, assign mentors, and conduct 90-day check-ins to address "
         "early disengagement."),
        ("<b>4. Remote Work &amp; Flexibility</b>",
         "Distance from home is a significant attrition factor. Offer hybrid work "
         "arrangements for roles that permit it, and consider commuter benefits for "
         "on-site positions."),
        ("<b>5. Career Development Pathways</b>",
         "Employees with fewer total working years and lower job levels are at higher risk. "
         "Create visible career progression frameworks and invest in training programs."),
    ]

    for title, desc in recommendations:
        story.append(Paragraph(title, body_style))
        story.append(Paragraph(desc, bullet_style))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 16))

    # ── Risk Summary ──────────────────────────────────────────
    story.append(Paragraph("At-Risk Employee Summary", heading_style))
    story.append(Paragraph(
        f"A complete watch list has been generated with risk scores for all {total} employees. "
        f"The breakdown is as follows:",
        body_style,
    ))

    risk_table = Table([
        ["Risk Level", "Count", "Action"],
        ["HIGH", str(high_risk), "Immediate intervention required"],
        ["MEDIUM", str(medium_risk), "Monitor closely, schedule 1-on-1s"],
        ["LOW", str(total - high_risk - medium_risk), "Maintain engagement"],
    ], colWidths=[80, 60, 280])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("BACKGROUND", (0, 1), (-1, 1), HexColor("#ffe6e6")),
        ("BACKGROUND", (0, 2), (-1, 2), HexColor("#fff9e6")),
        ("BACKGROUND", (0, 3), (-1, 3), HexColor("#e6f7e6")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(risk_table)

    # ── Build PDF ─────────────────────────────────────────────
    doc.build(story)
    print("\nExecutive HR Report generated: reports/HR_Report.pdf")


if __name__ == "__main__":
    generate_report()