import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(page_title="Prediction", page_icon="🧪", layout="wide")
st.title("🧪 Diabetes Prediction")

@st.cache_resource
def load_model():
    return joblib.load("models/xgb.pkl")

def build_input(form):
    return pd.DataFrame([{
        # Demographic & lifestyle
        "age": form["age"],
        "gender": form["gender"],
        "ethnicity": form["ethnicity"],
        "education_level": form["education_level"],
        "income_level": form["income_level"],
        "employment_status": form["employment_status"],
        "smoking_status": form["smoking_status"],
        "alcohol_consumption_per_week": form["alcohol_consumption_per_week"],
        "physical_activity_minutes_per_week": form["physical_activity_minutes_per_week"],
        "diet_score": form["diet_score"],
        "sleep_hours_per_day": form["sleep_hours_per_day"],
        "screen_time_hours_per_day": form["screen_time_hours_per_day"],
        # History
        "family_history_diabetes": int(form["family_history_diabetes"]),
        "hypertension_history": int(form["hypertension_history"]),
        "cardiovascular_history": int(form["cardiovascular_history"]),
        # Clinical
        "bmi": form["bmi"],
        "waist_to_hip_ratio": form["waist_to_hip_ratio"],
        "systolic_bp": form["systolic_bp"],
        "diastolic_bp": form["diastolic_bp"],
        "heart_rate": form["heart_rate"],
        "cholesterol_total": form["cholesterol_total"],
        "hdl_cholesterol": form["hdl_cholesterol"],
        "ldl_cholesterol": form["ldl_cholesterol"],
        "triglycerides": form["triglycerides"],
        "glucose_fasting": form["glucose_fasting"],
        "glucose_postprandial": form["glucose_postprandial"],
        "insulin_level": form["insulin_level"],
        "hba1c": form["hba1c"],
    }])

try:
    model = load_model()
except Exception as e:
    st.error(f"Failed to load model at models/xgb.pkl: {e}")
    st.stop()

with st.form("predict"):
    st.subheader("Enter Patient Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", 18, 100, 45)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        ethnicity = st.selectbox("Ethnicity", ["Asian", "White", "Hispanic", "Black", "Other"])
        education_level = st.selectbox("Education Level", ["No formal", "Highschool", "Graduate", "Postgraduate"])
        income_level = st.selectbox("Income Level", ["Low", "Lower-Middle", "Middle", "Upper-Middle", "High"])
        employment_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Retired", "Student"])
    with c2:
        smoking_status = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
        alcohol_consumption_per_week = st.number_input("Alcohol (drinks/week)", 0, 50, 2)
        physical_activity_minutes_per_week = st.number_input("Physical Activity (min/week)", 0, 1500, 150)
        diet_score = st.slider("Diet Score (0-10)", 0.0, 10.0, 6.0, 0.1)
        sleep_hours_per_day = st.slider("Sleep Hours/Day", 3.0, 12.0, 7.0, 0.1)
        screen_time_hours_per_day = st.slider("Screen Time (hrs/day)", 0.0, 16.0, 6.0, 0.1)
        family_history_diabetes = st.checkbox("Family History of Diabetes")
        hypertension_history = st.checkbox("Hypertension History")
        cardiovascular_history = st.checkbox("Cardiovascular Disease History")
    with c3:
        bmi = st.number_input("BMI", 10.0, 60.0, 26.0, 0.1)
        waist_to_hip_ratio = st.number_input("Waist-to-Hip Ratio", 0.5, 1.2, 0.86, 0.01)
        heart_rate = st.number_input("Heart Rate (bpm)", 40, 140, 70)
        systolic_bp = st.number_input("Systolic BP", 80, 220, 120)
        diastolic_bp = st.number_input("Diastolic BP", 40, 130, 80)
        cholesterol_total = st.number_input("Total Cholesterol", 80, 400, 185)
        hdl_cholesterol = st.number_input("HDL", 10, 120, 50)
        ldl_cholesterol = st.number_input("LDL", 30, 250, 103)
        triglycerides = st.number_input("Triglycerides", 30, 800, 150)
        glucose_fasting = st.number_input("Fasting Glucose", 60, 300, 110)
        glucose_postprandial = st.number_input("Post-meal Glucose", 60, 400, 160)
        insulin_level = st.number_input("Insulin (µU/mL)", 2.0, 60.0, 10.0, 0.1)
        hba1c = st.number_input("HbA1c (%)", 4.0, 15.0, 6.2, 0.1)

    submitted = st.form_submit_button("🔍 Predict", use_container_width=True)

if submitted:
    X_input = build_input({
        "age": age, "gender": gender, "ethnicity": ethnicity, "education_level": education_level,
        "income_level": income_level, "employment_status": employment_status, "smoking_status": smoking_status,
        "alcohol_consumption_per_week": alcohol_consumption_per_week,
        "physical_activity_minutes_per_week": physical_activity_minutes_per_week,
        "diet_score": diet_score, "sleep_hours_per_day": sleep_hours_per_day,
        "screen_time_hours_per_day": screen_time_hours_per_day,
        "family_history_diabetes": family_history_diabetes, "hypertension_history": hypertension_history,
        "cardiovascular_history": cardiovascular_history, "bmi": bmi, "waist_to_hip_ratio": waist_to_hip_ratio,
        "systolic_bp": systolic_bp, "diastolic_bp": diastolic_bp, "heart_rate": heart_rate,
        "cholesterol_total": cholesterol_total, "hdl_cholesterol": hdl_cholesterol,
        "ldl_cholesterol": ldl_cholesterol, "triglycerides": triglycerides,
        "glucose_fasting": glucose_fasting, "glucose_postprandial": glucose_postprandial,
        "insulin_level": insulin_level, "hba1c": hba1c
    })

    try:
        pred = int(model.predict(X_input)[0])
        prob = model.predict_proba(X_input)[0][1] if hasattr(model, "predict_proba") else None
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    st.markdown("---")
    st.subheader("Result")
    colA, colB = st.columns([1,1])
    with colA:
        if pred == 1:
            st.error("Prediction: Diabetes (1)")
        else:
            st.success("Prediction: No Diabetes (0)")
    with colB:
        if prob is not None:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=float(prob*100),
                title={'text': "Risk Probability (%)"},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "red" if prob >= 0.7 else "orange" if prob >= 0.4 else "green"},
                       'steps': [
                           {'range': [0, 40], 'color': "lightgreen"},
                           {'range': [40, 70], 'color': "yellow"},
                           {'range': [70, 100], 'color': "lightcoral"},
                       ]}
            ))
            st.plotly_chart(gauge, use_container_width=True)

    st.markdown("---")
    if pred == 1:
        st.subheader("✅ Next Steps & Advice")
        st.write("- Consult a healthcare professional for confirmatory testing and a care plan.")
        st.write("- Adopt a balanced diet rich in vegetables, whole grains, and lean protein.")
        st.write("- Aim for ≥150 minutes/week of moderate physical activity, as medically appropriate.")
        st.write("- Monitor blood glucose and HbA1c per medical advice.")
        st.write("- Address comorbidities (hypertension, dyslipidemia, obesity) with a clinician.")
        st.write("- If smoking, seek support for cessation; limit alcohol consumption.")
        st.info("This tool is for educational support and does not replace medical diagnosis.")
    else:
        st.subheader("🎉 Positive News")
        st.write("Your risk appears low based on the current inputs.")
        st.write("Keep up healthy habits: regular exercise, balanced diet, sufficient sleep, and periodic checkups.")
        st.balloons()
