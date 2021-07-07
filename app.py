import home
import about
import hypothesis_one
import hypothesis_two
import borough_cases
import overview
import presentation
import streamlit as st

PAGES = {
    "Home": home,
    "Totals Overview": overview,
    "Borough Cases": borough_cases,
    "Hypothesis One": hypothesis_one,
    "Hypothesis Two": hypothesis_two,
    "Project Presentation": presentation,
    "About": about,
}

st.set_page_config(layout="wide")

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()