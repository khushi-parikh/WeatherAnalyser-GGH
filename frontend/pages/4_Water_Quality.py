import os
import streamlit as st
import pandas as pd

from dotenv import load_dotenv
from utils import data_footer


load_dotenv()
rootFolder = os.getenv('ROOT')

st.header("Water pollutants over the years : India")

def water_data_preprocessing(WATER_DATA_URL):
    water_data = pd.read_csv(WATER_DATA_URL, encoding='windows-1252', skiprows=[0], names=['state','district','block','panchayat','village','habitation','pollutant','year'])
    water_data = water_data.drop(["habitation"], axis=1)
    water_data['district'] = water_data.district.apply(lambda x: str(x).split('(')[0])
    water_data['block'] = water_data.block.apply(lambda x: str(x).split('(')[0])
    water_data['panchayat'] = water_data.panchayat.apply(lambda x: str(x).split('(')[0])
    water_data['village'] = water_data.village.apply(lambda x: str(x).split('(')[0])
    water_data['year'] = water_data.year.apply(lambda x: str(x).split('/')[-1])
    return water_data

WATER_DATA_URL = f"{rootFolder}data/IndiaAffectedWaterQualityAreas.csv"
water_data = water_data_preprocessing(WATER_DATA_URL)
# st.write(water_data)

def coord_data_preprocessing(COORD_DATA_URL):
    coord_data = pd.read_json(COORD_DATA_URL).transpose().reset_index()
    coord_data = coord_data.rename(columns={0:"lat", 1:"lon"})
    coord_data[['district', 'state', 'country']] = coord_data['index'].str.split(',', expand=True)
    coord_data = coord_data.drop(["index", "country"], axis=1)
    coord_data['district'] = coord_data['district'].str.upper()
    coord_data['state'] = coord_data['state'].str.upper()
    return coord_data

COORD_DATA_URL = f"{rootFolder}data/coordinates.json"
coord_data = coord_data_preprocessing(COORD_DATA_URL)

water_data_df = water_data.groupby(['pollutant','state', 'district','year']).size().unstack()
water_data_df.fillna('NA',inplace=True)

pollutant_list =  water_data['pollutant'].unique()
year_list = water_data['year'].unique()
pollutant = st.selectbox("Choose pollutant", pollutant_list)
year = st.selectbox("Choose year", year_list)

map_data = water_data.groupby(['pollutant']).get_group(pollutant).groupby(['year']).get_group(year)
map_data = pd.merge(map_data, coord_data, on=["district","state"])


@st.cache_data
def plot(data):
    st.subheader(f"Places where {pollutant} existed in {year} :")
    st.map(data)

plot(map_data)

data_footer(pd.merge(water_data, coord_data, on=["district","state"]))
