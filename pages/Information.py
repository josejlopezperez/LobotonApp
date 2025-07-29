import streamlit as st
from os import path
import pandas as pd

with open(path.join(path.abspath('Resources'), 'court_6_players.csv'), newline='') as csvFile:
    df = pd.read_csv(csvFile, index_col=0)
    st.write("Example of a court file with 6 players:")
    st.dataframe(df,)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download court file",
        data=csv,
        file_name='court_6_players.csv',
        mime='text/csv'
    )

with open(path.join(path.abspath('Resources'), 'court_7_players.csv'), newline='') as csvFile:
    df = pd.read_csv(csvFile, index_col=0)
    st.write("Example of a court file with 7 players:")
    st.dataframe(df)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download court file",
        data=csv,
        file_name='court_7_players.csv',
        mime='text/csv'
    )
    
with open(path.join(path.abspath('Resources'), 'court_8_players.csv'), newline='') as csvFile:
    df = pd.read_csv(csvFile, index_col=0)
    st.write("Example of a court file with 8 players:")
    st.dataframe(df)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download court file",
        data=csv,
        file_name='court_8_players.csv',
        mime='text/csv'
    )