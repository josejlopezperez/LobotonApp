from os import path
import streamlit as st
from PIL import Image
import pandas as pd
import csv
import io
from datetime import datetime
from Src.CourtInfo import CourtInfo

class LobotonSheetWepApp():
    def __init__(self):
        st.set_page_config(page_title="Loboton Sheet", page_icon=":tennis:",
                           menu_items={'About': '''**Loboton Sheet**:
                            This is a web app to manage Loboton games. It allows you to upload a court file, view players, and record game results.
                            You can find more information about Loboton at [Loboton](https://www.loboton.com/).'''})
        st.title("Loboton Sheet")
        if 'courtInfo' not in st.session_state:
            uploaded_court = st.file_uploader("Upload a court file", type=["csv"])
            if uploaded_court is None: return
            csv_data = uploaded_court.read().decode('utf-8')
            spamReader  = csv.reader(io.StringIO(csv_data), delimiter=',', quotechar='"')
            st.session_state.courtInfo = CourtInfo(spamReader)
        if 'winnerTeam' not in st.session_state:
            st.session_state.winnerTeam = None
        st.header(st.session_state.courtInfo.name)
        
    def Window1(self):
        if 'courtInfo' not in st.session_state: return
        col1, col2 = st.columns(2)
        for idx, player in enumerate(st.session_state.courtInfo.players):
            if idx % 2 == 0:
                with col1:
                    with st.container():
                        col3, col4 = st.columns(2, vertical_alignment="center")
                        with col3:
                            st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=50)
                        with col4:
                            st.markdown(f'**{player.name}**')
            else:
                with col2:
                    with st.container():
                        col3, col4 = st.columns(2, vertical_alignment="center")
                        with col3:
                            st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=50)
                        with col4:
                            st.markdown(f'**{player.name}**')
        st.button("Start", type="primary", on_click=self.secondPage)

    def secondPage(self): 
        st.session_state.page = 1

    def Window2(self):
        nCombination = len(st.session_state.courtInfo.teams['Team 1'])
        gameIdx = (st.session_state.courtInfo.gameIdx % nCombination) if (st.session_state.courtInfo.gameIdx % nCombination) != 0 else nCombination
        prevGameIdx = gameIdx if (st.session_state.courtInfo.gameIdx == 1) else  gameIdx - 1 if gameIdx - 1 > 0 else nCombination

        st.subheader(f'Game #{st.session_state.courtInfo.gameIdx}')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Team 1')
            for player in st.session_state.courtInfo.teams['Team 1'][str(gameIdx)]:
                text = f'**{player.name}**' if player in st.session_state.courtInfo.teams['Team 1'][str(prevGameIdx)] else f':blue-background[**{player.name}**]'
                with st.container():
                    col3, col4 = st.columns(2, vertical_alignment="center")
                    with col3:
                        st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=50)
                    with col4:
                        st.markdown(text)
        with col2:
            st.markdown('Team 2')
            for player in st.session_state.courtInfo.teams['Team 2'][str(gameIdx)]:
                text = f'**{player.name}**' if player in st.session_state.courtInfo.teams['Team 2'][str(prevGameIdx)] else f':blue-background[**{player.name}**]'
                with st.container():
                    col3, col4 = st.columns(2, vertical_alignment="center")
                    with col3:
                        st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=50)
                    with col4:
                        st.markdown(text)

        if len(st.session_state.courtInfo.winnerTeam) >= st.session_state.courtInfo.gameIdx:
            st.session_state.winnerTeam = st.session_state.courtInfo.winnerTeam[st.session_state.courtInfo.gameIdx - 1]
        if st.session_state.winnerTeam == 'Team 1': 
            st.session_state.winnerTeam = st.radio(f"Who won the Game #{st.session_state.courtInfo.gameIdx}:",["Team 1", "Team 2"], horizontal=True, index=0)
        elif st.session_state.winnerTeam == 'Team 2': 
            st.session_state.winnerTeam = st.radio(f"Who won the Game #{st.session_state.courtInfo.gameIdx}:",["Team 1", "Team 2"], horizontal=True, index=1)
        else:
            st.session_state.winnerTeam = st.radio(f"Who won the Game #{st.session_state.courtInfo.gameIdx}:",["Team 1", "Team 2"], horizontal=True, index=None)
        
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.button("Prev Game", on_click=self.PrevGame, disabled= st.session_state.winnerTeam == None)
        with col2:
            st.button("Next Game", on_click=self.NextGame, disabled= st.session_state.winnerTeam == None)
        st.button("Finish Loboton", on_click=self.FinishLoboton, disabled= st.session_state.winnerTeam == None)

    def NextGame(self):
        try:
            st.session_state.courtInfo.winnerTeam[st.session_state.courtInfo.gameIdx-1] = st.session_state.winnerTeam
        except:
            st.session_state.courtInfo.winnerTeam.append(st.session_state.winnerTeam)
        st.session_state.courtInfo.gameIdx += 1
        st.session_state.winnerTeam = None

    def PrevGame(self):
        try:
            st.session_state.courtInfo.winnerTeam[st.session_state.courtInfo.gameIdx-1] = st.session_state.winnerTeam
        except:
            st.session_state.courtInfo.winnerTeam.append(st.session_state.winnerTeam)
        if st.session_state.courtInfo.gameIdx == 1: return
        st.session_state.courtInfo.gameIdx -= 1
        st.session_state.winnerTeam = None

    def FinishLoboton(self):
        try:
            st.session_state.courtInfo.winnerTeam[st.session_state.courtInfo.gameIdx-1] = st.session_state.winnerTeam
        except:
            st.session_state.courtInfo.winnerTeam.append(st.session_state.winnerTeam)
        st.session_state.courtInfo.Finish()
        self.thirdPage()

    def thirdPage(self): 
        st.session_state.page = 2

    def Window3(self):
        info = []
        st.subheader(f'Results: ')
        sortedPlayers = sorted(st.session_state.courtInfo.players, key=lambda x: x.wonGames, reverse=True)
        col1, col2 = st.columns(2)
        for idx, player in enumerate(sortedPlayers):
            if idx % 2 == 0:
                with col1:
                    with st.container():
                        col3, col4 = st.columns(2, vertical_alignment="center")
                        with col3:
                            st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=50)
                        with col4:
                            st.markdown(f'{player.name}: {player.wonGames} / {st.session_state.courtInfo.NGames}')
            else:
                with col2:
                    with st.container():
                        col3, col4 = st.columns(2, vertical_alignment="center")
                        with col3:
                            st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=50)
                        with col4:
                            st.markdown(f'{player.name}: {player.wonGames} / {st.session_state.courtInfo.NGames}')
            info.append({"Player": player.name, "Games won": f'{player.wonGames} / {st.session_state.courtInfo.NGames}'})
        df = pd.DataFrame(info)
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Results",
            data=csv,
            file_name=f'results_{st.session_state.courtInfo.name}_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.csv',
            mime='text/csv'
        )
        
if __name__ == '__main__':
    if 'page' not in st.session_state: st.session_state.page = 0
    lobotonSheet = LobotonSheetWepApp()
    if st.session_state.page == 0:
        lobotonSheet.Window1()
    elif st.session_state.page == 1:
        lobotonSheet.Window2()
    elif st.session_state.page == 2:
        lobotonSheet.Window3()
        
    
