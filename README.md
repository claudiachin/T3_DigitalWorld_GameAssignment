# URL
Game Video: https://youtu.be/2TwpzC_Pucs

# Aim of the Game
You are a sorcerer, living in a world where magic has been outlawed. Embark on a quest to win your freedom, fighting the Knights that try to stop you along the way.
In this

# How to play the Game
## Sign Up
To start playing, you must first have an account. If you do not have an account, click on 'Sign Up' on the Log In Page (the page when you enter the game). This action should bring you to the Sign Up Page. You will automatically enter the game's Main Page if the account name and password chosen are valid. Else, an error message will pop up.

## Log In
If you already have an account, proceed to enter your details on the Log In Page and click 'Log in'. This will bring you to the Main Page.

## Accessing the User Guide
To learn how to play the game, click on the 'User Guide' button at the bottom left hand corner of the Main Page. The User Guide Popup containing everything you need to know about the gameplay should appear. Click outside the User Guide Popup to close it.

## Choosing your Avatar
In the center of the Main Page, you will find a carousel of Avatars. Swipe right or left to select your avatar. The avatar of choice does not affect your attack power/HP levels.

## Choosing your Pet
In the center of the Main Page, you will find a carousel of pets. Swipe right or left to select your pet. The pet of choice does not affect your attack power/HP levels.

## Choosing your level
To choose which level to play, click on the 'Play' button at the bottom right hand corner of the Main Page. The Play Popup should appear, where you can see the levels available for playing, the stars you have achieved for each level, and the type of Knight (see Game Play) you will be fighting. Click the 'Start' button to begin. This should bring you to the Maze Page.

## Game Play
Currently, there are only 3 levels of game play to complete.

### Maze
Complete the maze to get to the next level, using the movement buttons at the bottom of the screen. Difficulty increases from one maze to the next. In each maze, Knights await to ambush you. Coming across them will lead you to the Fighting Page. Defeat them to continue on your journey.

### Knights
Knights hidden in the Maze will engage in battle with you. Defeat them in a turn-based duel, using the attack buttons at the bottom of the page.

Attack power and uses vary.
Attack 1: Causes damage of HP10-25. Infinite uses.
Attack 2: Causes damage of HP10-30. 3 uses per Knight.
Attack 3: Causes damage of HP10-40. 1 use per Knight.
Pet Attack: Causes damage of HP10-35. 1 use per Knight.

Losing automatically brings you to the Main Page with a popup informing you of your defeat, while winning either lets you continue with the maze or brings you to the Main Page with a popup informing you of your success.

### Stars
Incoplete game: 0 Stars
Complete with below HP30/100: 1 Star
Complete with below HP50/100: 2 Stars
Complete with above HP50/100: 3 Stars

# About the code
There are two important files: the game.py file, and the game.kv file. The kv file contains mostly formatting. Hence, for the kv file, any "logic" used will be explained alongside the corresponding class in the py file.

## game.py
Classes instantiated in this file correspond to the screens that appear in the game. All functions needed on a page are created in the corresponding Class.

### Global Variables
Global variables are required so that information can be passed from page to page. these are userID(str), avatar(int), pet(int), lvlChosen(int), and currentLvlData(list of [x_coord(int), y_coord(int), mazeData(array), knightsLeft(int), heroHP(int)]).

### class LoginPage(Screen)
This class utilises the database created in userdata.py, which reads from userdata.txt to validate registered users.

### class SignUpPage(Screen)
This class utilises the database created in userdata.py, which reads from userdata.txt to register users.
#### class SignUpErrorPopUp(FloatLayout) and def show_SignUpErrorPopUp()
This class and function work together to inform users when their username of choice is already taken in a popup. The class gets the content of the popup from the kv file, and the function (called in the SignUpPage class) opens the popup.

### class MainPage(Screen)
On the Main Page, users:
- Choose which avatar they want to use: Swiping the carousel updates the global variable avatar, via getIndexAvatar() and the on_index function in the kv file.
- Choose which pet they want to use: Swiping the carousel updates the global variable pet, via getIndexPet() and the on_index function in the kv file.
- Access the User Guide: Button labelled 'User Guide' is linked to the UserGuideBtn() function, which opens the a popup (see below).
- Choose which level they want to play: Button labelled 'Play' is linked to the PlayBtn() function, which opens the a popup (see below).
#### class UserGuidePopUp(FloatLayout) and def show_UserGuidePopUp()
This class and function work together to show users the user guide in a popup. The class gets the content of the popup from the kv file, and the function (called in the MainPage class, UserGuideBtn()) opens the popup.
#### class PlayPopUp(FloatLayout) and def show_PlayPopUp()
This class and function work together to let users choose which level they want to play in a popup. The class gets the content of the popup from the kv file, and the function (called in the MainPage class, PlayBtn()) opens the popup.

Swiping the carousel updates the global variable lvlChosen, via getLevel() and the on_index function in the kv file.

The kv file calls the function getStarsImg(), which utilises the database created in usergamedata.py, which reads from usergamedata.txt to get image with the appropriate number of stars for a level.

Pressing the 'Start' button triggers the popup to close and the Maze Page to open (lines 123-127).

### class MazePage(Screen)
Upon opening the Maze Page, global variable currentLvlData is called to initialise the class variables x_coord (where the character is on the x axis), y_coord (where the character is on the y axis), mazeData (how the maze will look like), knightsLeft (knights left to fight in the level), and heroHP (health points the hero has left).

The functions setUp() and createCanvas() are also called (in the kv file). setUP() updates the class variables to the character's starting position, the level maze, the number of knights in the level. createCanvas() then creates the maze based on the updated mazaData.

moveBtn() is called from the kv file, linked to the movement buttons at the bottom of the screen. checkNext() checks for if the movement the player wants to take is valid. If not valid, the character doesnt move.

checkFight() is called from the kv file, after any press of the movement buttons. If the tile the character is on is where a knight is, the global variable currentLvlData is updated for next return to the Maze Page, and the Fighting Page is called.

reset(), as the name suggests, is to reset the global variable currentLvlData back to before any level is selected.

### class FightingPage(Screen)
Upon opening the Fighting Page, the functions setUp(), enableBtns(), and getImgs() are called from the kv file. 

setUp() ensures that the player's character begins with the amount of HP left from the previous fight in the lvl, knights begin with HP100, and that attack uses start from [0,0,0,0]. HP Labels, Hero HP Bars and Knight HP Bars are also updated to reflect the beginning of a fight (see below).

enableBtns() check that buttons have not reached their maximum amount of use per fight using checkBtn(), and enables buttons accordingly.

getImgs() gets the correct avatar, pet and knight for the level.

Characters attack using the buttons at the bottom of the screen. Pressing each buttons causes a series of functions to be called simultaneously from the kv file: 
- attackBtn(): lowers knightHP
- updateHPLabels(): updates to reflect the amount of HP the knight has left after the attack in word format
- updateKnightHPBar(): updates to reflect the amount of HP the knight has left after the attack in bar format
- attackAnimation(): animates Knight being pushed back by attack, and then moving back to original position
- disableBtns(): disables player from attacking during Knight's turn
- checkWin(): checks if player has won. If player has won, then win() is called. Else, the knightAttack() is called after 1 second.

knightAttck() is similar to the hero's attack in which a series of functions are called simultaneously:
- updateHPLabels()
- updateHerotHPBar(): updates to reflect the amount of HP the character has left after the attack in bar format
- attackAnimation()
- checkLose(): checks if player has lost. If player has lost, then lose() is called. Else, the enableBtns() is called after 1 second.

If win() is called and currentLvlData[3], aka knightsLeft, is equal to 0, currentLvlData is reset to before any level is selected, the player returns to the Main Page and the usergamedata database is updated. The Level Completed Popup also shows (see below).

If win() is called and currentLvlData[3], aka knightsLeft, is NOT equal to 0, currentLvlData[4], aka heroHP, is updated to reflect the amount of HP the hero has left. The player returns to the Maze Page and Success Popup shows (see below).

If lose() is called, currentLvlData is reset to before any level is selected. The player returns to the Main Page and Defeated Popup shows (see below).

#### class DefeatedPopUp(FloatLayout) and def show_DefeatedPopUp()
This class and function work together to let inform users when they have been defeated in game in a popup. The class gets the content of the popup from the kv file, and the function (called in the FightingPage class, lose()) opens the popup.
#### class SuccessPopUp(FloatLayout) and def show_SuccessPopUp()
This class and function work together to let inform users when they have been successfully won one of the many knights in a popup. The class gets the content of the popup from the kv file, and the function (called in the FightingPage class, win()) opens the popup.
#### class LevelCompletePopUp(FloatLayout) and def show_LevelCompletePopUp()
This class and function work together to let inform users when they have completed the level in a popup. The class gets the content of the popup from the kv file, and the function (called in the FightingPage class, win()) opens the popup.



# END
Claudia Chin. F03. 1004328. For SUTD Freshmore year 10.009 Digital World Final Assignment 2020. 