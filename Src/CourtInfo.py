from Src.Player import Player

class CourtInfo():
    def __init__(self,*args):
        self.name = ''
        self.players = []
        self.gameIdx = 1
        self.games = []
        self.gamesTemplate = []
        self.nCombination = 0
        for rowIdx, playerInfo in enumerate([row for row in args[0]]):
            if rowIdx == 0: 
                self.name = playerInfo[0]
                for gameIdx in range(len(playerInfo[1::])):
                    self.gamesTemplate.append(Game(gameIdx + 1))
                self.nCombination = len(playerInfo[1::])
                continue
            self.players.append(Player(playerInfo[0]))
            for gameIdx, team in enumerate(playerInfo[1::]):
                if team in ['|','1','A','B']:
                    self.gamesTemplate[gameIdx].teams['Team 1'].append(self.players[-1])
                    if team in ['A','B']:
                        self.gamesTemplate[gameIdx].subteams[team].append(self.players[-1])
                else:
                    self.gamesTemplate[gameIdx].teams['Team 2'].append(self.players[-1])
                    if team in ['C','D']:
                        self.gamesTemplate[gameIdx].subteams[team].append(self.players[-1])
        self.CreateNewGame()
    
    @property
    def NGames(self):
        return len(self.games)
    
    def CreateNewGame(self):
        gameIdx = (self.gameIdx % self.nCombination) if (self.gameIdx % self.nCombination) != 0 else self.nCombination
        self.games.append(Game(self.gameIdx))
        self.games[-1].teams = self.gamesTemplate[gameIdx - 1].teams.copy()
        self.games[-1].subteams = self.gamesTemplate[gameIdx - 1].subteams.copy()
    
    def Finish(self):
        for game in self.games:
            for player in game.teams[game.winnerTeam]:
                player.wonGames += 1
                
class Game():
    def __init__(self,*args):
        self.teams = {'Team 1':[], 'Team 2':[]}
        self.subteams = {'A':[], 'B':[], 'C':[], 'D':[]}
        self.winnerTeam = ''
        self.gameIdx = args[0] if args else 1