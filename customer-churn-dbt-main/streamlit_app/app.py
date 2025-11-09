import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Placeholder for loading model and scaler
# In a real scenario, these would be loaded from the ml/ directory
try:
    with open('ml/churn_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('ml/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    model_loaded = True
except FileNotFoundError:
    st.warning("ML model or scaler not found. Please run `python ml/train_model.py` first.")
    model_loaded = False
    model = None
    scaler = None

st.set_page_config(page_title="Customer Churn Prediction Dashboard", layout="wide")

st.title("Customer Churn Prediction and Analytics")

st.markdown("""
This dashboard provides insights into customer churn and allows for real-time prediction.
""")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard Overview", "Predict Churn"])

if page == "Dashboard Overview":
    st.header("Dashboard Overview")
    st.write("This section would display various analytics and visualizations related to churn.")

    st.subheader("Churn Probability Distribution (Placeholder)")
    # Placeholder for a histogram or density plot of churn probabilities
    st.bar_chart(pd.DataFrame({'Churn Probability': np.random.rand(100)}).groupby(pd.cut(pd.DataFrame({'Churn Probability': np.random.rand(100)})['Churn Probability'], 10)).count())

    st.subheader("Feature Importance (Placeholder)")
    # Placeholder for feature importance chart
    st.bar_chart(pd.DataFrame({'Feature': ['Contract Type', 'Monthly Spend', 'Days Since Payment', 'Tenure'], 'Importance': [0.3, 0.25, 0.2, 0.15]}))

elif page == "Predict Churn":
    st.header("Predict Churn for a New Customer")

    if not model_loaded:
        st.error("Cannot predict churn: ML model or scaler not loaded. Please ensure `ml/churn_model.pkl` and `ml/scaler.pkl` exist.")
    else:
        with st.form("churn_prediction_form"):
            st.subheader("Customer Information")
            gender = st.selectbox("Gender", ["Male", "Female"])
            contract_type = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            monthly_spend = st.number_input("Average Monthly Spend", min_value=0.0, value=50.0)
            days_since_payment = st.number_input("Days Since Last Payment", min_value=0, value=30)
            tenure = st.number_input("Customer Tenure (months)", min_value=0, value=12)

            submitted = st.form_submit_button("Predict Churn")

            if submitted:
                # Create a DataFrame for prediction
                input_data = pd.DataFrame([{
                    'gender': gender,
                    'contract_type': contract_type,
                    'avg_monthly_spend': monthly_spend,
                    'days_since_payment': days_since_payment,
                    'tenure': tenure
                }])

                # Apply one-hot encoding for categorical features
                input_data_encoded = pd.get_dummies(input_data, columns=['gender', 'contract_type'], drop_first=True)

                # Ensure all expected columns are present, fill missing with 0
                # This is a simplified approach; in a real app, you'd align with training features
                expected_features = ['avg_monthly_spend', 'days_since_payment', 'tenure',
                                     'gender_Male', 'contract_type_One year', 'contract_type_Two year']
                for feature in expected_features:
                    if feature not in input_data_encoded.columns:
                        input_data_encoded[feature] = 0

                # Reorder columns to match training data (important for scaler and model)
                # This assumes a specific order from train_model.py; adjust as needed
                input_data_processed = input_data_encoded[expected_features]

                # Scale the input data
                scaled_input = scaler.transform(input_data_processed)

                # Make prediction
                churn_probability = model.predict_proba(scaled_input)[:, 1][0]
                churn_prediction = model.predict(scaled_input)[0]

                st.subheader("Prediction Result")
                if churn_prediction == 1:
                    st.error(f"This customer is likely to churn with a probability of {churn_probability:.2f}")
                else:
                    st.success(f"This customer is unlikely to churn with a probability of {churn_probability:.2f}")

                st.write(f"Raw Churn Probability: {churn_probability:.4f}")
