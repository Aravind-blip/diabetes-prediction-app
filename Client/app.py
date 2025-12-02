import os
import time
import streamlit as st
import requests

# Backend URL from environment (Render) or local default
FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://localhost:8000")

st.title("Diabetes Prediction")

# --- Load dropdown options from backend ---
try:
    gender_response = requests.get(f"{FASTAPI_URL}/get-gender", timeout=10)
    smoking_response = requests.get(f"{FASTAPI_URL}/get-smoking", timeout=10)

    if gender_response.status_code == 200:
        genders = gender_response.json().get("gender", [])
    else:
        genders = []

    if smoking_response.status_code == 200:
        smoking_histories = smoking_response.json().get("smoking_history", [])
    else:
        smoking_histories = []

    # Fallbacks in case backend returns empty values
    if not genders:
        genders = ["Male", "Female"]
    if not smoking_histories:
        smoking_histories = ["never", "former", "current", "ever"]

except Exception as e:
    st.error(f"Failed to load dropdown options from backend: {e}")
    genders = ["Male", "Female"]
    smoking_histories = ["never", "former", "current", "ever"]

# --- Input form ---
with st.form("prediction_form"):
    age = st.number_input("Age", min_value=25.0, max_value=80.0, step=0.1, value=25.0)
    hypertension = 1 if st.radio("Hypertension", ["No", "Yes"], index=0) == "Yes" else 0
    heart_disease = 1 if st.radio("Heart Disease", ["No", "Yes"], index=0) == "Yes" else 0
    bmi = st.number_input("BMI", min_value=15.0, max_value=70.0, step=0.1, value=15.0)
    hba1c = st.number_input("HbA1c Level", min_value=3.5, max_value=9.0, step=0.1, value=3.5)
    blood_glucose = st.number_input("Blood Glucose Level", min_value=80, max_value=240, step=1, value=80)
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
            "smoking_history": smoking,
        }

        max_retries = 3
        delay_seconds = 5
        response = None

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(
                    f"{FASTAPI_URL}/get-prediction",
                    json=payload,
                    timeout=20,
                )

                # If backend is waking up / rate-limiting, retry
                if response.status_code == 429 or response.status_code == 503:
                    if attempt < max_retries:
                        st.warning(
                            f"Backend waking up (status {response.status_code}). "
                            f"Retrying... ({attempt}/{max_retries})"
                        )
                        time.sleep(delay_seconds)
                        continue
                break  # Got a non-429/503 response, exit loop

            except Exception as e:
                if attempt < max_retries:
                    st.warning(f"Error contacting backend ({e}). Retrying...")
                    time.sleep(delay_seconds)
                else:
                    st.error(f"Error contacting backend: {e}")
                    response = None

        if response is not None:
            if response.status_code == 200:
                result = response.json().get("Prediction", 0)
                label = "Diabetes Risk: YES" if int(result) == 1 else "Diabetes Risk: NO"
                st.success(label)
            else:
                st.error(f"Prediction request failed: {response.status_code}")
