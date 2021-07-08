import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

import model as m
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('DATRASH') #title

# Create a page dropdown 
page = st.selectbox("Choose your page", ["Détection de déchets plastique", "Carte"])
if page == "Détection de déchets plastique":
    # Display details of page 1
    #hour_to_filter = st.slider('hour', 0, 23, 17)
    uploaded_file = st.file_uploader("Choose a file")
    #title = st.text_input('Nom du cours d eau', 'Marne')
    if st.button('Prédire'):
        #st.write('Why hello there')
        m.trashdetect(uploaded_file.name)
        st.pyplot()

    #t = st.time_input()
    #st.write('Alarm is set for', t)
elif page == "Carte":
    # Display details of page 2
    DATE_COLUMN = 'date/time'

    # SETTING PAGE CONFIG TO WIDE MODE
    #st.set_page_config(layout="wide")

    # LOADING DATA
    DATE_TIME = "date/time"
    DATA_URL = (
        
    )

    @st.cache(persist=True)
    def load_data(nrows):
        data = pd.read_csv("coordonnees_gps.csv")
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis="columns", inplace=True)
        #data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
        return data

    data = load_data(1000)



#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#filtered_data = data[data[DATE_COLUMN].dt.hour]

    print(data)
    print(data.columns)

    midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.write("**Déchets répertoriés en france**")
    st.map(data)


