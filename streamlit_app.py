import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import json
import os

DATA_FILE = "data.json"

def load_data_safe():
    """read data.json but with a try/except to avoid crash between write and reading"""
    print(f"DEBUG : Le fichier sera ici -> {os.path.abspath(DATA_FILE)}")
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            #if not exist
            default_data = {"battery": 100, "current_point": 0, "fire_detected": False, "command": "NONE" }
            with open(DATA_FILE, "w") as f:
                json.dump(default_data, f, indent=4)
            return default_data
    except Exception:
        #nothing done if writing
        pass
    return None

def save_command(cmd):
    try:
        data = load_data_safe()
        data["command"] = cmd
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error in the command: {e}")
        

#setting configuration of title
st.set_page_config(
    page_title='EARLY FIRE DETECTION',
    page_icon=':fire:', 
)

st.title(":fire: DRONE MONITORING")

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

 
#control buttons and info
with st.sidebar:
    st.header("COMMAND OF THE FLIGHT")
    if st.button(":flight_departure: DEPARTURE"):
        save_command("START")
        st.success("start order sent")
    
    if st.button(":stop_sign: ABORT AND RETURN TO HOME", type="primary"):
        save_command("ABORT")
        st.warning("mission aborted")
    
    if st.button(":video_game: TAKE CONTROL"):
        save_command("HOLD")
        st.warning("autonomous flight stoped")

    st.divider() 
    
    st.subheader("State of the drone:")
    
    
    
@st.fragment(run_every="2s")
def update_dynamic_content():
    data = load_data_safe()
    
    if data:
        cols = st.columns(3)
        cols[0].metric("Battery level: ", f"{data['battery']}%")
        cols[1].info(f"Status: {data['status']}")
        
        #visual if fire detected
        if data["alerts"]:
            cols[2].error(f":warning: FIRE DETECTED (points: {data['alerts']})")
        else:
            cols[2].success("No alert")

        #update map
        df = pd.DataFrame(fixed_points)
        #red: alert, else blue or green
        df['color_r'] = df['id'].apply(lambda x: 255 if x in data["alerts"] else 0)
        df['color_g'] = df['id'].apply(lambda x: 0 if x in data["alerts"] else 150)
        df['color_b'] = df['id'].apply(lambda x: 0 if x in data["alerts"] else 255)

        view_state = pdk.ViewState(latitude=48.9150, longitude=2.1000, zoom=12, pitch=45)
        
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position='[lon, lat]',
            get_color='[color_r, color_g, color_b, 200]',
            get_radius=250,
            pickable=True
        )

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer],
            tooltip={"text": "{name}"}
        ))


update_dynamic_content()
st.title("Forest of St-Germain")


#auto-refresh (Optionnal: force le rechargement toutes les 5s)
time.sleep(5)
st.rerun())
