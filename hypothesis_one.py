import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import style
from hypothesis_two import clean_data

#Setting dataset variable with cleaned data
group_data = clean_data()
boro_initials_list = ["BX", "BK", "MN", "QN", "SI"]
boro_names = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']

def borough_filter_function(num):
    boro_initials = boro_initials_list[num]
    borough_filter = f'{boro_initials}_CASE_COUNT'
    borough_fatality_filter = f'{boro_initials}_FATALITY_RATE'
    data1 = group_data.groupby('subgroup')[borough_filter].sum()
    data2 = group_data.groupby('subgroup')[borough_fatality_filter].sum()
    return boro_initials, borough_filter, borough_fatality_filter, data1, data2

#Declaring chart variables
labels = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
x = np.arange(len(labels))
width = 0.25

y1 = group_data.iloc[:,2:12:2]
y2 = group_data.iloc[:, 12:]

def bar_1(data1,data2,boro_initials):

    data1 = data1
    data2 = data2

    plt.style.use('fivethirtyeight')
    fig, ax1= plt.subplots(figsize=(30,15))
    ax2 = ax1.twinx()

    ax1.bar(x-width/2, data1, width=width*2,label='Number of Cases', color='#0077B6')
    ax2.bar(x+width/2, data2,width=width*2,label='Fatality Rate',color= '#C5DCA0')

    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_xlabel('Age', size=25)
    ax1.set_ylabel('Number of cases', size=25)
    ax2.set_ylabel('Fatality Rate', size=25)
    ax1.set_title(f'Infection (Number of cases) and Fatality Rate(deaths/number of cases) Per Age Group in {boro_initials}', size=35)
    # plt.legend(loc='upper right', prop={"size":20})
    ax1.legend(loc='upper left', prop={"size":20})
    ax2.legend(loc='upper right',prop={"size":20})
    return fig

def app():
    st.title('First Hypothesis:')
    st.subheader('The infection (number of cases) and fatality rate(deaths/total cases) in the 75 + age group will be the highest because this is the oldest age group.')
    
    st.header('Fatality, Count and Deaths per age Group Dataframe')
    st.write(clean_data())

    st.header('Analysis:')

    st.write('The Borough filter option will isolate the corresponding column from the dataframe that matches that borough name. It will then display the number of cases per age group according to that specific borough.')
    st.write('The pattern mentioned above is seen throughout all the NYC boroughs, showing that the fatality is the highest amount the older age group.')

    option = st.selectbox('Select a Borough', (boro_names))

    st.subheader('Figure 1.1 Description')
    st.write('For this bar diagram we are showing the comparison between the Number of COVID-19 Cases and the Fatality Rate per Age Group. We have estimated the Fatality Rate by dividing the Death Cases to the Number of Total Case Count per each Borough and Age Group.')
    st.write("This diagram only partially proves our First Hypothesis where we have stated that the Fatality Rate increases in the older generation (75th age group).")
    st.write("For each neighborhood, we see that the fatality rate is the highest in the oldest age gorup, 75+. This trend is observed in all of the NYC boroughs.")
    st.write("However,we originally hypothesized that the number of cases would increase in the 75+ age group but is not what was observed. For instance, we see that the highest number of Covid-19 cases is seen in the 25-34 age group with over 40,000 cases. This is most likely because we didn't take the census into consideration and we assumed that the distribution between the different age groups would be the same.")
    st.write("In conclusion, this diagram only proves that the highest fatality rate is seen in the older age group, 75+. What this means is that although the 75+ age group might not have as much cases of covid,  WHEN they do get infected, they are 0.25% more likely to die of it.")

    if option == boro_names[0]:
        num = 0
        boro_initials, borough_filter, borough_fatality_filter, data1, data2 = borough_filter_function(num)
        st.write(bar_1(data1,data2,boro_initials))
    elif option == boro_names[1]:
        num = 1
        boro_initials, borough_filter, borough_fatality_filter, data1, data2 = borough_filter_function(num)
        st.write(bar_1(data1,data2,boro_initials))
    elif option == boro_names[2]:
        num = 2
        boro_initials, borough_filter, borough_fatality_filter, data1, data2 = borough_filter_function(num)
        st.write(bar_1(data1,data2,boro_initials))
    elif option == boro_names[3]:
        num = 3
        boro_initials, borough_filter, borough_fatality_filter, data1, data2 = borough_filter_function(num)
        st.write(bar_1(data1,data2,boro_initials))
    else:
        num = 4
        boro_initials, borough_filter, borough_fatality_filter, data1, data2 = borough_filter_function(num)
        st.write(bar_1(data1,data2,boro_initials))
