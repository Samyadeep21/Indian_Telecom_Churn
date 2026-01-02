import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px  # Professional interactive plotting

# Load Assets
model = pickle.load(open('indian_churn_model.pkl', 'rb'))
partner_le = pickle.load(open('partner_encoder.pkl', 'rb'))

st.set_page_config(page_title="Bharat Telco Retention AI", layout="wide")
st.title("🇮🇳 Bharat Telco: Customer Retention Dashboard")

# Sidebar for Market Context - Professional placement move!
with st.sidebar:
    st.header("🏢 Indian Telecom Market 2026")
    st.info("""
    **Current Trends:**
    - 5G Adoption: 75% coverage in Tier 1 cities.
    - Churn Driver: Pricing war & data-heavy OTT bundles.
    - Average Revenue: Rising by 12% YoY.
    """)

# Main UI Inputs
col1, col2 = st.columns(2)
with col1:
    age = st.slider("Customer Age", 18, 90, 30)
    salary = st.number_input("Estimated Monthly Salary (₹)", 10000, 500000, 45000)
    partner = st.selectbox("Telecom Partner", partner_le.classes_)
with col2:
    calls = st.number_input("Calls Made (Last Month)", 0, 5000, 300)
    data = st.number_input("Data Used (GB)", 0, 500, 20)
    sms = st.number_input("SMS Sent", 0, 1000, 50)

# Prediction Logic
partner_encoded = partner_le.transform([partner])[0]
input_df = pd.DataFrame([[age, salary, calls, sms, data, partner_encoded]], 
                        columns=['age', 'estimated_salary', 'calls_made', 'sms_sent', 'data_used', 'telecom_partner'])

if st.button("Analyze Risk", use_container_width=True):
    prob = model.predict_proba(input_df)[0][1]
    
    # Using Containers for clean grouping
    with st.container(border=True):
        st.subheader(f"Churn Probability: {prob:.2%}")
        
        if prob > 0.6:
            st.error("🚨 HIGH RISK CUSTOMER")
            st.info("💡 **Strategy:** Offer unlimited data loyalty pack.")
        elif prob > 0.3:
            st.warning("⚠️ MODERATE RISK")
            st.info("💡 **Strategy:** Send SMS for new 5G trial plans.")
        else:
            st.success("✅ LOYAL CUSTOMER")

    # IMPROVED: Interactive Feature Importance Chart
    st.divider()
    st.subheader("📊 Why this score?")
    
    importances = model.feature_importances_
    features = input_df.columns
    imp_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values('Importance', ascending=True)

    fig = px.bar(imp_df, x='Importance', y='Feature', orientation='h',
                 title='Key Factors Influencing AI Decision',
                 color='Importance', color_continuous_scale='Viridis',
                 template='plotly_dark') # Matching dark theme
    
    st.plotly_chart(fig, use_container_width=True) # Makes it responsive

    # ADDED: Market Context and Business Impact Section
    with st.expander("📈 See Business Impact & Market Context"):
        st.markdown(f"""
        - **Impact:** Reducing churn for customers like this could save an estimated **₹{int(salary * 0.1)}/year**.
        - **Market Insight:** In India, '{partner}' customers are currently highly sensitive to '{features[np.argmax(importances)]}'.
        - **Retention Value:** High-usage customers are 3x more likely to refer others.
        """)
        