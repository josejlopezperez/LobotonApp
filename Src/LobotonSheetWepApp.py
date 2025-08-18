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
        column1, column2 = st.columns(2)
        for idx, player in enumerate(st.session_state.courtInfo.players):
            column = column1 if idx % 2 == 0 else column2
            container = column.container()
            column3, column4 = container.columns(2, vertical_alignment="center")
            column3.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=25)
            column4.markdown(f'**{player.name}**')
        st.button("Start", type="primary", on_click=self.secondPage)

    def secondPage(self): 
        st.session_state.page = 1

    def Window2(self):
        nCombination = st.session_state.courtInfo.nCombination
        game = st.session_state.courtInfo.games[st.session_state.courtInfo.gameIdx - 1]
        gameIdx = (st.session_state.courtInfo.gameIdx % nCombination) if (st.session_state.courtInfo.gameIdx % nCombination) != 0 else nCombination
        prevGameIdx = gameIdx if (st.session_state.courtInfo.gameIdx == 1) else  gameIdx - 1 if gameIdx - 1 > 0 else nCombination
        prevGame = st.session_state.courtInfo.games[prevGameIdx - 1]

        st.subheader(f'Game #{st.session_state.courtInfo.gameIdx}')
        column1, column2 = st.columns(2)
        for idx in range(2):
            column = column1 if idx == 0 else column2
            teamName = 'Team 1' if idx == 0 else 'Team 2'
            column.markdown(teamName)
            for player in game.teams[teamName]:
                if len(st.session_state.courtInfo.players) == 6:
                    text = f'**{player.name}**' if player in prevGame.teams[teamName] else f':blue-background[**{player.name}**]'
                elif len(st.session_state.courtInfo.players) == 7:
                    if player in game.subteams['A']:
                        text = f':red-background[**{player.name}**]'
                    elif player in game.subteams['B']:
                        text = f':green-background[**{player.name}**]'
                    else:
                        text = f'**{player.name}**'
                else:
                    if player in game.subteams['A']:
                        text = f':red-background[**{player.name}**]'
                    elif player in game.subteams['B']:
                        text = f':green-background[**{player.name}**]'
                    elif player in game.subteams['C']:
                        text = f':blue-background[**{player.name}**]'
                    else:
                        text = f':orange-background[**{player.name}**]'
                container = column.container()
                column3, column4 = container.columns(2, vertical_alignment="center")
                column3.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=25)
                column4.markdown(text)

        if st.session_state.winnerTeam == 'Team 1': 
            st.session_state.winnerTeam = st.radio(f"Who won the Game #{st.session_state.courtInfo.gameIdx}:",["Team 1", "Team 2"], horizontal=True, index=0)
        elif st.session_state.winnerTeam == 'Team 2': 
            st.session_state.winnerTeam = st.radio(f"Who won the Game #{st.session_state.courtInfo.gameIdx}:",["Team 1", "Team 2"], horizontal=True, index=1)
        else:
            st.session_state.winnerTeam = st.radio(f"Who won the Game #{st.session_state.courtInfo.gameIdx}:",["Team 1", "Team 2"], horizontal=True, index=None)

        column1, column2 = st.columns(2, vertical_alignment="center")
        column1.button("Prev Game", on_click=self.PrevGame, disabled= st.session_state.winnerTeam == None)
        column2.button("Next Game", on_click=self.NextGame, disabled= st.session_state.winnerTeam == None)
        st.button("Finish Loboton", on_click=self.FinishLoboton, disabled= st.session_state.winnerTeam == None)

    def NextGame(self):
        st.session_state.courtInfo.games[st.session_state.courtInfo.gameIdx - 1].winnerTeam = st.session_state.winnerTeam
        st.session_state.courtInfo.gameIdx += 1
        if len(st.session_state.courtInfo.winnerTeam) >= st.session_state.courtInfo.gameIdx:
            st.session_state.winnerTeam = st.session_state.courtInfo.winnerTeam[st.session_state.courtInfo.gameIdx - 1]
        else:
            st.session_state.winnerTeam = None
        if st.session_state.courtInfo.NGames < st.session_state.courtInfo.gameIdx:
            st.session_state.courtInfo.CreateNewGame()

    def PrevGame(self):
        st.session_state.courtInfo.games[st.session_state.courtInfo.gameIdx - 1].winnerTeam = st.session_state.winnerTeam
        st.session_state.courtInfo.gameIdx -= 1 if st.session_state.courtInfo.gameIdx > 1 else 0
        st.session_state.winnerTeam = st.session_state.courtInfo.games[st.session_state.courtInfo.gameIdx - 1].winnerTeam

    def FinishLoboton(self):
        st.session_state.courtInfo.games[st.session_state.courtInfo.gameIdx - 1].winnerTeam = st.session_state.winnerTeam
        st.session_state.courtInfo.Finish()
        st.session_state.page = 2 

    def Window3(self):
        info = []
        st.subheader(f'Results: ')
        sortedPlayers = sorted(st.session_state.courtInfo.players, key=lambda x: x.wonGames, reverse=True)
        column1, column2 = st.columns(2)
        for idx, player in enumerate(sortedPlayers):
            column = column1 if idx % 2 == 0 else column2
            container = column.container()
            column3, column4 = container.columns(2, vertical_alignment="center")
            column3.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), width=25)
            column4.markdown(f'{player.name}: {player.wonGames} / {st.session_state.courtInfo.NGames}')
            info.append({"Player": player.name, "Games won": f'{player.wonGames} / {st.session_state.courtInfo.NGames}'})
        df = pd.DataFrame(info)
        csv = df.to_csv(index=False)
        column1.download_button(
            label="Download Results",
            data=csv,
            file_name=f'results_{st.session_state.courtInfo.name}_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.csv',
            mime='text/csv'
        )
        column2.button("Send Results", on_click=self.SendEmail, disabled= True)
    
    def SendEmail(self):
        pass
