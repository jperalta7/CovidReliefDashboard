import home
import about
import first_diagram
import second_diagram
import third_diagram
# import folium_map
import overview
import streamlit as st

PAGES = {
    "Home": home,
    "About": about,
    # "NYC Covid Map": folium_map,
    "Totals Overview": overview,
    "First Diagram": first_diagram,
    "Second Diagram": second_diagram,
    "Third Diagram": third_diagram,
}

# st.set_page_config(layout="wide")

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()