from os import path
import streamlit as st
from PIL import Image
import pandas as pd
import csv
from Src.CourtInfo import CourtInfo

if 'page' not in st.session_state: st.session_state.page = 0
def firstPage(): st.session_state.page = 0
def secondPage(): st.session_state.page = 1
def thirdPage(): st.session_state.page = 2

class LobotonSheetWepApp():
    def __init__(self):
        # st.set_page_config(layout="wide")
        st.title("Loboton Sheet")
        if 'courtInfo' not in st.session_state:
            with open(path.join(path.abspath('Resources'), 'court1.csv'), newline='') as csvFile:
                spamReader  = csv.reader(csvFile, delimiter=',', quotechar='|')
                st.session_state.courtInfo = CourtInfo(spamReader)
        if 'winnerTeam' not in st.session_state:
            st.session_state.winnerTeam = None
        st.header(st.session_state.courtInfo.name)
        
        
    def Window1(self):
        gameIdx = 1
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            for player in st.session_state.courtInfo.teams['Team 1'][str(gameIdx)]:
                st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), caption=player.name, width=50)
        with col2:
            for player in st.session_state.courtInfo.teams['Team 2'][str(gameIdx)]:
                st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), caption=player.name, width=50)
        st.button("Start", type="primary", on_click=secondPage)
        
    def Window2(self):
        nCombination = len(st.session_state.courtInfo.teams['Team 1'])
        gameIdx = (st.session_state.courtInfo.gameIdx % nCombination) if (st.session_state.courtInfo.gameIdx % nCombination) != 0 else nCombination
        prevGameIdx = gameIdx if (st.session_state.courtInfo.gameIdx == 1) else  gameIdx - 1 if gameIdx - 1 > 0 else nCombination

        st.subheader(f'Game #{st.session_state.courtInfo.gameIdx}')
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            st.markdown(f'Team 1')
            for player in st.session_state.courtInfo.teams['Team 1'][str(gameIdx)]:
                st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), caption=player.name, width=50)
        with col2:
            st.markdown(f'Team 2')
            for player in st.session_state.courtInfo.teams['Team 2'][str(gameIdx)]:
                st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), caption=player.name, width=50)
        
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
        thirdPage()

    def Window3(self):
        gameIdx = 1
        col1, col2 = st.columns(2, vertical_alignment="center")
        with col1:
            for player in st.session_state.courtInfo.teams['Team 1'][str(gameIdx)]:
                st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), caption=f'{player.name} : {player.wonGames}/{st.session_state.courtInfo.gameIdx}', width=50)
        with col2:
            for player in st.session_state.courtInfo.teams['Team 2'][str(gameIdx)]:
                st.image(Image.open(path.join(path.abspath('Resources'), 'person.jpg')), caption=f'{player.name} : {player.wonGames}/{st.session_state.courtInfo.gameIdx}', width=50)

    #     self.__window1 = CTK.CTkFrame(self)
    #     self.__window1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    #     self.__window1.grid_rowconfigure(1, weight=1)
    #     self.__window1.grid_columnconfigure(0, weight=1)  
        
    #     CTK.CTkLabel(self.__window1, text= f'Results of {self.__courtInfo.name}').grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    #     self.__teamPlayers = CTK.CTkFrame(self.__window1)
    #     self.__teamPlayers.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    #     self.__teamPlayers.grid_columnconfigure((1,2), weight=1)  
    #     self.__teamPlayers.grid_rowconfigure(tuple(range(len(self.__courtInfo.players))), weight=1) 
    #     for i,player in enumerate(self.__courtInfo.players):
    #         img = CTK.CTkImage(light_image=Image.open('./Resources/person.jpg'),dark_image=Image.open('./Resources/person.jpg'),size=(50, 50))
    #         CTK.CTkLabel(self.__teamPlayers, image=img, text='').grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
    #         CTK.CTkLabel(self.__teamPlayers, text=player.name, fg_color='gray').grid(row=i, column=1, sticky="nsew", padx=5, pady=5)
    #         CTK.CTkLabel(self.__teamPlayers, text=f'{player.wonGames}/{self.__courtInfo.gameIdx}', fg_color='gray').grid(row=i, column=2, sticky="nsew", padx=5, pady=5)
    #     send = CTK.CTkButton(self.__window1, text='Send', command=self.SendResults)
    #     send.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)   
    
    # def SendResults(self):
    #     self.__window1.destroy()
    #     with open('.\Resources\court3.csv', newline='') as csvFile:
    #         spamReader  = csv.reader(csvFile, delimiter=',', quotechar='|')
    #         self.__courtInfo = CourtInfo(spamReader)
    #     self.Window1()

        
if __name__ == '__main__':
    lobotonSheet = LobotonSheetWepApp()
    if st.session_state.page == 0:
        lobotonSheet.Window1()
    elif st.session_state.page == 1:
        lobotonSheet.Window2()
    elif st.session_state.page == 2:
        lobotonSheet.Window3()
        
    
