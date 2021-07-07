import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

plt.style.use('fivethirtyeight')
st.set_page_config(layout="wide")

age_filter = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']

def clean_data():
    by_boro = pd.read_csv("https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/group-data-by-boro.csv")
    by_boro.drop([12,13,14,15,16,17], inplace=True)
    by_boro = by_boro.fillna((by_boro[by_boro['group']=='Age'][:3].sum()))
    by_boro.drop([1,2,3],inplace=True)
    for col in by_boro.columns:
        if "RATE" in col or "HOSPITALIZED_COUNT" in col:
            by_boro = by_boro.drop(col, axis=1)
    by_boro.drop([0],inplace=True)
    by_boro["BK_FATALITY_RATE"] = by_boro["BK_DEATH_COUNT"]/by_boro["BK_CASE_COUNT"]
    by_boro["BX_FATALITY_RATE"] = by_boro["BX_DEATH_COUNT"]/by_boro["BX_CASE_COUNT"]
    by_boro["MN_FATALITY_RATE"] = by_boro["MN_DEATH_COUNT"]/by_boro["MN_CASE_COUNT"]
    by_boro["QN_FATALITY_RATE"] = by_boro["QN_DEATH_COUNT"]/by_boro["QN_CASE_COUNT"]
    by_boro["SI_FATALITY_RATE"] = by_boro["SI_DEATH_COUNT"]/by_boro["SI_CASE_COUNT"]
    by_boro.drop(columns = ['group'], axis=1, inplace=True)
    return by_boro
#All  rows with citywide- the 6 rows are needed for the cases/population chart
def pop_data():
    r = requests.get("https://data.cityofnewyork.us/resource/xywu-7bv9.json?")
    population = pd.DataFrame(json.loads(r.text))
    total = population[["borough", "_2020"]]
    return total
def five_boro():
    total = pop_data()
    total = total.drop([0]).reset_index(drop=True)
    return total
def population_density_fatality_filtered(filtration):
    filt = filtration
    total = five_boro()
    total["_2020"]=total._2020.astype(float)
    total["borough"]=total.borough.astype(str)
    total.loc[0, 'borough']  #there are white spaces at the front
    ##strip spaces
    total['borough'] = total['borough'].str.strip()
    #Land area in square miles per boro, taken from https://en.wikipedia.org/wiki/Boroughs_of_New_York_City
    d = {'Bronx': 42.10, 'Brooklyn':70.82, 'Manhattan':22.83, 'Queens':108.53, 'Staten Island':58.37}
    total['land'] = d.values()
    total["Density"] = total["_2020"]/total["land"]
    #Adding Fataity row per age group from clean data
    by_boro = clean_data()
    lst = by_boro[by_boro['subgroup']==filt][['BK_FATALITY_RATE', 'BX_FATALITY_RATE','MN_FATALITY_RATE','QN_FATALITY_RATE','SI_FATALITY_RATE']].to_dict('records')
    fatality = lst[0].values()
    total['Fatality'] = fatality
    return total
def population_density_fatality():
    total = five_boro()
    total["_2020"]=total._2020.astype(float)
    total["borough"]=total.borough.astype(str)
    total.loc[0, 'borough']  #there are white spaces at the front
    ##strip spaces
    total['borough'] = total['borough'].str.strip()
    #Land area in square miles per boro, taken from https://en.wikipedia.org/wiki/Boroughs_of_New_York_City
    d = {'Bronx': 42.10, 'Brooklyn':70.82, 'Manhattan':22.83, 'Queens':108.53, 'Staten Island':58.37}
    total['land'] = d.values()
    total["Density"] = total["_2020"]/total["land"]
    #Adding Fataity row per age group from clean data
    by_boro = clean_data()
    lst = by_boro[by_boro['subgroup']==age_filter][['BK_FATALITY_RATE', 'BX_FATALITY_RATE','MN_FATALITY_RATE','QN_FATALITY_RATE','SI_FATALITY_RATE']].to_dict('records')
    fatality = lst[0].values()
    total['Fatality'] = fatality
    return total
#Format column values before being passed to pie chart so # can be integer instead of % 
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        # val = val / 1000000
        return '{v:d}'.format(v=val)
    return my_format

total = population_density_fatality()
def pie_1():
    #transforming pie shares
    pie_shares = total.groupby('borough')['_2020'].sum()
    #Chart custumization
    fig, axes = plt.subplots(figsize=(10,7))
    axes.set(title="NYC Population per borough")
    labels = total['borough'].values
    wedges, texts, autotexts = axes.pie(pie_shares,explode=(0.00,0.09,0.00,0.09,0.00), shadow=False, startangle=0, autopct=autopct_format(pie_shares))
    axes.legend(wedges, labels, title = 'Boroughs', loc = 'center left', bbox_to_anchor = (1,0,0.5,1))
    axes.axis('equal')
    return fig
def pie_2():
    #transforming pie shares
    second_pie = total.groupby('borough')['Density'].sum()
    #Chart custumization
    fig, axes = plt.subplots(figsize=(10,7))
    axes.set(title="NYC Density ( Population / area in square miles) per borough")
    labels = total['borough'].values
    wedges, texts, autotexts = axes.pie(second_pie, explode=(0.00,0.09,0.09,0.00,0.00), shadow=False, startangle=0, autopct=autopct_format(second_pie))
    axes.legend(wedges, labels, title = 'Boroughs', loc = 'center left', bbox_to_anchor = (1,0,0.5,1))
    axes.axis('equal')
    return fig 
width = 0.25
labels = total['borough'].values
x = np.arange(len(labels))
def density_bar(filtration):
    filt = filtration
    data1 = total.groupby('borough')['Density'].sum()
    data2 = total.groupby('borough')['Fatality'].sum()
    plt.style.use('fivethirtyeight')
    fig, ax1= plt.subplots(figsize=(20,10))
    ax2 = ax1.twinx()
    ax1.bar(x-width/2, data1, width=width,label='Density', color='#C5DCA0')
    ax2.bar(x+width/2, data2,width=width,label='Fatality Rate',color= '#F1A208')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_xlabel('Borough')
    ax1.set_ylabel('Density')
    ax2.set_ylabel('Fatality Rate')
    ax1.set_title(f'Borough Density and Fatality Rate(deaths/number of cases) for {filt} Age Group')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    return fig

def exp_res1():
    data = [['Manhattan','Brooklyn','Bronx', 'Queens', 'Staten Island'], 
    ['Bronx','Brooklyn','Queens','Staten Island','Manhattan']]
    index = ['Expected', 'Result']
    df = pd.DataFrame(data, index=index)
    return df.transpose()

def exp_res2():
    data = [['Brooklyn','Queens','Manhattan','Bronx','Staten Island'], 
    ['Bronx','Brooklyn','Queens','Staten Island','Manhattan']]
    index = ['Expected', 'Result']
    df = pd.DataFrame(data, index=index)
    return df.transpose()


def population_bar(filtration):
    filt = filtration
    data1 = total.groupby('borough')['_2020'].sum()
    data2 = total.groupby('borough')['Fatality'].sum()
   
    fig, ax1= plt.subplots(figsize=(20,10))
    ax2 = ax1.twinx()
    ax1.bar(x-width/2, data1, width=width,label='Populations (millions)', color='#C5DCA0')
    ax2.bar(x+width/2, data2,width=width,label='Fatality Rate',color= '#D5573B')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_xlabel('Borough')
    ax1.set_ylabel('Populations (millions)')
    ax2.set_ylabel('Fatality Rate')
    ax1.set_title(f'Borough Population and Fatality Rate(deaths/number of cases) for {filt} Age Group')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    return fig

def app():
    st.title('Second Hypothesis:')
    st.subheader("Also,there is a direct correlation between the fatality rate and density of borough for the 75+ age group. A 75+ person living in a denser borough will have a higher chance of exposure and have a higher fatality than another 75+ person living in a less dense borough.")
    
    st.header('Fatality, Count and Deaths per age Group Dataframe')
    st.write(clean_data())

    st.subheader('Introduction')
    col1, col2 = st.beta_columns(2)
    st.write('Based on our second hypothesis, and as seen in figure 2.1, we are expecting Manhattan and Brooklyn to have the highest fatality rates because a 75+ person living in a denser borough will have a higher chance of exposure and have a higher fatality than another 75+ person living in a less dense borough.')


    with col1:
        st.subheader('Figure 2.1 Description')
        st.write('From this pie chart we can conclude that the density is highest in manhattan out of the five NYC boroughs with 71,760 residents per square mile and the second most dense borough is Brooklyn with 37,397 per square mile.')
        st.pyplot(pie_2())
    
    with col2:
        st.subheader('Figure 2.2 Description')
        st.write('In the second pie chart we are exploring the population of the five NYC boroughs. Here we can see that "Queens" and "Brooklyn" have the highest population with 2,648,452 residents and 2,330,295 residents respectively.')
        st.pyplot(pie_1())

    st.header('Analysis:')

    st.write('The Age filter option will isolate the corresponding row from the first dataframe that matches that age "subgroup"') 
    st.write('From the row selected: the columns containing the fatality rate of the 5 NYC boroughs will get added as a new column in the second dataframe.')
    
    option = st.selectbox('Select an Age', (age_filter))
    if option == age_filter[0]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[0]} group')
        st.write(population_density_fatality_filtered(age_filter[0]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1())
        st.write(density_bar(age_filter[0]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[0]))
    elif option == age_filter[1]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[1]} group')
        st.write(population_density_fatality_filtered(age_filter[1]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1())       
        st.write(density_bar(age_filter[1]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[1]))
    elif option == age_filter[2]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[2]} group')
        st.write(population_density_fatality_filtered(age_filter[2]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1())  
        st.write(density_bar(age_filter[2]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[2]))
    elif option == age_filter[3]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[3]} group')
        st.write(population_density_fatality_filtered(age_filter[3]))    
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1()) 
        st.write(density_bar(age_filter[3]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[3]))
    elif option == age_filter[4]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[4]} group')
        st.write(population_density_fatality_filtered(age_filter[4]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1()) 
        st.write(density_bar(age_filter[4]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[4]))
    elif option == age_filter[5]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[5]} group')
        st.write(population_density_fatality_filtered(age_filter[5]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1())     
        st.write(density_bar(age_filter[5]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[5]))
    elif option == age_filter[6]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[6]} group')
        st.write(population_density_fatality_filtered(age_filter[6]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1()) 
        st.write(density_bar(age_filter[6]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[6]))
    elif option == age_filter[7]:
        st.header(f'Population, Density and Fatality in borough for {age_filter[7]} group')
        st.write(population_density_fatality_filtered(age_filter[7]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1()) 
        st.write(density_bar(age_filter[7]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[7]))
    else:
        st.header(f'Population, Density and Fatality in borough for {age_filter[8]} group')
        st.write(population_density_fatality_filtered(age_filter[8]))
        st.subheader('Figure 2.3 Description')
        st.write(f"In our second hypothesis we stated that there is a direct correlation between the fataly rate and density of borough for the 75+ age group, however our graphs don't supprt this statement.")
        st.write('The chart below contradicts with our hypothesis. For the most dense boroughs, Manhattan and Brooklyn we were expecting the highest fatality rate, however our results show Bronx and Brooklyn with a higher fatality rate for the 75+ age group even though they are less dense.')
        st.write("This pattern could be a result of other socioeconomic factors, such as more family members having to live together because of low income household, that we aren't taking into consideration in this research.")
        st.write(exp_res1()) 
        st.write(density_bar(age_filter[8]))
        st.subheader('Figure 2.4 Description')
        st.write(f"For our second bar chart, we decided to see if the number of total population in a borough would have a better correlation with fatality rate for the 75+ age group than density, however we didn't find that to be the case. There was more similarity between number of total population and fatality rate than it was with density and fatality rate but it was still not similar enough to conclude any correlation.")
        st.write("In conclusion, there is no correlation between number of total popultion and fatality rate of the 75+ age group per borough.")
        st.write('For the most populated boroughs, Brooklyn and Queens we were expecting the highest fataly rate however our results puts Bronx and Brooklyn with a higher fatality rate.')
        st.write(exp_res2())
        st.write(population_bar(age_filter[8]))