import streamlit as st
import requests

# عنوان التطبيق
st.title("❤️ Heart Disease Risk Prediction")

st.write("Fill in the patient information below and click **Predict** to get the risk estimation.")

# ---------------------- Inputs ---------------------- #

# 1) age (numeric)
age = st.number_input("Age", min_value=1, max_value=120, value=50, step=1)

# 2) sex (binary)
sex = st.selectbox("Sex (0 = Female, 1 = Male)", options=[0, 1], index=1)

# 3) ChestPain (categorical coded as numbers)
ChestPain = st.selectbox("Chest Pain Type (0–3)", options=[0, 1, 2, 3], index=0)

# 4) RestBloodPressure
RestBloodPressure = st.number_input("Resting Blood Pressure (mm Hg)", min_value=60, max_value=250, value=120, step=1)

# 5) chol (cholesterol)
chol = st.number_input("Cholesterol (mg/dl)", min_value=80, max_value=700, value=200, step=1)

# 6) FastingBloodSugar (0/1)
FastingBloodSugar = st.selectbox("Fasting Blood Sugar > 120 mg/dl (1 = Yes, 0 = No)", options=[0, 1], index=0)

# 7) restecg (0–2)
restecg = st.selectbox("Resting ECG Results (0–2)", options=[0, 1, 2], index=0)

# 8) thalach (max heart rate)
thalach = st.number_input("Maximum Heart Rate Achieved", min_value=50, max_value=250, value=150, step=1)

# 9) exang (exercise induced angina)
exang = st.selectbox("Exercise Induced Angina (1 = Yes, 0 = No)", options=[0, 1], index=0)

# 10) oldpeak (ST depression)
oldpeak = st.number_input("Oldpeak (ST depression induced by exercise)", min_value=-5.0, max_value=10.0, value=1.0, step=0.1)

# 11) slope (0–2)
slope = st.selectbox("Slope of Peak Exercise ST Segment (0–2)", options=[0, 1, 2], index=1)

# 12) ca (number of major vessels, 0–4)
ca = st.selectbox("Number of Major Vessels Colored by Flourosopy (0–4)", options=[0, 1, 2, 3, 4], index=0)

# 13) thal (0–3 typically)
thal = st.selectbox("Thalassemia (0–3 coded)", options=[0, 1, 2, 3], index=1)

# 14) smoking (0/1)
smoking = st.selectbox("Smoking (1 = Yes, 0 = No)", options=[0, 1], index=0)

# 15) diabetes (0/1)
diabetes = st.selectbox("Diabetes (1 = Yes, 0 = No)", options=[0, 1], index=0)

# 16) bmi (numeric)
bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=60.0, value=25.0, step=0.1)

# API endpoint
API_URL = "http://127.0.0.1:5000/predict"

# ---------------------- Predict Button ---------------------- #

if st.button("Predict"):

    # ترتيب الـ features لازم يكون بنفس ترتيب التدريب:
    features = [
        age,
        sex,
        ChestPain,
        RestBloodPressure,
        chol,
        FastingBloodSugar,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal,
        smoking,
        diabetes,
        bmi
    ]

    try:
        # إرسال الطلب للـ Flask API
        response = requests.post(API_URL, json={"features": features})

        st.write("Status code:", response.status_code)   # مفيد لو في Error

        if response.status_code == 200:
            data = response.json()
            pred = data.get("prediction")
            prob = data.get("risk_probability")

            if pred is not None and prob is not None:
                label = "🟥 High Risk (Heart Disease)" if pred == 1 else "🟩 Low Risk (No Heart Disease)"
                st.subheader(label)
                st.write(f"**Risk Probability:** {prob:.2f}")
            else:
                st.error("API did not return expected keys. Check API implementation.")
        else:
            st.error(f"API returned an error: {response.text}")

    except Exception as e:
        st.error(f"Error contacting API: {e}")
