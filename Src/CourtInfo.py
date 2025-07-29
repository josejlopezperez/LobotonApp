from Src.Player import Player

class CourtInfo():
    def __init__(self,*args):
        self.name = ''
        self.players = []
        self.gameIdx = 1
        self.winnerTeam = []
        courtInfo = [row for row in args[0]]
        self.teams = {'Team 1':{},'Team 2':{}}
        for rowIdx, playerInfo in enumerate(courtInfo):
            if rowIdx == 0: 
                self.name = playerInfo[0]
                continue
            self.players.append(Player(playerInfo[0]))
            for gameIdx, team in enumerate(playerInfo[1::]):
                if team in ['|','1','A','B']:
                    try:
                        self.teams['Team 1'][str(gameIdx + 1)].append(self.players[-1])
                    except:
                        self.teams['Team 1'][str(gameIdx + 1)] = [self.players[-1]]
                else:
                    try:
                        self.teams['Team 2'][str(gameIdx + 1)].append(self.players[-1])
                    except:
                        self.teams['Team 2'][str(gameIdx + 1)] = [self.players[-1]]
    
    @property
    def NGames(self):
        return len(self.winnerTeam)
    
    def Finish(self):
        nGames = len(self.teams['Team 1'])
        for gameNum, team in enumerate(self.winnerTeam):
            gameIdx = ((gameNum + 1) % nGames) if ((gameNum + 1) % nGames) != 0 else nGames
            for player in self.teams[team][str(gameIdx)]:
                player.wonGames += 1