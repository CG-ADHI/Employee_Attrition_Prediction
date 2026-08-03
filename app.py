import streamlit as st
import pandas as pd
import joblib
import numpy as np
from src.predictor import AttritionPredictor

predictor = AttritionPredictor()

st.set_page_config(
    page_title="Employee Attrition Prediction",
    page_icon="📊",
    layout="wide"
)

model = joblib.load("models/random_forest.pkl")
df = pd.read_csv("data/processed_attrition.csv")

st.title("📊 Employee Attrition Prediction System")
st.markdown("### HR Analytics Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Dashboard",
        "👤 Employee Details",
        "📈 Analytics",
        "⭐ Feature Importance",
        "📄 Report"
    ]
)

if page == "🏠 Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Employees", "1470")

    with col2:
        st.metric("Features", "35")

    with col3:
        st.metric("Models", "2")

    st.info("Use the sidebar to navigate through the application.")

elif page == "👤 Employee Details":

    st.header("Employee Information")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input("Age", 18, 60, 30)

        department = st.selectbox(
            "Department",
            [
                "Sales",
                "Research & Development",
                "Human Resources"
            ]
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        monthly_income = st.number_input(
            "Monthly Income",
            1000,
            500000,
            40000
        )

        overtime = st.selectbox(
            "OverTime",
            [
                "No",
                "Yes"
            ]
        )

    with col2:

        years_company = st.number_input(
            "Years At Company",
            0,
            40,
            5
        )

        worklife = st.slider(
            "Work Life Balance",
            1,
            4,
            3
        )

        satisfaction = st.slider(
            "Job Satisfaction",
            1,
            4,
            3
        )

        distance = st.number_input(
            "Distance From Home",
            1,
            50,
            10
        )

        jobrole = st.selectbox(
            "Job Role",
            [
                "Sales Executive",
                "Research Scientist",
                "Laboratory Technician",
                "Manager",
                "Healthcare Representative",
                "Manufacturing Director",
                "Sales Representative",
                "Research Director",
                "Human Resources"
            ]
        )

    predict = st.button(
        "Predict Attrition",
        use_container_width=True
    )

    if predict:

        sample = df.drop("Attrition", axis=1).iloc[[0]]

        prediction = model.predict(sample)[0]
        probability = model.predict_proba(sample)[0][1]

        st.divider()

        st.subheader("Prediction Result")

        if prediction == 1:
            st.error("🔴 Employee is likely to Leave")
        else:
            st.success("🟢 Employee is likely to Stay")

        st.metric(
            "Attrition Probability",
            f"{probability*100:.2f}%"
        )

        if probability < 0.30:
            st.success("🟢 Risk Level : LOW")

        elif probability < 0.60:
            st.warning("🟡 Risk Level : MEDIUM")

        else:
            st.error("🔴 Risk Level : HIGH")

        st.subheader("Top Risk Factors")

        factors = []

        if overtime == "Yes":
            factors.append("• Overtime")

        if satisfaction <= 2:
            factors.append("• Low Job Satisfaction")

        if monthly_income < 40000:
            factors.append("• Low Monthly Income")

        if years_company < 5:
            factors.append("• Short Company Tenure")

        if distance > 20:
            factors.append("• Long Distance From Home")

        if len(factors) == 0:
            st.success("No major risk factors detected.")
        else:
            for item in factors:
                st.write(item)

elif page == "📈 Analytics":

    st.header("Analytics Dashboard")

    st.info("Charts will be added in Part 3.")

elif page == "⭐ Feature Importance":

    st.header("Feature Importance")

    st.info("Feature Importance will be added in Part 4.")

elif page == "📄 Report":

    st.header("Report")

    st.info("Download Report will be added in Part 5.")