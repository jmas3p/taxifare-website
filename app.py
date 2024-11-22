import streamlit as st
from datetime import datetime
import requests
import folium
from streamlit_folium import st_folium

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

st.markdown("### Map of Pickup and Dropoff Locations")

# Initialize Folium map
m = folium.Map(location=[(pickup_latitude + dropoff_latitude) / 2, (pickup_longitude + dropoff_longitude) / 2],
               zoom_start=12)

# Add pickup marker
folium.Marker(
    location=[pickup_latitude, pickup_longitude],
    popup="Pickup Location",
    icon=folium.Icon(color="blue", icon="cloud"),
).add_to(m)

# Add dropoff marker
folium.Marker(
    location=[dropoff_latitude, dropoff_longitude],
    popup="Dropoff Location",
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(m)

# Optionally add a line connecting the two points
folium.PolyLine(
    locations=[[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]],
    color="green",
    weight=2.5,
    opacity=1,
).add_to(m)

# Render the map in Streamlit
st_data = st_folium(m, width=700, height=500)
