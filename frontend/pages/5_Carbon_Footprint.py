import os
import numpy as np
import streamlit as st

from PIL import Image
from dotenv import load_dotenv


load_dotenv()
rootFolder = os.getenv('ROOT')
IMG_URL = f"{rootFolder}frontend/imgs/"

st.header("Calculate your carbon footprint!")

calc, info = st.tabs(["Form", "Information"])

with calc:
    with st.form("my_form"):
        ans1 = st.number_input(label="Monthly Electricity Bill", key="ans1")*105

        ans2 = st.number_input(label="Monthly Gas Bill", key="ans2")*105

        ans3 = st.number_input(label="Monthly Oil Bill", key="ans3")*113

        ans4 = st.number_input(label="Yearly Mileage", key="ans4")*0.79

        ans5 = st.number_input(label="Number of flights <= 4 hours per year", key="ans5")*1100

        ans6 = st.number_input(label="Number of flights > 4 hours per year", key="ans6")*4400

        news1 = st.radio(options=("Yes", "No"), label="Do you recycle newspaper?", horizontal=True, key="news1")
        if(news1=="No"):
            ans7 = 184
        else:
            ans7 = 0

        news2 = st.radio(options=("Yes", "No"), label="Do you recycle aluminium and tin?", horizontal=True, key="news2")
        if(news2=="No"):
            ans7 = 166
        else:
            ans7 = 0

        submitted = st.form_submit_button("Submit", type="primary")
        if submitted:
            ans_pounds = ans1 + ans2 + ans3 + ans4 + ans5 + ans6 + ans7
            ans_metric_tons = ans_pounds/2205
            
            if ans_pounds<6000:
                st.success(f"Excellent job! Your carbon footprint is {ans_pounds} pounds = {ans_metric_tons} tons.")

            elif ans_pounds<16000:
                st.info(f"Good job! Your carbon footprint is {ans_pounds} pounds = {ans_metric_tons} tons.")
            
            elif ans_pounds<22000:
                st.info(f"Average! Your carbon footprint is {ans_pounds} pounds = {ans_metric_tons} tons, about the average value.")

            else:
                st.error(f"Too much! Your carbon footprint is {ans_pounds} pounds = {ans_metric_tons} tons, much higher than normal.")

with info:
    with st.expander("What is carbon footprint?", expanded=True):
        col1, col2 = st.columns([3,2])
        with col1:
            st.markdown("""
                According to the wikipedia, the carbon footprint (or greenhouse gas footprint) serves as an **indicator to compare the total amount of greenhouse gases** emitted from an activity, person, service, company or country.
            
                The carbon footprint is commonly expressed as the **carbon dioxide equivalent (CO2e)** and is meant to sum up the total greenhouse gas emissions (not just carbon dioxide) caused by economic activities, events, organizations, services etc.
            """)
        with col2:
            path = IMG_URL+'carbon-footprint.png'
            img= Image.open(path)
            np_img = np.array(img)
            st.image(np_img)

    with st.expander("What is a good carbon footprint value?"):
        col1, col2 = st.columns([3,2])
        with col1:
            st.markdown("""
                A number below 6,000 (reflected in pounds per year) is excellent. 
                Good is anywhere from 6,000 to 15,999, while 16,000 to 22,000 is average.
                Over 22,000? Not so great. 
            """)
        with col2:
            path = IMG_URL+'footprint-levels.png'
            img= Image.open(path)
            np_img = np.array(img)
            st.image(np_img)

    with st.expander("How can we reduce the carbon footprint?"):
        st.markdown("""
            * Minimise carbon footprint at home by using energy-efficient appliances and reducing water use.
            * SAlways opt for carpooling or any other form of public transport.
            * Do not use single-use plastics, including disposable coffee cups, straws, cutlery, etc. Use reusable utensils instead.   
            * Switch off the lights and any electrical appliances when not in use.
            * Reduce, reuse and recycle as much as you can.
        """)
        path = IMG_URL+'reduce-carbon.png'
        img= Image.open(path)
        np_img = np.array(img)
        st.image(np_img)
            