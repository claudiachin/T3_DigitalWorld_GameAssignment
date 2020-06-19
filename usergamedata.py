class UserGameData:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.gamedata = {}
        self.load()

    def load(self):
        self.file = open(self.filename, 'r')
        for line in self.file:
            i,lvl1,lvl2,lvl3 = line.strip().split(';')
            self.gamedata[i] = [lvl1,lvl2,lvl3]
        self.file.close()
    
    def getStarsImg(self, i):
        starsImg = []
        for lvl in self.gamedata[i]:
            starsImg.append('other/stars'+str(lvl)+'.png')
        return starsImg

    def updateLvl(self, userID, lvlChosen, HP):
        if HP < 30:
            self.gamedata[userID][lvlChosen-1] = 1
        elif HP < 50:
            self.gamedata[userID][lvlChosen-1] = 2
        else:
            self.gamedata[userID][lvlChosen-1] = 3
        self.save()
        self.load()
    
    def createNewUserData(self, userID):
        self.gamedata[userID] = [0,0,0]
        self.save()
        self.load()

    def save(self):
        newFile = open(self.filename, 'w')
        for user in self.gamedata.keys():
            newFile.write(str(user) +';'+ str(self.gamedata[user][0]) +';'+ str(self.gamedata[user][1]) +';'+ str(self.gamedata[user][2])+'\n')