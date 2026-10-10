import streamlit as st
import pandas as pd
import numpy as np
import pickle as pk
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

model = pk.load(open('carprice_charges.pkl', 'rb'))
scaler = pk.load(open('scaler.pkl', 'rb'))
df = pd.read_csv('../../datasets/Car Dataset Processed.csv')

st.title("🚗 CAR PRICE PREDICTOR")
st.caption("Fill in the vehicle specifications below to estimate the market value.")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.subheader("📋 General Information")
        if 'brand' in df.columns:
            CarBrand = st.selectbox('Car Brand', df['brand'].unique())
        elif 'name' in df.columns:
            CarBrand = st.selectbox('Car Brand', df['name'].unique())
        else:
            CarBrand = st.selectbox('Car Brand', ['Maruti', 'Hyundai', 'Honda', 'Toyota', 'Ford', 'Mahindra', 'Tata', 'BMW', 'Audi'])
        CarManufacturedYear = st.slider('Car Manufactured Year', 2000, 2026, 2020)
        KmsDriven = st.slider('No Of Kms Driven', 0, 100000, 15000)
        
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            Fuel = st.selectbox('Fuel Type', df['fuel_type'].unique())
            Seats = st.selectbox('No Of Seats', df['seats'].unique())
        with sub_col2:
            Owner = st.selectbox('Owner', df['ownsership'].unique())
            Trans = st.selectbox('Transmission Type', df['transmission'].unique())

with col2:
    with st.container(border=True):
        st.subheader("⚙️ Technical Specifications")
        Mlg = st.slider('Mileage (kmpl)', 0, 40, 18)
        Eng = st.slider('Engine (CC)', 700, 2000, 1200)
        Maxi = st.slider('Maximum Power (bhp)', 700, 2000, 1000)
        Tor = st.slider('Torque (Nm)', 0, 2000, 250)

st.divider()

if st.button('Predict The Final Price OF Car', use_container_width=True, type="primary"):

    input_data = pd.DataFrame([[
        Seats,
        KmsDriven,
        CarManufacturedYear,
        Mlg,
        Eng,
        Maxi,
        Tor,
        1 if Fuel == 'Diesel' else 0,
        1 if Fuel == 'Petrol' else 0,
        1 if Owner == 'Second Owner' else 0,
        1 if Owner == 'Third Owner' else 0,
        1 if Trans == 'Manual' else 0
    ]], columns=[
        'seats',
        'kms_driven',
        'manufacturing_year',
        'mileage(kmpl)',
        'engine(cc)',
        'max_power(bhp)',
        'torque(Nm)',
        'fuel_type_Diesel',
        'fuel_type_Petrol',
        'ownsership_Second Owner',
        'ownsership_Third Owner',
        'transmission_Manual'
    ])

    input_data_scaled = scaler.transform(input_data)
    cpp_charges = model.predict(input_data_scaled)
    predicted_val = cpp_charges[0]

    st.success("Prediction Completed Successfully!")
    
    with st.container(border=True):
        res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
        with res_col2:
            st.metric(
                label="Estimated Market Value",
                value=f"₹ {predicted_val:.2f} Lakhs",
                delta=f"Raw Value: {predicted_val:.4f}"
            )