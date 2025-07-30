import streamlit as st
from Src.LobotonSheetWepApp import LobotonSheetWepApp    
 
if __name__ == '__main__':
    if 'page' not in st.session_state: st.session_state.page = 0
    lobotonSheet = LobotonSheetWepApp()
    if st.session_state.page == 0:
        lobotonSheet.Window1()
    elif st.session_state.page == 1:
        lobotonSheet.Window2()
    elif st.session_state.page == 2:
        lobotonSheet.Window3()