import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
    st.title('Our Findings')

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
