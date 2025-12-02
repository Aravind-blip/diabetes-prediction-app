import os
import streamlit as st
import requests

FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000")

st.title("Diabetes Prediction")

# Fetch dropdown options
gender_response = requests.get(f"{FASTAPI_URL}/get-gender")
smoking_response = requests.get(f"{FASTAPI_URL}/get-smoking")

if gender_response.status_code == 200 and smoking_response.status_code == 200:
    genders = gender_response.json().get("gender", [])
    smoking_histories = smoking_response.json().get("smoking_history", [])

    if isinstance(genders, str):
        genders = [genders]
    if isinstance(smoking_histories, str):
        smoking_histories = [smoking_histories]
else:
    st.error("Failed to load gender or smoking history options.")
    st.stop()

# Input form
with st.form("prediction_form"):
    age = st.number_input("Age", min_value=25.0, max_value=80.0, step=0.1)
    hypertension = 1 if st.radio("Hypertension", ["No", "Yes"]) == "Yes" else 0
    heart_disease = 1 if st.radio("Heart Disease", ["No", "Yes"]) == "Yes" else 0
    bmi = st.number_input("BMI", min_value=15.0, max_value=70.0, step=0.1)
    hba1c = st.number_input("HbA1c Level", min_value=3.5, max_value=9.0, step=0.1)
    blood_glucose = st.number_input("Blood Glucose Level", min_value=80, max_value=240, step=1)
    gender = st.selectbox("Gender", genders)
    smoking = st.selectbox("Smoking History", smoking_histories)

    submit = st.form_submit_button("Predict")

    if submit:
        payload = {
            "age": age,
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "bmi": bmi,
            "HbA1c_level": hba1c,
            "blood_glucose_level": blood_glucose,
            "gender": gender,
            "smoking_history": smoking
        }

        response
