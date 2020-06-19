class UserData:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.nextIndex = -1
        self.users = {}
        self.load()

    def load(self):
        self.file = open(self.filename, 'r')
        for line in self.file:
            i,user,passw = line.strip().split(';')
            self.users[user] = (i, passw)
        self.nextIndex = int(i)+1
        self.file.close()
    
    def validate(self, userInput, passwInput):
        if userInput in self.users.keys():
            return self.users[userInput][1] == passwInput
        else:
            return False
    
    def add_user(self, userInput, passwInput):
        if userInput in self.users.keys():
            return -1
        else:
            self.users[userInput] = (self.nextIndex, passwInput)
            self.save()
            self.load()
    
    def save(self):
        newFile = open(self.filename, 'w')
        for user in self.users.keys():
            newFile.write(str(self.users[user][0]) +';'+ user +';'+str(self.users[user][1])+'\n')
    
    def getUserID(self, userInput):
        return self.users[userInput][0]