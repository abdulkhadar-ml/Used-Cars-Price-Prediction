import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Page configuration
st.set_page_config(page_title="Used Car Price Predictor", page_icon="🚗", layout="wide")

# Load model and scaler
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Header
st.title("🚗 RideRepublic")
st.markdown("### PREDICT  YOUR  CAR  AT  THE  BEST  PRICE ")
st.markdown("---")

# Sidebar Inputs
st.sidebar.header("Enter Car Details")

year = st.sidebar.number_input("Year", 2000, 2025, 2018)
km_driven = st.sidebar.number_input("KM Driven", 0, 300000, 40000)
mileage = st.sidebar.number_input("Mileage (km/l)", 5.0, 40.0, 18.0)
engine = st.sidebar.number_input("Engine (CC)", 800, 5000, 1500)
seats = st.sidebar.number_input("Seats", 2, 10, 5)

owner = st.sidebar.selectbox(
    "Owner Type",
    ["First Owner","Second Owner","Third Owner","Fourth & Above Owner"]
)

owner_mapping = {
    "First Owner":0,
    "Second Owner":1,
    "Third Owner":2,
    "Fourth & Above Owner":3
}

owner = owner_mapping[owner]

brand = st.sidebar.selectbox("Brand", [
    "BMW","Chevrolet","Ford","Honda","Hyundai",
    "Mahindra","Maruti","Mercedes-Benz","Nissan",
    "Renault","Skoda","Tata","Toyota","Other"
])

fuel = st.sidebar.selectbox("Fuel", ["Diesel","Petrol","LPG"])
transmission = st.sidebar.selectbox("Transmission", ["Manual","Automatic"])
seller_type = st.sidebar.selectbox("Seller Type", ["Individual","Trustmark Dealer"])

# Main prediction section
st.subheader("Prediction Result")

if st.button("Predict Price 🚀"):

    with st.spinner("Analyzing car data..."):

        input_df = pd.DataFrame(columns=model.feature_names_in_)
        input_df.loc[0] = 0

        input_df.at[0,'year'] = year
        input_df.at[0,'km_driven'] = km_driven
        input_df.at[0,'mileage(km/ltr/kg)'] = mileage
        input_df.at[0,'engine'] = engine
        input_df.at[0,'seats'] = seats
        input_df.at[0,'owner'] = owner

        brand_col = f"brand_{brand}"
        fuel_col = f"fuel_{fuel}"
        transmission_col = f"transmission_{transmission}"
        seller_col = f"seller_type_{seller_type}"

        if brand_col in input_df.columns:
            input_df.at[0,brand_col] = 1

        if fuel_col in input_df.columns:
            input_df.at[0,fuel_col] = 1

        if transmission_col in input_df.columns:
            input_df.at[0,transmission_col] = 1

        if seller_col in input_df.columns:
            input_df.at[0,seller_col] = 1

        numeric_cols = ['year','km_driven','mileage(km/ltr/kg)','engine','seats']
        input_df[numeric_cols] = scaler.teransform(input_df[numeric_cols])

        y_log = model.predict(input_df)
        y_actual = np.exp(y_log)

        price = round(y_actual[0],0)

        # Price range estimate
        low = round(price*0.9)
        high = round(price*1.1)

        st.success(f"💰 Estimated Price: ₹ {price}")

        st.metric("Expected Price Range", f"₹{low} - ₹{high}")

st.markdown("---")

# Information Section
st.subheader("About This Model")

st.write("""
RideRepublic is an AI-powered car valuation platform that estimates the resale price of used cars based on key vehicle attributes. The machine learning model is trained using Linear Regression which analyzes factors such as manufacturing year, kilometers driven, mileage, engine capacity, fuel type, transmission, brand, and ownership history to predict the approximate market value of a vehicle.
        
RideRepublic © 2026

NOTE: Predictions are estimates and actual market prices may vary depending on vehicle condition, location and demand.
""")

st.markdown("---")

# Footer
st.caption("Technology Stack:  Python • Scikit-Learn • Streamlit")
