import customtkinter as CTK
from PIL import Image
import csv

class CourtInfo():
    def __init__(self,*args):
        self.name = ''
        self.members = {}
        self.gameIdx = 1
        self.winnerTeam = []
        courtInfo = [row for row in args[0]]
        self.teams = {'Team 1':{},'Team 2':{}}
        for rowIdx, row in enumerate(courtInfo):
            if rowIdx == 0: 
                self.name = row[0]
                continue
            self.members[row[0]] = 0
            for gameIdx, team in enumerate(row[1::]):
                if team == '1':
                    try:
                        self.teams['Team 1'][str(gameIdx + 1)].append(row[0])
                    except:
                        self.teams['Team 1'][str(gameIdx + 1)] = [row[0]]
                else:
                    try:
                        self.teams['Team 2'][str(gameIdx + 1)].append(row[0])
                    except:
                        self.teams['Team 2'][str(gameIdx + 1)] = [row[0]]

class LobotonSheetApp(CTK.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('LobotonSheet')
        self.geometry("%dx%d+0+0" % (int(720/2), int(1280/2)))
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.Exit)
        
        with open('.\Resources\court4.csv', newline='') as csvFile:
            spamReader  = csv.reader(csvFile, delimiter=',', quotechar='|')
            self.__courtInfo = CourtInfo(spamReader)
        
        self.Window1()
        
    def Exit(self):
        exit()
        
    def Window1(self):
        self.__window1 = CTK.CTkFrame(self)
        self.__window1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.__window1.grid_rowconfigure(1, weight=1)
        self.__window1.grid_columnconfigure(0, weight=1)  
        
        CTK.CTkLabel(self.__window1, text= self.__courtInfo.name).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        teamMembers = CTK.CTkFrame(self.__window1)
        teamMembers.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        teamMembers.grid_columnconfigure(1, weight=1)  
        teamMembers.grid_rowconfigure(tuple(range(len(self.__courtInfo.members))), weight=1) 
        for i,member in enumerate(self.__courtInfo.members.keys()):
            img = CTK.CTkImage(light_image=Image.open('./Resources/person.jpg'),dark_image=Image.open('./Resources/person.jpg'),size=(50, 50))
            CTK.CTkLabel(teamMembers, image=img, text='').grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            CTK.CTkLabel(teamMembers, text=member, fg_color='gray').grid(row=i, column=1, sticky="nsew", padx=5, pady=5)
        start = CTK.CTkButton(self.__window1, text='Start', command=self.GoWindows2)
        start.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
    def GoWindows2(self):
        self.__window1.destroy()
        self.Window2()
        
    def Window2(self):
        nCombination = len(self.__courtInfo.teams['Team 1'])
        nMembersTeam1 = len(self.__courtInfo.teams['Team 1']['1'])
        nMembersTeam2 = len(self.__courtInfo.teams['Team 2']['1'])
        gameIdx = (self.__courtInfo.gameIdx % nCombination) if (self.__courtInfo.gameIdx % nCombination) != 0 else nCombination
        prevGameIdx = gameIdx if (self.__courtInfo.gameIdx == 1) else  gameIdx - 1 if gameIdx - 1 > 0 else nCombination 
        
        self.__window2 = CTK.CTkFrame(self)
        self.__window2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.__window2.grid_rowconfigure(1, weight=1)
        self.__window2.grid_columnconfigure(0, weight=1)  
        
        CTK.CTkLabel(self.__window2, text= f'Game {self.__courtInfo.gameIdx}').grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        teamFrame = CTK.CTkFrame(self.__window2)
        teamFrame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        teamFrame.grid_columnconfigure((0,1), weight=1)
        teamFrame.grid_rowconfigure(1, weight=1)
        CTK.CTkLabel(teamFrame, text= f'Team 1').grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        
        team1Frame = CTK.CTkFrame(teamFrame)
        team1Frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        team1Frame.grid_columnconfigure((0,1), weight=1)
        team1Frame.grid_rowconfigure(tuple(range(nMembersTeam1)), weight=1)
        for i,teamMember in enumerate(self.__courtInfo.teams['Team 1'][str(gameIdx)]):
            if teamMember in  self.__courtInfo.teams['Team 1'][str(prevGameIdx)]: color = 'gray'
            else: color = 'blue'
            img = CTK.CTkImage(light_image=Image.open('./Resources/person.jpg'),dark_image=Image.open('./Resources/person.jpg'),size=(40, 40))
            CTK.CTkLabel(team1Frame, image=img, text='').grid(row=i, column=0, sticky="nsew", padx=5, pady=1)
            CTK.CTkLabel(team1Frame, text=teamMember, fg_color= color).grid(row=i, column=1, sticky="nsew", padx=5, pady=1)
        CTK.CTkLabel(teamFrame, text= f'Team 2').grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        
        team2Frame = CTK.CTkFrame(teamFrame)
        team2Frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        team2Frame.grid_columnconfigure((0,1), weight=1)
        team2Frame.grid_rowconfigure(tuple(range(nMembersTeam2)), weight=1)
        for i,teamMember in enumerate(self.__courtInfo.teams['Team 2'][str(gameIdx)]):
            if teamMember in  self.__courtInfo.teams['Team 2'][str(prevGameIdx)]:color = 'gray'
            else:color = 'blue'
            img = CTK.CTkImage(light_image=Image.open('./Resources/person.jpg'),dark_image=Image.open('./Resources/person.jpg'),size=(40, 40))
            CTK.CTkLabel(team2Frame, image=img, text='').grid(row=i, column=0, sticky="nsew", padx=5, pady=1)
            CTK.CTkLabel(team2Frame, text=teamMember, fg_color= color).grid(row=i, column=1, sticky="nsew", padx=5, pady=1)
            
        buttonFrame  = CTK.CTkFrame(self.__window2)
        buttonFrame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        buttonFrame.grid_columnconfigure((0,1), weight=1) 
        nextGameButton = CTK.CTkButton(buttonFrame, text='Next Game', command=self.NextGame)
        nextGameButton.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        prevGameButton = CTK.CTkButton(buttonFrame, text='Prev Game', command=self.PrevGame)
        prevGameButton.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        finishButton = CTK.CTkButton(buttonFrame, text='Finish Loboton', command=self.FinishLoboton)
        finishButton.grid(row=1, column=0, columnspan = 2, sticky="nsew", padx=5, pady=5)
        
        winnerTeam = CTK.StringVar()
        winnerFrame  = CTK.CTkFrame(self.__window2)
        winnerFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        winnerFrame.grid_columnconfigure((0,1), weight=1) 
        CTK.CTkLabel(winnerFrame, text= f'Winner Team:').grid(row=0, column=0, columnspan = 2, sticky="nsew", padx=1, pady=1)
        winnerTeam1 = CTK.CTkRadioButton(winnerFrame, text="Team 1", variable=winnerTeam, value='Team 1', command=lambda: self.EnableWin2Buttons(buttonFrame, winnerTeam))
        winnerTeam1.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        winnerTeam2 = CTK.CTkRadioButton(winnerFrame, text="Team 2", variable=winnerTeam, value='Team 2', command=lambda: self.EnableWin2Buttons(buttonFrame, winnerTeam))
        winnerTeam2.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        if len(self.__courtInfo.winnerTeam) >= self.__courtInfo.gameIdx:
            if self.__courtInfo.winnerTeam[self.__courtInfo.gameIdx - 1] == 'Team 1': winnerTeam1.select()
            elif self.__courtInfo.winnerTeam[self.__courtInfo.gameIdx - 1] == 'Team 2': winnerTeam2.select()
        else:
            for child in buttonFrame.winfo_children():
                child.configure(state='disabled')
        
    def NextGame(self):
        self.__courtInfo.gameIdx += 1
        self.__window2.destroy()
        self.Window2()
    
    def PrevGame(self):
        if self.__courtInfo.gameIdx == 1: return
        self.__courtInfo.gameIdx -= 1
        self.__window2.destroy()
        self.Window2()
    
    def FinishLoboton(self):
        nCombination = len(self.__courtInfo.teams['Team 1'])
        for gameNum, team in enumerate(self.__courtInfo.winnerTeam):
            gameIdx = ((gameNum + 1) % nCombination) if ((gameNum + 1) % nCombination) != 0 else nCombination
            for member in self.__courtInfo.teams[team][str(gameIdx)]:
                self.__courtInfo.members[member] += 1
        self.__window2.destroy()
        self.Window3()
        
    def EnableWin2Buttons(self, buttonFrame, winnerTeam):
        try:
            self.__courtInfo.winnerTeam[self.__courtInfo.gameIdx-1] = winnerTeam.get()
        except:
            self.__courtInfo.winnerTeam.append(winnerTeam.get())
        for child in buttonFrame.winfo_children():
                child.configure(state='normal')
     
    def Window3(self):
        self.__window1 = CTK.CTkFrame(self)
        self.__window1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.__window1.grid_rowconfigure(1, weight=1)
        self.__window1.grid_columnconfigure(0, weight=1)  
        
        CTK.CTkLabel(self.__window1, text= f'Results of {self.__courtInfo.name}').grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.__teamMembers = CTK.CTkFrame(self.__window1)
        self.__teamMembers.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.__teamMembers.grid_columnconfigure((1,2), weight=1)  
        self.__teamMembers.grid_rowconfigure(tuple(range(len(self.__courtInfo.members))), weight=1) 
        for i,member in enumerate(self.__courtInfo.members.items()):
            img = CTK.CTkImage(light_image=Image.open('./Resources/person.jpg'),dark_image=Image.open('./Resources/person.jpg'),size=(50, 50))
            CTK.CTkLabel(self.__teamMembers, image=img, text='').grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
            CTK.CTkLabel(self.__teamMembers, text=member[0], fg_color='gray').grid(row=i, column=1, sticky="nsew", padx=5, pady=5)
            CTK.CTkLabel(self.__teamMembers, text=f'{member[1]}/{self.__courtInfo.gameIdx}', fg_color='gray').grid(row=i, column=2, sticky="nsew", padx=5, pady=5)
        send = CTK.CTkButton(self.__window1, text='Send', command=self.SendResults)
        send.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)   
    
    def SendResults(self):
        pass

        
if __name__ == '__main__':
    lobotonSheetApp = LobotonSheetApp()
    lobotonSheetApp.mainloop()
    
