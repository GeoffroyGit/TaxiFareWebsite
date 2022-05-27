import streamlit as st
import datetime
import requests as rq
import pandas as pd

url_api = 'https://api-3d2vvkkptq-ew.a.run.app/predict'

'''
# Welcome to New York City
'''

columns = st.columns(4)

user_date = columns[0].date_input("", datetime.date(2022, 9, 2))
user_time = columns[0].time_input("", datetime.time(12, 00))
user_pickup_lon = columns[1].number_input('pickup longitude', -73.950655)
user_pickup_lat = columns[1].number_input('pickup latitude', 40.783282)
user_dropoff_lon = columns[2].number_input('dropoff longitude', -73.984365)
user_dropoff_lat = columns[2].number_input('dropoff latitude', 40.769802)
user_passenger_count = columns[3].number_input('passengers', 1)

df = pd.DataFrame({
    "lat" : [user_pickup_lat, user_dropoff_lat],
    "lon" : [user_pickup_lon, user_dropoff_lon]
})

st.map(df)


if st.button('Get taxi fare'):
    params_for_api = {
        "pickup_datetime" : f"{user_date} {user_time}",
        "pickup_longitude" : user_pickup_lon,
        "pickup_latitude" : user_pickup_lat,
        "dropoff_longitude" : user_dropoff_lon,
        "dropoff_latitude" : user_dropoff_lat,
        "passenger_count" : user_passenger_count
    }
    response = rq.get(url_api, params=params_for_api)
    if response.status_code == 200:
        ":-)"
        fare = response.json().get("fare", 0)
        fare
    else:
        ":-("
