import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import HeatMap
import pandas as pd

url = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/latest/last7days-by-modzcta.csv"
df = pd.read_csv(url)
icon_url = 'covid-red.png'
astoria_ditmars = [40.7644, -73.9235]
popup = folium.Popup(min_width=5550)
lat = df.lat.values
lon = df.lon.values
zipcode = df.modzcta.values
area = df.modzcta_name.values
people_positive = df.people_positive.values
nl = '\n'
points = list(zip(lat, lon, zipcode, area, people_positive))
m = folium.Map(location=astoria_ditmars, zoom_start=11, tiles="openstreetmap")
for lat, lon, zipcode, area, people_positive in points:
    folium.Marker(
        [lat,lon], popup=f"<p>Zipcode: {zipcode}{nl} Area: {area}{nl} Positive Cases: {people_positive}{nl}</p>",
        icon=folium.features.CustomIcon(icon_url,icon_size=(10, 10))
    ).add_to(m)

def app():
    st.title('NYC Covid Map by Zipcode')

    folium_static(m)