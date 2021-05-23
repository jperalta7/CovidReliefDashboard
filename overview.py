import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import folium_static
import folium

url = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/latest/last7days-by-modzcta.csv"
df = pd.read_csv(url)
icon_url = './img/covid-red.png'
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
        [lat,
            lon], popup=f"<p>Zipcode: {zipcode}{nl} Area: {area}{nl} Positive Cases: {people_positive}{nl}</p>",
        icon=folium.features.CustomIcon(icon_url, icon_size=(15, 15))
    ).add_to(m)




def data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-boro.csv")
    df.drop(columns=['CASE_RATE', 'HOSPITALIZED_RATE',
            'DEATH_RATE'], inplace=True, axis=1)
    return df[:-1]

def t_data():
    df1 = data().transpose()
    df1.columns = df1.iloc[0]
    df1.drop(df1.index[0], inplace=True)
    return df1

def bronx():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x = t_data()['Bronx']
    y = data().columns[1:]
    sns.barplot(x,y, color='#b74f6f')
    
    return fig

def brooklyn():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x = t_data()['Brooklyn']
    y = data().columns[1:]
    sns.barplot(x,y, color='#b74f6f')
    
    return fig

def manhattan():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x = t_data()['Manhattan']
    y = data().columns[1:]
    sns.barplot(x,y, color='#b74f6f')
    
    return fig

def queens():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x = t_data()['Queens']
    y = data().columns[1:]
    sns.barplot(x,y, color='#b74f6f')
    
    return fig

def staten_island():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    x = t_data()['StatenIsland']
    y = data().columns[1:]
    sns.barplot(x,y, color='#b74f6f')
    
    return fig

def app():

    col1, col2 = st.beta_columns(2)

    with col1:
        st.header('Our Findings')

        st.write(data())
        option = st.selectbox('Select a Borough', ('Bronx',
                            'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'))
        if option == 'Bronx':
            st.write(bronx())
        elif option == 'Brooklyn':
            st.write(brooklyn())
        elif option == 'Manhattan':
            st.write(manhattan())
        elif option == 'Queens':
            st.write(queens())
        else:
            st.write(staten_island())

    with col2:
        st.header('NYC Covid Map by Zipcode')

        folium_static(m)

        st.write('This is a map of the five borough that make up New York City. We see many covid looking icons scattered all across the map. Each one of these icons represent an individual zipcode in New York City. If you zoom in and click on a covid icon, you will see a pop up that inform sus whhich zipcode it is, the name of the neighborhood, the current cases and the positivity rate within the past 7 days.')



