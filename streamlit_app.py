import streamlit as st
import pandas as pd
import math
from numpy.random import default_rng as rng
import pydeck as pdk
from pathlib import Path


#setting configuration of title
st.set_page_config(
    page_title='EARLY FIRE DETECTION',
    page_icon=':fire:', 
)


#visual of actual page 
'''
# :fire: DRONE FOR EARLY FIRE DETECTION

Project made in the frame of an Aerospace Track. 
With the global warming of the Earth, more and more fire occurs in the forest. This crucial events have many impacts on biodiversity, that is why we need to prevent it. 
Our project consists in a embedded drone which sends update when a start of fire is detected. 
'''

''
''

fixed_points = [
    {"id": 1, "name": "Étoile du Grand Veneur", "lat": 48.9150, "lon": 2.1000},
    {"id": 2, "name": "Proche Château", "lat": 48.9000, "lon": 2.1050},
    {"id": 3, "name": "Zone Nord", "lat": 48.9300, "lon": 2.0900}
]

#connexion to the api or flux (way of receiving the alerts)
warning_update = []


def update_map(ids):
    #ids: the list of the id where an alert has been detected : 1, 2 and/or 3, or empty if none
    df = pd.DataFrame(fixed_points)
    
    #for each point, puting it in red if it has been warned
    df['color_r'] = df['id'].apply(lambda x: 255 if x in ids else 0)
    df['color_g'] = df['id'].apply(lambda x: 0 if x in ids else 100)
    df['color_b'] = df['id'].apply(lambda x: 0 if x in ids else 255)

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11', # Style adapté à la forêt
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                df,
                get_position='[lon, lat]',
                get_color='[color_r, color_g, color_b, 200]',
                get_radius=150,
                pickable=True
            ),
        ],
        initial_view_state=pdk.ViewState(
            latitude=48.9150, 
            longitude=2.1000, 
            zoom=12,
            pitch=0)
    ))
    
    
st.title("Forest of St-Germain")
update_map(warning_update)
