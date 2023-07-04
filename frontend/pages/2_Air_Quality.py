import os
import json
import datetime
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from utils import data_footer

load_dotenv()
apiKey = os.getenv("API_KEY")
lat = os.getenv("LAT")
long = os.getenv("LONG")
city = os.getenv("CITY")


@st.cache_data
def extract_current():
    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&APPID={apiKey}'
    response = requests.request("GET", getUrl, params={"appid": apiKey})    
    return(json.loads(response.content.decode('utf-8')))

@st.cache_data
def extract_forecast():
    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={long}&APPID={apiKey}'
    response = requests.request("GET", getUrl, params={"appid": apiKey})  
    return(json.loads(response.content.decode('utf-8')))

def extract_history():
    start = datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata')) - datetime.timedelta(days=7)
    start_timestamp = int(round(datetime.datetime.timestamp(start)))

    end = datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata'))
    end_timestamp = int(round(datetime.datetime.timestamp(end)))

    getUrl = f'https://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={long}&start={start_timestamp}&end={end_timestamp}&APPID={apiKey}'
    response = requests.request("GET", getUrl, params={"appid": apiKey})  
    return(json.loads(response.content.decode('utf-8')))

@st.cache_data
def air_forecast(response_forecast):
    df = pd.DataFrame()
    aqi_values = [aqi["main"]["aqi"] for aqi in response_forecast["list"]]

    component_values = []
    component_names = [name for name in response_forecast["list"][0]["components"]]
    dates = [datetime.datetime.fromtimestamp(comp["dt"]).date() for comp in response_forecast["list"]]
    times = [datetime.datetime.fromtimestamp(comp["dt"]).time() for comp in response_forecast["list"]]
    for component in component_names:
        daily_values = []
        for day in response_forecast["list"]:
            daily_values.append(day["components"][component])
        component_values.append(daily_values)
    
    df["Date"] = dates
    df["Time"] = times
    df['AQI'] = aqi_values
    for i in range(len(component_names)):
        df[component_names[i]] = component_values[i]
    
    return df
    

response_current = extract_current()
response_forecast = extract_forecast()
air_forecast_df = air_forecast(response_forecast)
response_history = extract_history()
# st.write(response_current)
air_history_df = air_forecast(response_history)


st.header(f"Current Air Quality Info : {city}")
st.divider()

current_weather, temp, current_comp =  st.columns([5,2,3])
with current_weather:
    aqi = response_current["list"][0]["main"]["aqi"]


    with st.expander(f'Todays Statistics', expanded=True):
        st.markdown(f'''
        ##### AQI Level : {aqi}
        ''', unsafe_allow_html=True)

    label = ["Very Low", "Low", "Moderate", "Good", "Very Good"]
    val = [1,1,1,1,1]

    st.write("The higher the AQI, the more air pollution.")

    label.append("")
    val.append(sum(val))
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'white']

    # plot
    fig = plt.figure(figsize=(4,6), dpi=100)
    ax = fig.add_subplot(1,1,1)
    ax.pie(val, labels=label, colors=colors)
    ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))

    L = np.array([0, 0.8])
    center = [0, 0]
    phi = np.deg2rad(180-(180*aqi/5-180/10))
    x = center[0] + np.cos(phi) * L
    y = center[1] + np.sin(phi) * L
    ax.plot(x, y, 'k', linewidth=3)

    st.pyplot(fig)


with current_comp:
    component_names = response_current["list"][0]["components"]
    
    for i in component_names:
        st.markdown(
            f"""
            - {i} :  {component_names[i]}
            """
        )

forecast, history = st.tabs(["Forecast", "History"])

with forecast:
    st.header("Forecast of next 4 days")

    with st.container():
        st.subheader("Average AQI")

        aqi_values = air_forecast_df["AQI"]
        aqi_max = max(aqi_values)
        aqi_avg = sum(aqi_values)/len(aqi_values)

        temp_df = air_forecast_df.filter(['AQI','Date'], axis=1)
        aqi_daily_values = temp_df.groupby("Date", as_index=False).mean()

        col1, col2 = st.columns([1,3])
        with col1:
            st.write(aqi_daily_values.groupby("Date").mean())
        with col2:
            st.line_chart(aqi_daily_values, x="Date", y="AQI")

    with st.container():
        st.subheader("Values of each component")
        air_forecast_df_copy = air_forecast_df.copy()
        air_forecast_df_copy["DateTime"] = air_forecast_df["Date"].astype(str) + " " + air_forecast_df["Time"].astype(str)
        air_forecast_df_copy = air_forecast_df_copy.drop(["Date","Time"], axis=1)
        st.bar_chart(air_forecast_df_copy, x="DateTime")

    with st.container():
        data_footer(air_forecast_df)


with history:
    st.header("History of past 7 days")

    with st.container():
        st.subheader("Average AQI")

        aqi_values = air_history_df["AQI"]
        aqi_max = max(aqi_values)
        aqi_avg = sum(aqi_values)/len(aqi_values)

        temp_df = air_history_df.filter(['AQI','Date'], axis=1)
        aqi_daily_values = temp_df.groupby("Date", as_index=False).mean()

        col1, col2 = st.columns([1,3])
        with col1:
            st.write(aqi_daily_values.groupby("Date").mean())
        with col2:
            st.line_chart(aqi_daily_values, x="Date", y="AQI")

    with st.container():
        st.subheader("Values of each component")
        air_history_df_copy = air_history_df.copy()
        air_history_df_copy["DateTime"] = air_history_df["Date"].astype(str) + " " + air_history_df["Time"].astype(str)
        air_history_df_copy = air_history_df_copy.drop(["Date","Time"], axis=1)
        st.bar_chart(air_history_df_copy, x="DateTime")

    with st.container():
        data_footer(air_history_df)

