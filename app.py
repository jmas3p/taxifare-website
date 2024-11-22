import streamlit as st
from datetime import datetime
import requests

st.title("TaxiFareModel Front")
st.markdown('''
This app allows you to predict taxi fares using a pre-trained model hosted on an API.
''')

st.markdown('''
## Select ride parameters
Fill in the details of your ride below:
''')

pickup_datetime = st.text_input("Date and Time (format: YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=10, value=1)

if st.button("Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    url = "https://taxifare.lewagon.ai/predict"
    response = requests.get(url, params=params)
    prediction = response.json().get("fare", "Error: 'fare' key not found in response")
    st.success(f"Estimated fare: ${prediction:.2f}")
