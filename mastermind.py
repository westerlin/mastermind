
"""
 Mastermind Thinker demo

 Very simple game of mastermind - trying out Thinker for Python
 By Rasmus Westerlin, Apps'n Downs, December 2017

 Developed for Python 3.6
"""

import tkinter as tk
import random

root = tk.Tk()

import time

frame = tk.Frame(root)
canvas = tk.Canvas(frame, width=400,height=600, highlightthickness=0,highlightbackground="black", relief=tk.FLAT,bg='#aaaaff',bd=0)

#item = canvas.create_rectangle(10,10,100,80, fill='green', outline="green" )
#item = canvas.create_oval(10,10,20,20,fill='green',outline='black')
#item2 = canvas.create_oval(30,30,50,50,fill='blue',outline='black', width=0)

basecolors = ['white','green','red','maroon1','gold','dark orange','dodger blue','grey60']

position = 0
speed = 2

noOfGuesses = 12
codeLength = 4
colorSize = 40
colorpadding = 50

row = 0
cpos = 0

selectColors = []

colorpicks = [[-1 for i in range(codeLength)] for j in range(noOfGuesses)]

def userAction():
    canvas.unbind('<space>')
    canvas.bind('<Left>', lambda _: selectPos(-1))
    canvas.bind('<Right>', lambda _: selectPos(1))
    canvas.bind('<Up>', lambda _: switchColor(1))
    canvas.bind('<Down>', lambda _: switchColor(-1))
    canvas.bind('<Return>', lambda _: switchrow())

def userInAction():
    canvas.unbind("<Left>")
    canvas.unbind("<Right>")
    canvas.unbind("<Up>")
    canvas.unbind("<Down>")
    canvas.unbind("<Return>")

def createCode():
    selection = [x for x in range(len(basecolors))]
    code = []
    for i in range(codeLength):
        codeIndex = random.randint(0,len(selection)-1)
        code.append(selection[codeIndex])
        selection.pop(codeIndex)
    return code

codedColor = createCode()

def initRow():
    global selectColors,tops, bots
    selectColors = [x for x in range(len(basecolors))]
    tops = 0
    bots = 0

def initGame():
    global row, cpos, colorpicks, codedColor
    canvas.itemconfig(board[row][cpos],width=0)
    for i in range(noOfGuesses):
        for j in range(codeLength):
            canvas.itemconfig(board[i][j], fill='#8888dd')
            if i < noOfGuesses - 1:
                canvas.itemconfig(response[i][j], fill='#8888dd')
    colorpicks = [[-1 for i in range(codeLength)] for j in range(noOfGuesses)]
    row = 0
    cpos = 0
    canvas.itemconfig(board[row][cpos],width=1)
    userAction()
    codedColor = createCode()
    initRow()

board = []
response = []
for i in range(noOfGuesses):
    newRow = []
    newResponse = []
    for j in range(codeLength):
        x = colorpadding*j+5
        y = 600 - colorpadding*i - colorSize - 5
        newRow.append(canvas.create_oval(x,y,x+colorSize,y+colorSize,fill='#8888dd',outline='black',width=0))
        if i < noOfGuesses-1:
            x = colorpadding/2*j+255
            y += colorSize/8
            newResponse.append(canvas.create_oval(x+ colorSize/4, y+ colorSize/4, x + colorSize/2, y + colorSize/2, fill='#8888dd', outline='black', width=0))
    board.append(newRow)
    if i < noOfGuesses - 1:
        response.append(newResponse)
initGame()
canvas.itemconfig(board[row][cpos],width=1)

def select(colorPosition):
    canvas.itemconfig(colorPosition, width=5)

def deselect(colorPosition):
    canvas.itemconfig(colorPosition, width=0)

def setcolor(colorPosition,color):
    canvas.itemconfig(colorPosition, fill=color)

def selectPos(increment):
    global cpos
    canvas.itemconfig(board[row][cpos],width=0)
    cpos += increment
    if cpos < 0: cpos = codeLength-1
    if cpos >= codeLength: cpos = 0
    canvas.itemconfig(board[row][cpos],width=1)

def switchColor(increment):
    colorpicks[row][cpos] += increment
    if colorpicks[row][cpos] > len(basecolors)-1: colorpicks[row][cpos] = 0
    if colorpicks[row][cpos] < 0: colorpicks[row][cpos] = len(basecolors)-1
    canvas.itemconfig(board[row][cpos], fill=basecolors[colorpicks[row][cpos]])


def switchrow():
    global row, tops, bots, colorpicks
    for i in range(codeLength):
        if colorpicks[row][i] == -1:
            print("Colors not set {},{}:".format(row,i))
            return False
        for j in range(codeLength):
            if (j==i and codedColor[j]==colorpicks[row][i]): tops += 1
            if (j!=i and codedColor[j]==colorpicks[row][i]): bots += 1
    if tops < codeLength and row < noOfGuesses-2:
        print("tops:{}, bots:{}".format(tops,bots))
        for i in range(tops):
            canvas.itemconfig(response[row][i], fill="black")
        for i in range(bots):
            canvas.itemconfig(response[row][i+tops], fill="white")
        canvas.itemconfig(board[row][cpos],width=0)
        row += 1
        canvas.itemconfig(board[row][cpos],width=1)
        initRow()
        return False
    else:
        print("Row{} tops{} and bots{}".format(row,tops,bots))
        output = True
        if row == noOfGuesses-2:
            output = False
        for i in range(tops):
            canvas.itemconfig(response[row][i], fill="black")
        for i in range(bots):
            canvas.itemconfig(response[row][i+tops], fill="white")
        for i in range(codeLength):
            canvas.itemconfig(board[noOfGuesses-1][i], fill=basecolors[codedColor[i]])
        userInAction()
        canvas.bind("<space>", lambda _: initGame())
        return output


#for i in range(codeLength):
#    canvas.itemconfig(board[noOfGuesses-1][i], fill=basecolors[codedColor[i]])


"""
def moveIt(increment):
    canvas.move(item,increment*speed,0)
    cwidth = eval(canvas.itemcget(item2,'width'))
    print(cwidth)
    cwidth += 0.1
    canvas.itemconfig(item2, width=cwidth)


def moving():
    global position
    canvas.move(item,speed,0)
    position += speed
    if position > 400:
        canvas.move(item,-position,0)
        position = 0
    #root.after(2,moving)
"""
frame.pack()
canvas.pack()

root.title("Mastermind")

#root.after(2000,moving)
#root.mainloop()
canvas.focus_set()
userAction()
canvas.bind("<space>", lambda _: initGame())
#userInAction()

root.mainloop()
"""
while True:
    root.update_idletasks()
    root.update()
    #time.sleep(0.01)
"""
