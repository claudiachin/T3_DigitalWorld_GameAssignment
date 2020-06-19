import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, WipeTransition
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.animation import Animation, AnimationTransition
from kivy.uix.image import Image
from kivy.clock import Clock
from userdata import UserData
from usergamedata import UserGameData
from random import randint
from time import sleep

# made for iPhone 7 Plus size
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '550')
Config.set('graphics', 'height', '306')

kv = Builder.load_file('game.kv')

#databases
db = UserData('userdata.txt')
gdb = UserGameData('usergamedata.txt')

#global variables
userID = ''
avatar = 0
pet = 0
lvlChosen = 1
currentLvlData = [None,None,None,None,100] #x_coord, y_coord, mazeData, knightsLeft, heroHP

class LoginPage(Screen):
    user = ObjectProperty(None)
    passw = ObjectProperty(None)
    
    def LoginBtn(self):
        if self.user.text == '' or self.passw.text == '':
            pass
        else:
            if db.validate(self.user.text, self.passw.text):
                screen_manager.current = 'main'
                global userID
                userID = db.getUserID(self.user.text)
            else:
                screen_manager.current = 'login'
        self.user.text = ''
        self.passw.text = ''

class SignUpPage(Screen):
    user = ObjectProperty(None)
    passw = ObjectProperty(None)

    def SignUpBtn(self):
        if self.user.text == '' or self.passw.text == '':
            pass
        else:
            if db.add_user(self.user.text, self.passw.text) != -1:
                screen_manager.current = 'main'
                global userID
                userID = db.getUserID(self.user.text)
                gdb.createNewUserData(userID)
            else:
                show_SignUpErrorPopUp()
        self.user.text = ''
        self.passw.text = ''

class SignUpErrorPopUp(FloatLayout):
    pass

def show_SignUpErrorPopUp():
    show = SignUpErrorPopUp()
    popupWin = Popup(title='Error', content=show, size_hint=(None,None), size=(400,90))
    popupWin.open()

class MainPage(Screen):
    def getIndexAvatar(self, index):
        global avatar
        avatar = index

    def getIndexPet(self, index):
        global pet
        pet = index

    def UserGuideBtn(self):
        show_UserGuidePopUp()
    
    def PlayBtn(self):
        show_PlayPopUp()

class UserGuidePopUp(FloatLayout):
    f = open('userguide.txt', 'r')
    userGuide = StringProperty(f.read())

def show_UserGuidePopUp():
    show = UserGuidePopUp()
    popupWin = Popup(title='User Guide', content=show, size_hint=(None,None), size=(400,250))
    popupWin.open()

class PlayPopUp(FloatLayout):
    #clicking on the play button brings you to a carousel, where you choose which level to play
    buttonObj = ObjectProperty(None)

    def getLevel(self, ind):
        global lvlChosen
        lvlChosen = ind+1

    def getStarsImg(self):
        return gdb.getStarsImg(userID)
    
    def getButtonObj(self):
        return self.buttonObj

def show_PlayPopUp():
    show = PlayPopUp()
    popupWin = Popup(title='Choose Level', content=show, size_hint=(None,None), size=(400,250))
    
    show.getButtonObj().bind(on_press=popupWin.dismiss)
    def startGame(self):
        App.get_running_app().root.transition.direction = 'left'
        App.get_running_app().root.current = 'maze'
    show.getButtonObj().bind(on_release=startGame)
    
    popupWin.open()

    global lvlChosen
    lvlChosen = 1

class MazePage(Screen):
    #mazeBase initialises a 10x6 matrix, with vals 0
    mazeBase = [[0 for i in range(10)] for i in range(6)]
    #vals of squares that cannot be stepped on will be 1
    #vals of squares w knights will be 2
    #based on mazeBase, a canvas of 30x30 squares will be created
    #0 = white square, 1 = black square, 2 = purple
    global currentLvlData
    x_coord, y_coord, mazeData, knightsLeft, heroHP = currentLvlData

    def setUp(self):
        global currentLvlData
        if currentLvlData == [None,None,None,None,100]:
            global lvlChosen
            if lvlChosen == 1: #lvl1: straight line
                for row in [0,1,3,4,5]:
                    self.mazeBase[row] = [1 for i in range(10)]
                self.mazeBase[2] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
                self.x_coord = 0
                self.y_coord = 2
                self.knightsLeft = 1

            elif lvlChosen == 2: #lvl2: up-down
                self.mazeBase = [[0, 1, 0, 0, 0, 1, 0, 0, 0, 1],\
                                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],\
                                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],\
                                [0, 1, 0, 1, 0, 1, 2, 1, 0, 1],\
                                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],\
                                [0, 0, 2, 1, 0, 0, 0, 1, 0, 2]]
                self.x_coord = 0
                self.y_coord = 0
                self.knightsLeft = 3
            
            elif lvlChosen == 3: #lvl3: spiral
                self.mazeBase = [[1, 1, 1, 1, 1, 0, 0, 0, 1, 1],\
                                [2, 0, 0, 0, 1, 0, 1, 0, 1, 1],\
                                [0, 1, 1, 0, 0, 0, 1, 0, 0, 1],\
                                [0, 0, 1, 0, 1, 1, 1, 1, 0, 1],\
                                [1, 0, 1, 0, 1, 1, 2, 1, 0, 1],\
                                [0, 0, 1, 0, 0, 0, 0, 1, 0, 2]]
                self.x_coord = 0
                self.y_coord = 5
                self.knightsLeft = 3
            self.heroHP = 100
        else:
            self.x_coord, self.y_coord, self.mazeBase, self.knightsLeft, self.heroHP = currentLvlData
    
    p = ''
    def createCanvas(self):
        with self.canvas:
            Rectangle(size=(350,210), pos=(self.center_x-5*35,self.center_y-3*35+20), source='other/background_maze.png')
            for j in range(6):
                for i in range(10):
                    row_pos = self.center_x+((i-5)*35)
                    col_pos = self.center_y-((j-3)*35+15)
                    if self.mazeBase[j][i] == 0:
                        Rectangle(size=(35, 35), pos=(row_pos,col_pos), source='other/path.png')
                    elif self.mazeBase[j][i] == 1:
                        Rectangle(size=(35, 35), pos=(row_pos,col_pos), source ='other/tree.png')
                    elif self.mazeBase[j][i] == 2:
                        Rectangle(size=(35, 35), pos=(row_pos,col_pos), source ='other/path_knight.png')
            self.p = Image(source='other/avatar_maze_right.png', size=(30,30), pos=(self.center_x+((self.x_coord-5)*35), self.center_y-(self.y_coord-3)*35+15-25))

    def reset(self):
        global currentLvlData
        currentLvlData = [None,None,None,None,100]

    def moveBtn(self, move):
        if move == 'u' and self.checkNext(self.y_coord-1, self.x_coord):
            self.y_coord -= 1
            self.p.y += 35
            self.p.source = 'other/avatar_maze_back.png'
        elif move == 'd' and self.checkNext(self.y_coord+1, self.x_coord):
            self.y_coord += 1
            self.p.y -= 35
            self.p.source = 'other/avatar_maze_front.png'   
        elif move == 'r' and self.checkNext(self.y_coord, self.x_coord+1):
            self.x_coord += 1
            self.p.x += 35
            self.p.source = 'other/avatar_maze_right.png'
        elif move == 'l' and self.checkNext(self.y_coord, self.x_coord-1):
            self.x_coord -= 1
            self.p.x -= 35
            self.p.source = 'other/avatar_maze_left.png'
    
    def checkNext(self, newY, newX):
        if newY < 0 or newY > 5:
            return False
        elif newX < 0 or newX > 9:
            return False
        elif self.mazeBase[newY][newX] == 1:
            return False
        else:
            return True
    
    def checkFight(self):
        if self.mazeBase[self.y_coord][self.x_coord] == 2:
            self.mazeBase[self.y_coord][self.x_coord] = 0
            global currentLvlData
            currentLvlData = [self.x_coord,self.y_coord,self.mazeBase,self.knightsLeft-1,self.heroHP]

            App.get_running_app().root.transition.direction = 'up'
            App.get_running_app().root.current = 'fight'

class FightingPage(Screen):
    heroHP = 100
    knightHP = 100
    maxUse = [None,3,1,1]
    use = [0,0,0,0]

    def setUp(self):
        global currentLvlData
        self.heroHP = currentLvlData[4]
        self.knightHP = 100
        self.use = [0,0,0,0]
        self.updateHPLabels()
        self.updateHeroHPBar()
        self.updateKnightHPBar()

    def attackBtn(self, attack):
        if attack == 1: #can use infinite amt of times
            self.knightHP -= randint(10,25)
        elif attack == 2 and self.checkBtn(2):
            self.knightHP -= randint(10,30)
            self.use[1] += 1
        elif attack == 3 and self.checkBtn(3):
            self.knightHP -= randint(10,40)
            self.use[2] += 1
        elif attack == 4 and self.checkBtn(4):
            self.knightHP -= randint(10,35)
            self.use[3] += 1
    
    def checkBtn(self, btn):
        return self.use[btn-1] != self.maxUse[btn-1]

    attackBtn1 = ObjectProperty(None)
    attackBtn2 = ObjectProperty(None)
    attackBtn3 = ObjectProperty(None)
    attackBtn4 = ObjectProperty(None)
    def enableBtns(self):
        self.attackBtn1.disabled = False if self.checkBtn(1) else True
        self.attackBtn2.disabled = False if self.checkBtn(2) else True
        self.attackBtn3.disabled = False if self.checkBtn(3) else True
        self.attackBtn4.disabled = False if self.checkBtn(4) else True
    
    def disableBtns(self):
        self.attackBtn1.disabled = True
        self.attackBtn2.disabled = True
        self.attackBtn3.disabled = True
        self.attackBtn4.disabled = True

    def knightAttack(self):
        self.heroHP -= randint(5,10)
        self.updateHPLabels()
        self.updateHeroHPBar()
        self.attackAnimation('hero')
        self.checkLose()

    avatarAndPet = ObjectProperty(None)
    knightImg = ObjectProperty(None)
    def attackAnimation(self, attacked):
        if attacked == 'knight':
            xpos = self.knightImg.x
            widget = self.knightImg
            mov = 1
        else:
            xpos = self.avatarAndPet.x
            widget = self.avatarAndPet
            mov = -1
        animSeq = Animation(x=xpos+mov*20, duration=0.5, t='in_elastic')
        animSeq += Animation(x=xpos, duration=0.5, t='in_back')
        animSeq.start(widget)


    heroHPLabel = ObjectProperty(None)
    knightHPLabel = ObjectProperty(None)
    def updateHPLabels(self):
        self.heroHPLabel.text = 'Hero HP: '+str(self.heroHP)+'/100'
        self.knightHPLabel.text = 'Knight HP: '+str(self.knightHP)+'/100'
    
    heroHPBar = ObjectProperty(None)
    def updateHeroHPBar(self):
        with self.canvas:
            Color(1,0,0,1)
            Rectangle(size=(100,2), pos=(self.heroHPBar.center_x-50, self.heroHPBar.center_y))
            Color(1,1,1,1)
            Rectangle(size=(self.heroHP,2), pos=(self.heroHPBar.center_x-50, self.heroHPBar.center_y))
    
    knightHPBar = ObjectProperty(None)
    def updateKnightHPBar(self):
        with self.canvas:
            Color(1,0,0,1)
            Rectangle(size=(100,2), pos=(self.knightHPBar.center_x-50, self.knightHPBar.center_y))
            Color(1,1,1,1)
            Rectangle(size=(self.knightHP,2), pos=(self.knightHPBar.center_x-50, self.knightHPBar.center_y))

    def checkWin(self):
        if self.knightHP > 0: #nvr win, knight attack
            Clock.schedule_once(lambda dt: self.knightAttack(), 1)
        else:
            self.win()
    
    def checkLose(self):
        if self.heroHP > 0: #nvr lose, attack again
            Clock.schedule_once(lambda dt: self.enableBtns(), 1)
        else:
            self.lose()
    
    def win(self):
        global currentLvlData
        if currentLvlData[3] == 0: #LEVEL COMPLETE
            currentLvlData = [None,None,None,None,100]
            App.get_running_app().root.transition.direction = 'down'
            App.get_running_app().root.current = 'main'
            global userID, lvlChosen
            gdb.updateLvl(userID, lvlChosen, self.heroHP)
            show_LevelCompletePopUp()
            
        else: #LEVEL INCOMPLETE
            currentLvlData[4] = self.heroHP
            App.get_running_app().root.transition.direction = 'down'
            App.get_running_app().root.current = 'maze'
            show_SuccessPopUp()
    
    def lose(self):
        global currentLvlData
        currentLvlData = [None,None,None,None,100]
        App.get_running_app().root.transition.direction = 'down'
        App.get_running_app().root.current = 'main'

        show_DefeatedPopUp()
    
    def getHeroHP(self):
        return self.heroHP
    
    def getKnightHP(self):
        return self.knightHP
    
    avatarImg = ObjectProperty(None)
    petImg = ObjectProperty(None)
    def getImgs(self):
        global avatar, pet, lvlChosen
        self.avatarImg.source = 'other/avatar'+str(avatar+1)+'_fight.png'
        self.petImg.source = 'other/pet'+str(pet+1)+'_fight.png'
        self.knightImg.source = 'other/knight'+str(lvlChosen)+'.png'

class DefeatedPopUp(FloatLayout):
    buttonObj = ObjectProperty(None)
    def getButtonObj(self):
        return self.buttonObj

def show_DefeatedPopUp():
    show = DefeatedPopUp()
    popupWin = Popup(title='Defeated', content=show, size_hint=(None,None), size=(400,90))
    show.getButtonObj().bind(on_press=popupWin.dismiss)
    popupWin.open()

class SuccessPopUp(FloatLayout):
    buttonObj = ObjectProperty(None)
    def getButtonObj(self):
        return self.buttonObj

def show_SuccessPopUp():
    show = SuccessPopUp()
    popupWin = Popup(title='Success', content=show, size_hint=(None,None), size=(400,90))
    show.getButtonObj().bind(on_press=popupWin.dismiss)
    popupWin.open()

class LevelCompletePopUp(FloatLayout):
    #show num of stars completed with (based on lost exp)
    global lvlChosen
    def getStarsImg(self):
        return gdb.getStarsImg(userID)[lvlChosen-1]

    buttonObj = ObjectProperty(None)
    def getButtonObj(self):
        return self.buttonObj

def show_LevelCompletePopUp():
    show = LevelCompletePopUp()
    popupWin = Popup(title='Level Completed', content=show, size_hint=(None,None), size=(400,250))
    show.getButtonObj().bind(on_press=popupWin.dismiss)
    popupWin.open()

screen_manager = ScreenManager()
screen_manager.add_widget(LoginPage())
screen_manager.add_widget(SignUpPage())
screen_manager.add_widget(MainPage()) # display hero (lvl, exp) + pet (lvl, exp), user stats (lvl, exp, current villain) [left top], user guide [left bottom], log out [right top], play [right bottom]
screen_manager.add_widget(MazePage())
screen_manager.add_widget(FightingPage())

class GameApp(App):
    def build(self):
        return screen_manager

if __name__ == '__main__':
    GameApp().run()