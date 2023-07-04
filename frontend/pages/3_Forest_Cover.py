import os
import json
import folium
import geojson
import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit_folium as st_folium

from area import area
from dotenv import load_dotenv
from utils import data_footer

load_dotenv()
rootFolder = os.getenv('ROOT')

DATA_URL = f"{rootFolder}data/forest_stripped.csv"

with open(f"{rootFolder}data/india_state.geojson") as f:
    geojson_states = json.load(f)

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    data = data.replace('-', 0)
    for col in data.columns[1:]:
        data[col] = data[col].str.replace(',', '').fillna(0).astype(float)
    return data

@st.cache_data
def geojson_area_df():
    geo_json = geojson.load(open(f"{rootFolder}data/india_state.geojson"))
    areas = {}
    for i in geo_json['features']:
        areas[i["properties"]["NAME_1"]] = area(i["geometry"])
    df = pd.DataFrame.from_records([areas]).transpose().reset_index()
    df.rename(columns={0:"Area", "index":"State/UT"}, inplace=True)
    return df

data = load_data()
total_df = data.loc[data['State/UT'] == 'Total']
data.drop(total_df.index, inplace=True)
years = data.columns[1:]

area_df = geojson_area_df()
area_df["Area"] = area_df["Area"]/1000000
area_data = data.copy()
area_data = pd.merge(area_data, area_df, on="State/UT", how='outer')

for i in years:
    area_data[i] = area_data[i]/area_data["Area"]

st.header("Forest Cover over the years : India")

map, plots = st.tabs(["Map", "Plots"])

with plots:
    st.subheader("Total forest cover variation with year")
    st.area_chart(data=total_df.set_index("State/UT").transpose())
    st.divider()

    st.subheader("Forest cover per unit area variation with state for a given year")
    year = st.selectbox("Select year", options=years)
    st.bar_chart(area_data, x="State/UT", y=year)
    st.divider()

    st.subheader("Forest cover per unit area variation with year for a given state")
    state = st.selectbox("Select state", options=area_data["State/UT"].to_list())
    temp_df = area_data.set_index("State/UT").copy().transpose().drop("Area")
    st.area_chart(temp_df, y=state)
    st.divider()

    data_footer(area_data)

with map:
    st.subheader("Which years forest cover per unit area would you like to see?")
    # # plot the slider that selects number of person died
    year = st.select_slider("Select the year you want to see", options=years)
    st.write("Selected year : ", year)

    year_ind = area_data.columns.get_loc(year)
    data1 = area_data.iloc[:,[0,year_ind]]

    gdf = gpd.read_file(f"{rootFolder}data/india_state.geojson")

    df_final = pd.merge(gdf, data1, right_on="State/UT", left_on='NAME_1', how='outer')

    m = folium.Map(location=[20.5937,78.9629], zoom_start=4, tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)
    choropleth = folium.Choropleth(
            geo_data = geojson_states,
            data = df_final,
            columns=['State/UT', year],
            key_on= 'feature.properties.NAME_1',
            highlight=True,
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
        ).geojson.add_to(m)

    # for s in choropleth.data['features']:
    #     s['properties'][year] = df_final.loc[s['properties']['NAME_1'], year]

    folium.GeoJsonTooltip(['NAME_1']).add_to(choropleth)

    st_folium.folium_static(m)