import os
import json
import datetime
import requests
import streamlit as st

from dotenv import load_dotenv
from utils import style_metric_cards


load_dotenv()
apiKey = os.getenv("API_KEY")
lat = os.getenv("LAT")
long = os.getenv("LONG")
city = os.getenv("CITY")

st.header(f"Current Weather : {city}")
st.divider()

def extract_current():
    getUrl = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={apiKey}'
    response = requests.request("GET", getUrl, params={"appid": apiKey})
    return(json.loads(response.content.decode('utf-8')))

current_json = extract_current()
icon_code = current_json["weather"][0]["icon"]
weather_main = current_json["weather"][0]["main"]
main = current_json["main"]
wind = current_json["wind"]
# st.markdown(f"""{weather_main} : ![{weather_main}](https://openweathermap.org/img/wn/{icon_code}@2x.png)""")
# st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Weather", weather_main)
col2.metric("Pressure", main["pressure"])
col3.metric("Humidity", main["humidity"])
st.divider()

st.subheader("Temperature")
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", main["temp"])
col2.metric("Max Temp", main["temp_max"])
col3.metric("Min Temp", main["temp_min"])
st.divider()

st.subheader("Wind")
col1, col2, col3 = st.columns(3)
col1.metric("Speed", wind["speed"])
col2.metric("Degree", wind["deg"])
if "gust"in wind:
    col3.metric("Gust", wind["gust"])
st.divider()

st.subheader("Temperature")
col1, col2, col3 = st.columns(3)
col1.metric("Sunrise", str(datetime.datetime.fromtimestamp(current_json["sys"]["sunrise"]).time()))
col2.metric("Sunset", str(datetime.datetime.fromtimestamp(current_json["sys"]["sunset"]).time()))
st.divider()

style_metric_cards()