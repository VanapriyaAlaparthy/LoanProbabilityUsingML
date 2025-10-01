import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Loan Approval Probability Checker")
st.write("Enter all details below:")

# --- Dynamic text inputs for all fields ---
gender = st.text_input("Gender")
married = st.text_input("Married")
dependents = st.text_input("Dependents")
education = st.text_input("Education")
self_emp = st.text_input("Self Employed")
app_income = st.number_input("Applicant Income", min_value=0, step=100)
coapp_income = st.number_input("Coapplicant Income", min_value=0, step=100)
loan_amount = st.number_input("Loan Amount", min_value=0, step=10)
loan_term = st.number_input("Loan Term (months)", min_value=0, step=1)
credit_history = st.text_input("Credit History")
property_area = st.text_input("Property Area")
age = st.number_input("Age", min_value=18, step=1)
has_credit_card = st.text_input("Has Credit Card")

if st.button("Check Probability"):
    payload = {
        "gender": gender.strip(),
        "married": married.strip(),
        "dependents": dependents.strip(),
        "education": education.strip(),
        "self_employed": self_emp.strip(),
        "applicantincome": app_income,
        "coapplicantincome": coapp_income,
        "loanamount": loan_amount,
        "loan_amount_term": loan_term,
        "credit_history": credit_history.strip(),
        "property_area": property_area.strip(),
        "age": age,
        "has_credit_card": has_credit_card.strip()
    }

    try:
        res = requests.post(f"{API_URL}/predict", json=payload)
        if res.ok:
            result = res.json()
            approval_prob = result.get("probability", None)
            if approval_prob is not None:
                st.info(f"Loan Approval Probability: {approval_prob}%")
                st.warning(f"Loan Disapproval Probability: {round(100 - approval_prob, 2)}%")
            else:
                st.error("Backend did not return probability.")
        else:
            st.error(f"API error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
