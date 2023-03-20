
import socket
from tkinter import *
from  threading import Thread
from PIL import ImageTk, Image
import random

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

player1_name=''
player2_name=''

player_1_score=0
player_2_score=0


player_1_scorelabel=None
player_2_scorelabel=None

canvas1 = None
canvas2=  None

playerName = None
nameEntry = None
nameWindow = None

finishingBox=None

player_turn=None
roll_btn=None
player_type=None
winningFunctionCall=0

leftBoxes=[]
rightBoxes=[]

dice=None

gameWindow=None

def savename():
    global playerName
    global nameEntry
    global nameWindow
    global SERVER

    playerName=nameEntry.get()
    nameEntry.delete(0,END)

    nameWindow.destroy()
    SERVER.send(playerName.encode("utf-8"))
    callgameWindow()

def resetGame():
    SERVER.send("Reset Game".encode("utf-8"))

def handleWin(msg):
    global roll_btn,player_type

    if "red" in msg:
        if player_type=='player 2':
            roll_btn.destoy()
    if "yellow" in msg:
        if player_type=='player 1':
            roll_btn.destroy()
    
    # add winning message

def updateScore(msg):
    global player_1_score,player_2_score
    if 'red' in msg:
        player_1_score+=1

    if 'yellow' in msg:
        player_2_score+=1

    canvas2.itemconfigure(player_1_scorelabel,text=player_1_score)
    canvas2.itemconfigure(player_2_scorelabel,text=player_2_score)
    
def callgameWindow():
    global gameWindow,canvas2,screen_height,screen_width,dice,roll_btn,player_1_score,player1_name,player2_name,player_2_score,player_1_scorelabel,player_2_scorelabel

    gameWindow=Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes("-fullscreen",True)
    screen_width=gameWindow.winfo_screenwidth()
    screen_height=gameWindow.winfo_screenheight()

    bg=ImageTk.PhotoImage(file="./assets/background.png")
    canvas2=Canvas(gameWindow,width=500,height=500)
    canvas2.pack(fill="both",expand=True)

    canvas2.create_image(0,0,image=bg,anchor="nw")

    # add text
    canvas2.create_text(screen_width/2,screen_height/5,text="Ludo Ladder",font=("helvetica",100),fill="white")

    # decllaring winning message

    winning_msg=canvas2.create_text(screen_width/2,screen_height/2,text="",font=("helvetica",20),fill='white')

    # creating reset button
    reset_btn=Button(gameWindow,text='Restart',font=("helvetica",20),fg='black',bg='grey',width=20,height=5,command=resetGame)

    gameWindow.resizable(True,True)
    leftBoard()
    rightBoard()
    finishing_Box()

    dice=canvas2.create_text(screen_width/2+10,screen_height/2+150,text="\u2680",font=("helvetica",250),fill='white')

    roll_btn=Button(gameWindow,text='Roll Dice',fg='black',bg='white',width=20,height=5,font=("helvetica",20),command=rollDice)

    if player_type=='player 1' and player_turn==True:
        roll_btn.place(x=screen_width/2-100,y=screen_height/2+250)
    else:
        roll_btn.pack_forget()
    
    # creating name board
    player1_label=canvas2.create_text(400,screen_height/2+150,text=player1_name,font=("helvetica",20),fill='white')
    player2_label=canvas2.create_text(400,screen_height/2+190,text=player2_name,font=("helvetica",20),fill='white')

    # displaying the scores
    player_1_scorelabel=canvas2.create_text(600,screen_height/2+150,text=player_1_score)
    player_2_scorelabel=canvas2.create_text(600,screen_height/2+190,text=player_2_score)

    gameWindow.mainloop()

    
def leftBoard():
    global gameWindow,leftBoxes,screen_height,screen_width
    x_pos=30
    for i in range(11):
        if i==0:
            boxlabel=Label(gameWindow,font=("helvetica",55),width=2,height=1,bg="red",borderwidth=0.5,relief="ridge")
            boxlabel.place(x=x_pos,y=screen_height/2-100)
            leftBoxes.append(boxlabel)
            x_pos+=50
        else:
            boxlabel=Label(gameWindow,font=("helvetica",55),width=2,height=1,bg="white",borderwidth=0.5,relief="ridge")
            boxlabel.place(x=x_pos,y=screen_height/2-100)
            leftBoxes.append(boxlabel)
            x_pos+=85

def rightBoard():
    global gameWindow,rightBoxes,screen_height
    x_pos=970
    for i in range(11):
        if i==10:
            boxlabel=Label(gameWindow,font=("helvetica",55),width=2,height=1,bg="yellow",borderwidth=0.5,relief="ridge")
            boxlabel.place(x=x_pos,y=screen_height/2-100)
            rightBoxes.append(boxlabel)
            x_pos+=50
        else:
            boxlabel=Label(gameWindow,font=("helvetica",55),width=2,height=1,bg="white",borderwidth=0.5,relief="ridge")
            boxlabel.place(x=x_pos,y=screen_height/2-100)
            rightBoxes.append(boxlabel)
            x_pos+=85
        
def finishing_Box():
    global gameWindow,screen_height,screen_width,finishingBox

    finishingBox=Label(gameWindow,text='HOME',font=("helvetica",30),width=8,height=4,bg="green",fg="white")
    finishingBox.place(x=screen_width/2-60,y=screen_height/2-150)

def rollDice():
    global SERVER,roll_btn,player_turn,player_type
    dice_choices=["\u2680","\u2681","\u2682","\u2683","\u2684","\u2685"]
    random_value=random.choice(dice_choices)
    roll_btn.destroy()
    player_turn=False

    if player_type=="player1":
        SERVER.send(f"{random_value} player 2 turn".encode("utf-8"))
    elif player_type=="player2":
        SERVER.send(f"{random_value} player 1 turn".encode("utf-8"))

def checkColorPosition(boxes,color):
    for box in boxes:
        boxcolor=box.cget("bg")
        if boxcolor==color:
            return boxes.index(box)
    return False

def moveplayerone(steps):
    global leftBoxes,finishing_Box,SERVER
    box_position=checkColorPosition(leftBoxes[1:],'red')

    if box_position:
        dice_value=steps
        colored_box_index=box_position
        total_steps=10
        remaining_steps=total_steps-colored_box_index

        if dice_value==remaining_steps:
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            finishing_Box.configure(bg='red')
            SERVER.send('Red wins the game'.encode("utf-8"))
        
        elif dice_value<remaining_steps:
            for box in leftBoxes[1:]:
                box.configure(bg='white')
            
            next_step=colored_box_index+1+dice_value
            leftBoxes[next_step].configure(bg='red')
        
        else:
            print("Cannot move!!")

    else:
        print("pawn is not on the board\n roll the dice again to get a six")

def moveplayertwo(steps):
    global rightBoxes,finishing_Box,SERVER
    temp_boxes=rightBoxes[-2::-1]
    box_position=checkColorPosition(rightBoxes[-2::-1],'yellow')

    if box_position:
        dice_value=steps
        colored_box_index=box_position
        total_steps=10
        remaining_steps=total_steps-colored_box_index

        if dice_value==remaining_steps:
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            finishing_Box.configure(bg='yellow')
            SERVER.send('yellow wins the game'.encode("utf-8"))
        
        elif dice_value<remaining_steps:
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')
            
            next_step=colored_box_index+1+dice_value
            rightBoxes[-2::-1][next_step].configure(bg='yellow')
        
        else:
            print("Cannot move!!")

    else:
        print("pawn is not on the board\n roll the dice again to get a six")

def askPlayerName():
    global playerName,nameEntry,nameWindow

    nameWindow=Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes("-fullscreen",True)
    screen_width=nameWindow.winfo_screenwidth()
    screen_height=nameWindow.winfo_screenheight()

    # backgroud image
    bg=ImageTk.PhotoImage(file="./assets/background.png")
    canvas=Canvas(nameWindow,width=500,height=500)
    canvas.pack(fill="both",expand=True)

    canvas.create_image(0,0,image=bg,anchor="nw")
    canvas.create_text(screen_width/2+30,screen_height/4,text="Enter Name",font=("helvetica",100),fill="white")

    nameEntry=Entry(nameWindow,width=15,justify="center",font=("helvetica",50))
    nameEntry.place(x=screen_width/2-200,y=screen_height/4+100)
    print("********************************name entry************************")

    btn=Button(nameWindow,text="Login",width=15,height=2,font=("helvetica",30),command=savename)
    btn.place(x=screen_width/2-150,y=screen_height/2)

    nameWindow.mainloop()

def recv_msg():
    global SERVER,player1_name,player2_name
    while True:
        msg=SERVER.recv(2048).decode('utf-8')
        if 'player_type' in msg:
            recv_message=eval(msg)
            player_type=recv_message['player_type']
            player_turn=recv_message['turn']
        elif 'player_names' in msg:
            players=eval(msg)
            players=players['player_names']
            print(players)

            for p in players:

                if (p['type']=='player 1'):
                    player1_name=p['player_name']

                elif (p['type']=='player 2'):
                    player2_name=p['player_name']
        elif('⚀' in msg):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in msg):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in msg):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in msg):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in msg):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in msg):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')
        #--------- Boilerplate Code Start--------
        elif('wins the game.' in msg and winingFunctionCall == 0):
            winingFunctionCall +=1
            print(msg)
            handleWin(msg)
            # Addition Activity
            updateScore(msg)
        # elif(msg == 'reset game'):
            # handleResetGame()

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread=Thread(target=recv_msg)
    thread.start()
    # Creating First Window
    askPlayerName()


setup()
