import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import requests
import json
from matplotlib import style
from first_diagram import pop_data



#Filter Variables

ticks = ["Bronx", "Brooklyn", "Manhattan", "Queens", "StatenIsland","Citywide" ]

def by_boro():
	totals_boro = pd.read_csv("https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/by-boro.csv")
	return totals_boro

def data_pop():
	data = pop_data()
	data.loc[data['borough']=='NYC Total', 'borough']= 'Citywide'
	data['borough'] = data['borough'].str.strip()
	data.loc[data['borough'] == "Staten Island", 'borough'] = "StatenIsland"
	data["_2020"] = data["_2020"].astype(int)
	return data

def join():
	totals_boro = by_boro()
	data = data_pop()
	totals_boro = totals_boro.set_index('BOROUGH_GROUP').join(data.set_index('borough'))
	totals_boro.drop(columns = ["CASE_RATE","HOSPITALIZED_RATE", "DEATH_RATE"], axis=1, inplace=True)
	totals_boro = totals_boro.rename(columns={"_2020": "POPULATION"})

	return totals_boro

def graph():
	totals_boro = join()
	fig,ax=plt.subplots(figsize=(20,10))
	color = ("red", "purple")
	ax.barh(ticks, totals_boro["POPULATION"],label='Cases (millions)',color="#D5573B")
	ax.barh(ticks, totals_boro["CASE_COUNT"], label='Populations (millions)',left= totals_boro["POPULATION"], color="#F1A208")
	ax.set_title(f'Number of Cases vs Total Population per Borough',size=35)
	ax.set_xlabel('Cases/Populations (millions)')
	ax.set_ylabel('Borough')
	ax.legend(loc='center right')

	return fig

def app():
    st.title('Third Diagram')

    st.write(join())
    st.write('In this diagram we are representing the correleation between Total Population and\
    Number of Cases per borough. We see that in boroughs where the population is higher there are\
    more COVID-19 cases.')

    st.pyplot(graph())

