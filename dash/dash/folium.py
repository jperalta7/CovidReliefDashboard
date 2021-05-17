import pandas as pd
import folium

url = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/latest/last7days-by-modzcta.csv"

def folium_map(url):
    df = pd.read_csv(url)
# For coordinates captured using a GPS, or by any means, longitude is the X value and latitude is the Y value. These are for a geographic coordinate system and have units of degrees.

    astoria_ditmars = [40.7644, -73.9235]
    icon_url = '../static/covid-red.png'
    popup = folium.Popup(min_width=5550)

    x = df.lat.values
    y = df.lon.values
    z = df.modzcta.values
    area = df.modzcta_name.values
    pos = df.people_positive.values

    nl = '\n'

    points = list(zip(x,y,z,area,pos))

    m = folium.Map(location=astoria_ditmars, zoom_start=11, tiles="openstreetmap")

    for x,y,z,area,pos in points:
        folium.Marker(
            [x, y], popup=f"<p>Zipcode: {z}{nl} Area: {area}{nl} Positive Cases: {pos}{nl}</p>",
#         icon=folium.Icon(color="black", icon="info-sign", icon_size=(10, 10))
            icon=folium.features.CustomIcon(icon_url,icon_size=(10, 10))
        ).add_to(m)

    return m