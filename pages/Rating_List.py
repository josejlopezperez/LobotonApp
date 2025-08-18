import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1azTJNnMNAVYobFHj9c1baT1rGId4aeaUc5gwsxXy0po/edit?gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)
st.dataframe(data)