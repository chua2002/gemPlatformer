from tkinter import *
root = Tk()
c = Canvas(root,width=500,height=500)

clrList = ["#E1E1E1","#FFFFFF","#0000FF","#c78f40","#000000","#ff4800","#7ebf80"]

class Tile:
    def __init__(self):
        self.xC = 50
        self.yC = 50
        self.w = 100
        self.h = 100
        self.color = "FFFFFF"
        self.outline = "#000000"

    def __init__(self,w):
        self.xC = 50
        self.yC = 50
        self.w = w
        self.h = w
        self.color = "#FFFFFF"
        self.id = 0
    #set values
    def setCenter(self,xC,yC):
        self.xC = xC
        self.yC = yC
    def setSquare(self,n):
        self.h = n
        self.w = n
    def setColor(self,pColor):
        self.color = pColor

    #getValues
    def getCenterX(self):
        return self.xC
    def getCenterY(self):
        return self.yC

    #Draw block
    def drawTile(self):
        lft = self.xC - self.w/2
        rit = self.xC + self.w/2
        top = self.yC -self.h/2
        btm = self.yC + self.h/2
        c.create_rectangle(lft,top,rit,btm, fill=self.color,outline=self.outline)

    def checkTile(self,pX,pY):
        left = self.xC - self.w / 2
        right = self.xC + self.w / 2
        top = self.yC - self.h / 2
        btm = self.yC + self.h / 2
        if pX >left and pX<right and pY>top and pY<btm:
            return True

    def setOutline(self,p):
        self.outline = p

class TileMap():
    def __init__(self):
        self.tileNum = 1
        self.objClrList = []
        self.objectList = []
        self.bkClr = 0
    def setTileNum(self, pNum):
        self.tileNum = pNum
        for x in range(pNum):
            self.objClrList.append([])
            self.objectList.append([])

        for i in range(pNum):
            for x in range(self.tileNum):
                if i ==0 or x ==0 or i==19 or x==19:
                    self.objClrList[i].append(0)
                else:
                    self.objClrList[i].append(self.bkClr)
                self.objectList[i].append(Tile(500/self.tileNum))
                self.objectList[i][x].setSquare(500 / self.tileNum)

    def changeClr(self,x,y):
        self.objClrList[x][y] = int(box.get())
        self.objectList[x][y].setColor(clrList[int(box.get())])
        self.objectList[x][y].drawTile()

    def fullMap(self):
        for i in range(0,self.tileNum):
            for x in range(0, self.tileNum):
                self.objectList[i][x].setCenter((.5 * self.objectList[i][x].h) + self.objectList[i][x].h * x, (.5 * self.objectList[i][x].h) + self.objectList[i][x].h * i)
                self.objectList[i][x].setColor(clrList[self.objClrList[i][x]])
                self.objectList[i][x].drawTile()

    def findTile(self,pX,pY):

        for x in range(self.tileNum):
            for i in range(self.tileNum):
                if self.objectList[i][x].checkTile(pX, pY):
                    return [i,x]


    def gridOff(self,p):
        if p == 1:
            for x in range(self.tileNum):
                for i in range(self.tileNum):
                    self.objectList[x][i].setOutline("")
        else:
            for x in range(self.tileNum):
                for i in range(self.tileNum):
                    self.objectList[x][i].setOutline("#FF0000")

    def getClr(self,pX,pY):
        return self.objClrList[pX][pY]

    def setBkClr(self,pColor):
        self.bkClr = pColor

    def convert(self):
        nL = []
        print(self.objClrList)
        for i in self.objClrList:
            nL.append([])

            for j in i:
                if j == 0: nL[-1].append(1)
                elif j == 1: nL[-1].append(3)
                elif j == 2: nL[-1].append(2)
                elif j == 3: nL[-1].append(4)
                elif j == 4: nL[-1].append(0)
                elif j == 5: nL[-1].append(5)
                elif j == 6: nL[-1].append(6)

        print("[")
        for i in nL: print(i)
        print("]")
    def set1clr(self,x,y,c):
        self.objClrList[y][x] = c



#Create tilemap main===========
window = TileMap()
print(clrList)
window.setBkClr(int(input("What Color background?(enter 0-4)\n")))
window.setTileNum(20)

window.gridOff(0)
window.fullMap()

frame = Frame(root)
box = Spinbox(frame, from_=0,to=6)
box.pack(side=LEFT)

button = Button(frame,text="print",command=window.convert)
button.pack(side=LEFT)
frame.pack()


def mousePress(event):
    try:
        cor = window.findTile(event.x,event.y)
        window.changeClr(cor[0],cor[1])
    except: print(end="")



c.bind("<B1-Motion>",mousePress)




c.pack(side=LEFT)
root.mainloop()