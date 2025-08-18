import streamlit as st
from os import path
import pandas as pd

with open(path.join(path.abspath('Resources'), 'court_6_players.csv'), newline='') as csvFile:
    df = pd.read_csv(csvFile, index_col=0)
    st.write("Example of a court file with 6 players:")
    st.data_editor(df)

with open(path.join(path.abspath('Resources'), 'court_7_players.csv'), newline='') as csvFile:
    df = pd.read_csv(csvFile, index_col=0)
    st.write("Example of a court file with 7 players:")
    st.data_editor(df)
    
with open(path.join(path.abspath('Resources'), 'court_8_players.csv'), newline='') as csvFile:
    df = pd.read_csv(csvFile, index_col=0)
    st.write("Example of a court file with 8 players:")
    st.data_editor(df)