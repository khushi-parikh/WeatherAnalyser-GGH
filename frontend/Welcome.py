from weatherbit.api import Api
import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
apiKey = os.getenv("API_KEY")
newline = '\n'

st.header('DesiEnviroMetrics - Environmental Data Analysis')


gif, inputs = st.columns([3,2])
with gif:
    st_lottie("https://assets6.lottiefiles.com/private_files/lf30_oj6pxozf.json")

with inputs:
    zipcode = st.text_input('Enter pin code')
    if st.button('Search'):
        getUrl = f'https://api.openweathermap.org/geo/1.0/zip?zip={zipcode},IN&appid={apiKey}'
        response = requests.request("GET", getUrl, params={"appid": apiKey})  
        ans = json.loads(response.content.decode('utf-8'))
        if zipcode and "message" in ans:
            st.error("Please choose another pin code. This one is not present in our database.")
        else:
            city = ans["name"]
            st.success(f"Selected city is {city} in India.")
            st.info("You can now look at various analysis for your city!")
            lat = str(ans["lat"])
            long = str(ans["lon"])
            os.environ["LAT"] = lat
            os.environ["LONG"] = long