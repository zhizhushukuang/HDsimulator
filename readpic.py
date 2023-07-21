from math import pi
import json
import pygame
import os
import cv2
import numpy as np
from pygame import surface
from pygame.draw import circle
from pygame.locals import *

ConfigPath = os.getcwd() + "\picconfig.json"
PicPath = os.getcwd() + "\IMGNEXT.png"
IMGPATH=os.getcwd() + "\IMG.png"
UsedColorQueue = []
WalkedPath = []
# 游戏窗口大小
Quad=60
WIDTH = 9 * Quad
HEIGHT = 12 * Quad

# 颜色定义
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
RAINBOW = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
READYTOCHANGE=(202,178,114)

MonsterColor = pygame.Color(255,255,255)
LineColor = pygame.Color(128,0,128)
BaseColor = [BLUE,RED,YELLOW,GREEN,RAINBOW]
WalkedPath = []
CurrentIndex = 0
NewColorList = []
def ChangeQuadColor(Position, SquareColor, NewColor):
    x = int(Position[0] / Quad)
    y = int(Position[1] / Quad)
    SquareColor[y][x] = NewColor

def ReadInPic():
    img = cv2.imread(PicPath)
    try:
        img2 = cv2.imread(IMGPATH)
        img2 = cv2.resize(img2,None,fx=0.5,fy=0.5)
        cv2.imshow("output2", img2)
    except:
        return
    try:
        img.shape
    except:
        return
    HEIGHT,WIDTH = img.shape[:2]
    initpoint = (int(WIDTH*0.43),int(HEIGHT*0.1))
    k = [30, 30.75, 31.5, 32.25, 33, 33.75, 34.5, 35.25, 36]
    k2 = np.math.tan(pi* 5 / 6)
    deltax = WIDTH * 0.05
    SquareColor = []
    for i in range(0,9):
        linestartpoint = (int(initpoint[0] - deltax * i), int(initpoint[1] - deltax * i *k2))
        k1 = np.math.tan((k[i]-2) / 180 * pi)
        b = linestartpoint[1] - linestartpoint[0] * k1
        LineColor = []
        for j in range(0,9):
            pointx = int(linestartpoint[0] + j * deltax)
            pointy = int(linestartpoint[1] + j * deltax * k1)
            if(pointx>WIDTH):
                pointx=WIDTH-1
            if(pointy>HEIGHT):
                pointy=HEIGHT-1
            point = (pointx,pointy)
            color = img[pointy,pointx]

            isBlue = (color[0] > (color[1] * 1.3)) & (color[0] > (color[2] * 1.3))
            isGreen = (color[1] > (color[0] * 1.3)) & (color[1] > (color[2] * 1.3))
            isRed = (color[2] > (color[0] * 1.3)) & (color[2] > (color[1] * 1.3))
            isYellow = (color[2] > (color[0] * 1.3)) & (color[1] > (color[0] * 1.3))
            PointColor = (0,0,0)
            if isBlue:
                PointColor = (255,0,0)
                LineColor.append(1)
            elif isRed:
                PointColor = (0,0,255)
                LineColor.append(2)
            elif isGreen:
                PointColor = (0,255,0)
                LineColor.append(4)
            elif isYellow:
                PointColor = (0,255,255)
                LineColor.append(3)
            else:
                LineColor.append(6)
            cv2.circle(img,point,2,PointColor,4)
        SquareColor.append(LineColor)
    Config = None
    with open(ConfigPath, 'r') as f:
        Config = json.load(f)
    Config["InitQuads"] = SquareColor

    NewConfigPathTmp = os.getcwd() + "\\NewConfigTmp.txt"
    NewConfigPath = os.getcwd() + "\picconfig.json"

    f = open(NewConfigPathTmp,'w+')
    json.dump(Config, f, indent = 0, separators = (",",":"))
    f.close()
    with open(NewConfigPathTmp,"r") as fin:
        with open(NewConfigPath, "w+") as fout:
            for line in fin:
                if not ("]," in line):
                    fout.write(line.replace("\n",""))
                else:
                    fout.write(line)
    os.remove(NewConfigPathTmp)
    img.resize()
    img = cv2.resize(img,None,fx=0.5,fy=0.5)
    cv2.imshow("output", img)
   
def GoOneStep(screen, Position, SquareColor):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    global NewColorList
    PathLength = len(WalkedPath)
    x = int(Position[0] / Quad)
    y = int(Position[1] / Quad)
    WalkedPath.append([x,y])
    pos = WalkedPath[PathLength-1]
    x = pos[0]
    y = pos[1]
    UsedColorQueue.append(SquareColor[y][x])

    CurrentIndex = CurrentIndex + 1
    print("Used Queue:")
    print(UsedColorQueue)
    print(NewColorList)
    print("WalkedPath:")
    print(WalkedPath)
    print("go one step")

def BackOneStep(screen, SquareColor):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    QuadColor = UsedColorQueue.pop()
    LastPos=WalkedPath.pop()
    if(len(WalkedPath)>0):
        LastPos = WalkedPath[len(WalkedPath) - 1]
    x = LastPos[0]
    y = LastPos[1]
    SquareColor[y][x] = QuadColor
    CurrentIndex = CurrentIndex - 1
    print("Used Queue:")
    print(UsedColorQueue)
    print(NewColorList)
    print("WalkedPath:")
    print(WalkedPath)
    print("back one step")

def OutputNewConfig(Config):
    global NewColorList
    NewConfigPathTmp = os.getcwd() + "\\NewConfigTmp.txt"
    NewConfigPath = os.getcwd() + "\\NewColorListjson.json"
    NewConfig = dict()
    NewConfig["QuadsColorList"] = NewColorList
    f = open(NewConfigPathTmp,'w+')
    json.dump(NewConfig, f, indent = 0, separators = (",",":"))
    f.close()
    with open(NewConfigPathTmp,"r") as fin:
        with open(NewConfigPath, "w+") as fout:
            for line in fin:
                if not ("]," in line):
                    fout.write(line.replace("\n",""))
                else:
                    fout.write(line)
    os.remove(NewConfigPathTmp)
        

def main():
    print(cv2.__file__)
    ReadInPic()

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Alchemy star sim')

    Config = None
    with open(ConfigPath, 'r') as f:
        NewColorListjson = json.load(f)
    #print(Config)
    editing_mode = False
    
    SquareColor = NewColorListjson["InitQuads"]
    LastPos = []
    while True:
        screen.fill((0))
        
        for i in range(0,9):
            for j in range(0,9):
                if (SquareColor[i][j] != 6):
                    QuadColor = BaseColor[SquareColor[i][j]-1]
                    pygame.draw.rect(screen, QuadColor, pygame.Rect(j*Quad, i*Quad, j*Quad+Quad, i*Quad+Quad))
                else:
                    pygame.draw.rect(screen, BLACK, pygame.Rect(j*Quad, i*Quad, j*Quad+Quad, i*Quad+Quad))
                pygame.draw.rect(screen, BLACK, pygame.Rect(j*Quad, i*Quad, j*Quad+Quad, i*Quad+Quad), 1)
        pygame.draw.rect(screen, BLACK,Rect(0,WIDTH,WIDTH,HEIGHT))
        ##画网格


        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_r:
                    OutputNewConfig(NewColorListjson)
                    print("LOAD NewColorListjson")
                elif event.key == K_ESCAPE :
                    editing_mode = not editing_mode
                    print("editing_mode:",editing_mode)
                    print("KEYUP:",event.key)
                if (editing_mode == True):
                        if event.key == K_1:
                            ChangeQuadColor(LastPos,SquareColor,1)
                        if event.key == K_2:
                            ChangeQuadColor(LastPos,SquareColor,2)
                        if event.key == K_3:
                            ChangeQuadColor(LastPos,SquareColor,3)
                        if event.key == K_4:
                            ChangeQuadColor(LastPos,SquareColor,4)
                        if event.key == K_5:
                            ChangeQuadColor(LastPos,SquareColor,5)
                        if event.key == K_6:
                            ChangeQuadColor(LastPos,SquareColor,6)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                LastPos = event.pos
                x = int(LastPos[0] / Quad)
                y = int(LastPos[1] / Quad)
                if event.button == 1:
                    print(event.pos)
                    if ((event.pos[0] < WIDTH) & (event.pos[1] < WIDTH)  & (not editing_mode)):
                        NewColorList.append(SquareColor[y][x])
                        GoOneStep(screen,event.pos,SquareColor)
                        
                elif event.button == 3:
                    if ((CurrentIndex > 0) ):
                        NewColorList.pop()
                        BackOneStep(screen,SquareColor)
                        

        if (len(WalkedPath) >= 1):
            for i in range(0,len(WalkedPath)-1):
                start = [WalkedPath[i][0] * Quad + 0.5 * Quad, WalkedPath[i][1] * Quad + 0.5 * Quad]
                end = [WalkedPath[i+1][0] * Quad + 0.5 * Quad, WalkedPath[i+1][1] * Quad + 0.5 * Quad]
                pygame.draw.line(screen, LineColor, start, end, 1)
            x = WalkedPath[len(WalkedPath) - 1][0]
            y = WalkedPath[len(WalkedPath) - 1][1]
            pygame.draw.rect(screen,BLACK,pygame.Rect(x*Quad, y*Quad, Quad, Quad))
            Length = len(WalkedPath)
            LengthFont = pygame.font.SysFont("",32)
            LengthText = LengthFont.render(str(Length),True,RED,BLACK)
            screen.blit(LengthText,(x*Quad,y*Quad))
        

        pygame.display.update()


if __name__ == '__main__':
    main()