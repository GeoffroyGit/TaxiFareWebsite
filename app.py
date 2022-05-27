import streamlit as st
import datetime
import requests as rq
import pandas as pd

# set page config
st.set_page_config(page_title="NYC cab fare", layout="wide")

# API URLs
url_api = 'https://api-3d2vvkkptq-ew.a.run.app/predict'
url_geoloc = "https://nominatim.openstreetmap.org"

#default location settings
default_lat = [40.7527, 40.7051]
default_lon = [-73.9772, -74.0106]
default_address = ["Grand Central station, NYC, NY, USA",
                   "Beaver street, NYC, NY, USA"]

#"# Welcome to New York City"

# split screen in two columns
columns = st.columns(2)

# force passenger count since it has negligeable influence on the price
user_passenger_count = 1

# ask user for pickup and dropoff addresses
user_addresses = ["", ""]
user_addresses[0] = columns[1].text_input("Pickup", default_address[0])
user_addresses[1] = columns[1].text_input("Dropoff", default_address[1])

# set location to default in case the API call fails
user_lon, user_lat = default_lon, default_lat
# change address to latitude and longitude
for i in range(2):
    # prepare geoloc API call
    params_geoloc = {'q': user_addresses[i], 'format': 'json'}
    # API call
    response = rq.get(url_geoloc, params=params_geoloc)
    if response.status_code == 200:
        if len(response.json()) > 0:
            response = response.json()[0]
            user_lon[i] = float(response.get("lon", default_lon[i]))
            user_lat[i] = float(response.get("lat", default_lat[i]))

# show the addresses on a map
df = pd.DataFrame({
    "lat" : user_lat,
    "lon" : user_lon
})
columns[0].map(df)

# ask user for the date and time
user_date = columns[1].date_input("", datetime.date(2022, 9, 2))
user_time = columns[1].time_input("", datetime.time(12, 00))

# get the taxi price
if columns[1].button('Get taxi fare'):
    params_for_api = {
        "pickup_datetime" : f"{user_date} {user_time}",
        "pickup_longitude" : user_lon[0],
        "pickup_latitude" : user_lat[0],
        "dropoff_longitude" : user_lon[1],
        "dropoff_latitude" : user_lat[1],
        "passenger_count" : user_passenger_count
    }
    response = rq.get(url_api, params=params_for_api)
    if response.status_code == 200:
        fare = response.json().get("fare", 0)
        columns[1].success(f"I'll drive you for {fare} $")
    else:
        columns[1].error("Oops, something went wrong")
