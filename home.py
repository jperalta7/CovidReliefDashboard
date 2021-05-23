import streamlit as st

def app():
    st.title('Home page')

    st.write('Research Statement')

    st.write('We are tasked with looking at available information to identify those in the city with the biggest risk of covid. It is documented that elderly are the ones who are most at risk for the covid virus. By analyzing the trends of Covid-19 as it applied to how age affects mortality in NYC we will be able to reach a conclusion and prove/disprove our hypothesis.')

    st.write('Proposed hypothesis 1:')

    st.write('The infection rate and fatality rate in the 75 + age group will be the highest fatality(deaths/total cases) because they are in the older age group.')

    st.write('Proposed hypothesis 2:')

    st.write('Also, there is a direct correlation between the fatality rate and density of borough for the 75 + age group. A 75 + person living in a denser borough will have a higher chance of exposure and have a higher fatality than another 75 + person living in a less dense borough.')

