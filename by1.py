import json
import pygame
import os
import math
from pygame import surface
from pygame.draw import circle
from pygame.locals import *
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
READYTOCHANGEcolor=0
READYTOCHANGEcolor2=7

bechangedcolor1=2
bechangedcolor2=3
bechangedcolorto=4#1是蓝色，2是红色，3是黄色，4是绿色
LastPos = []
rexcolor=[]
reycolor=[]
BaseColor = [BLUE,RED,YELLOW,GREEN,RAINBOW]
PlayerColor = pygame.Color(114,51,4)
MonsterColor = pygame.Color(255,255,255)
LineColor = pygame.Color(128,0,128)
UsedColorQueue = []
used_priority_list=[]
priority_list=[]
fixpriority_list=0
CurrentIndex = 0
rerskillrect=[[7]*9 for i in range(9)]
# 读取配置文件

def ChangeQuadColor(Position, SquareColor, NewColor):
    x = int(Position[0] / Quad)
    y = int(Position[1] / Quad)
    SquareColor[y][x] = NewColor
    

def GoOneStep(screen, ColorList, Position, SquareColor):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    global used_priority_list
    global priority_list
    global fixpriority_list
    QuadColor = BaseColor[ColorList[CurrentIndex]]
    PathLength = len(WalkedPath)
    x = int(Position[0] / Quad)
    y = int(Position[1] / Quad)
    WalkedPath.append([x,y])
    pos = WalkedPath[PathLength-1]
    x = pos[0]
    y = pos[1]
    UsedColorQueue.append(SquareColor[y][x])
    used_priority_list.append(CurrentIndex+fixpriority_list)
    priority_list[y][x]=CurrentIndex+fixpriority_list
    SquareColor[y][x] = ColorList[CurrentIndex]
    CurrentIndex = CurrentIndex + 1
    print("Used Queue:")
    print(UsedColorQueue)
    print("WalkedPath:")
    print(WalkedPath)
    print("go one step")

def BackOneStep(screen, ColorList, SquareColor):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    global priority_list
    global used_priority_list
    global fixpriority_list
    QuadColor = UsedColorQueue.pop()
    WalkedPath.pop()
    LastPos = WalkedPath[len(WalkedPath) - 1]
    x = LastPos[0]
    y = LastPos[1]
    repriority_list=used_priority_list.pop()
    priority_list[y][x]=repriority_list
    SquareColor[y][x] = QuadColor
    CurrentIndex = CurrentIndex - 1
    print("Used Queue:")
    print(UsedColorQueue)
    print("WalkedPath:")
    print(WalkedPath)
    print("back one step")

def distance_from_given_point(point,given_point):
    x, y = point
    distance = math.sqrt((x - given_point[0]) ** 2 + (y - given_point[1]) ** 2)
    return distance
def fixmathatan2(x,y):
    arc=math.atan2(x,y)
    if(math.atan2(x,y)<0):
        arc=math.atan2(x,y)+2*math.pi
    else:
        arc=math.atan2(x,y)
    return arc

def youxianjipaixu(list1, player_position):
    sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (player_position[0],player_position[1])), -fixmathatan2(player_position[0]-point[0],player_position[1]-point[1])))
    return sorted_points

def skill_q(screen, position, init_quads,changenumber):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    global reinit_quads
    global bechangedcolor1
    global READYTOCHANGEcolor
    reinit_quads=init_quads
    list1=[]
    player_position=position
    x=player_position[0]
    y=player_position[1]
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==bechangedcolor1):
                list1.append([j,i])
    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -priority_list[point[0]][point[1]]))          
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(point[1]-player_position[1],point[0]-player_position[0])))    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(point[0]-player_position[0],point[1]-player_position[1])))    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(player_position[1]-point[1],player_position[0]-point[0])))    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(player_position[0]-point[0],player_position[1]-point[1]))) 
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(point[1]-player_position[1],point[0]-player_position[0])))    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(point[0]-player_position[0],point[1]-player_position[1])))    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(player_position[1]-point[1],player_position[0]-point[0])))    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(player_position[0]-point[0],player_position[1]-point[1])))         
    sorted_points=youxianjipaixu(list1, player_position)
    k=0          
    for i in range(0,min(changenumber,len(list1))):
        obj1=sorted_points[i+k]
        x1=obj1[0]
        y1=obj1[1]
        if(x==x1 and y==y1):
            k=1
            obj1=sorted_points[i+k]
            x1=obj1[0]
            y1=obj1[1]
        
        init_quads[y1][x1]=READYTOCHANGEcolor
    print(sorted_points)

def REskill_q(screen, init_quads):
    global bechangedcolor1
    global READYTOCHANGEcolor
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==READYTOCHANGEcolor):
                init_quads[i][j]=bechangedcolor1

def ENskill_q(screen, init_quads):
    global bechangedcolorto
    global READYTOCHANGEcolor
    
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==READYTOCHANGEcolor):
                init_quads[i][j]=bechangedcolorto
    
def skill_w(screen, position, init_quads,changenumber):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    global reinit_quads
    global bechangedcolor1
    global bechangedcolor2
    global READYTOCHANGEcolor
    global READYTOCHANGEcolor2
    reinit_quads=init_quads
    list1=[]
    player_position=position
    x=player_position[0]
    y=player_position[1]
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==bechangedcolor1 or init_quads[i][j]==bechangedcolor2):
                list1.append([j,i])
    
    #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(player_position[0]-point[0],player_position[1]-point[1])))         
    sorted_points=youxianjipaixu(list1, player_position)            
    k=0           
    for i in range(0,min(changenumber,len(list1))):
        obj1=sorted_points[i+k]
        x1=obj1[0]
        y1=obj1[1]
        if(x==x1 and y==y1):
            k=1
            obj1=sorted_points[i+k]
            x1=obj1[0]
            y1=obj1[1]
        if (init_quads[y1][x1]==bechangedcolor1):
            init_quads[y1][x1]=READYTOCHANGEcolor
        else:
            init_quads[y1][x1]=READYTOCHANGEcolor2
    print(sorted_points)

def REskill_w(screen, init_quads):
    global bechangedcolor1
    global READYTOCHANGEcolor
    global bechangedcolor2
    global READYTOCHANGEcolor2
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==READYTOCHANGEcolor):
                init_quads[i][j]=bechangedcolor1
            if(init_quads[i][j]==READYTOCHANGEcolor2):
                init_quads[i][j]=bechangedcolor2    

def ENskill_w(screen, init_quads):
    global bechangedcolorto
    global READYTOCHANGEcolor
    
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==READYTOCHANGEcolor or init_quads[i][j]==READYTOCHANGEcolor2 ):
                init_quads[i][j]=bechangedcolorto

def skill_e(screen, position, init_quads):
    global reinit_quads
    global READYTOCHANGEcolor
    global rexcolor
    global reycolor
    reinit_quads=init_quads
    player_position=position
    y=player_position[0]
    x=player_position[1]
    for i in range(0,9):
        if(i!=y and init_quads[x][i]!=6):
            rexcolor.append(init_quads[x][i])
            init_quads[x][i]=READYTOCHANGEcolor   
    for i in range(0,9):
        if(i!=x and init_quads[i][y]!=6):
            reycolor.append(init_quads[i][y])
            init_quads[i][y]=READYTOCHANGEcolor
            
def REskill_e(screen,position, init_quads):
    global READYTOCHANGEcolor
    global rexcolor
    global reycolor
    player_position=position
    y=player_position[0]
    x=player_position[1]
    k=0#遇到黑色格子的修正
    for i in range(0,9):
            if(init_quads[i][y]==6):
                k=k+1
            elif(init_quads[i][y]==READYTOCHANGEcolor):
                if(i<x):
                    init_quads[i][y]=reycolor[i-k]
                else:
                    init_quads[i][y]=reycolor[i-1-k]
    k=0
    for i in range(0,9):
            if(init_quads[x][i]==6):
                k=k+1
            elif(init_quads[x][i]==READYTOCHANGEcolor):
                if(i<y):
                    init_quads[x][i]=rexcolor[i-k]
                else:
                    init_quads[x][i]=rexcolor[i-1-k]  
    k=0
    rexcolor.clear()
    reycolor.clear()       

def ENskill_e(screen, init_quads):
    global bechangedcolorto
    global READYTOCHANGEcolor
    global reycolor
    global rexcolor
    for i in range(0,9):
         for j in range(0,9):
            if(init_quads[i][j]==READYTOCHANGEcolor ):
                init_quads[i][j]=bechangedcolorto
    rexcolor.clear()
    reycolor.clear()

def OutputNewconfig(Config, ColorList, SquareColor):
    LastPos = WalkedPath[len(WalkedPath) - 1]
    x = LastPos[0]
    y = LastPos[1]
    SquareColor[y][x] = -1
    NewColorList = []
    for i in range(CurrentIndex,len(ColorList)):
        NewColorList.append(ColorList[i])
    NewconfigPathTmp = os.getcwd() + "\\NewconfigTmp.txt"
    NewconfigPath = os.getcwd() + "\\Newconfig.json"
    Newconfig = dict()
    Newconfig["InitQuads"] = SquareColor
    Newconfig["priority_list"]=priority_list
    Newconfig["PlayerPosition"] = [x,y]
    Newconfig["MonsterPosition"] = Config["MonsterPosition"]
    Newconfig["bechangedcolor1"]=bechangedcolor1
    Newconfig["bechangedcolor2"]=bechangedcolor2
    Newconfig["bechangedcolorto"]=bechangedcolorto
    Newconfig["fixpriority_list"]=CurrentIndex
    Newconfig["QuadsColorList"] = NewColorList
    f = open(NewconfigPathTmp,'w+')
    json.dump(Newconfig, f, indent = 0, separators = (",",":"))
    f.close()
    with open(NewconfigPathTmp,"r") as fin:
        with open(NewconfigPath, "w+") as fout:
            for line in fin:
                if not ("]," in line):
                    fout.write(line.replace("\n",""))
                else:
                    fout.write(line)
    os.remove(NewconfigPathTmp)

def main():
    global CurrentIndex
    global bechangedcolorto
    global bechangedcolor1
    global bechangedcolor2
    global priority_list
    global fixpriority_list
    temp=[]
    config_path = "config.json"
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            init_quads = config["InitQuads"]
            reinit_quads=[]
            quads_color_list = config["QuadsColorList"]
            player_position =config["PlayerPosition"]
            bechangedcolor1=config["bechangedcolor1"]
            bechangedcolor2=config["bechangedcolor2"]
            bechangedcolorto=config["bechangedcolorto"]
            WalkedPath.append(player_position)
            priority_list=config["priority_list"]
            fixpriority_list=config["fixpriority_list"]
    except FileNotFoundError:
        print("无法加载盘面。请确保有名为 'board.json' 的正确格式的文件。")
        return

    # 初始化Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect the Dots")

    # 游戏状态
    editing_mode = False
    qskill_mode=False
    wskill_mode=False
    eskill_mode=False
    rskill_mode=False
    x,y=player_position
    path = [player_position]
    used_colors = []

    # 游戏循环
    running = True
    while running:
        screen.fill(BLACK)

        # 绘制网格
        for i in range(9):
            for j in range(9):
                color = init_quads[i][j]
                if color != 6 and color !=0 and color !=7 :
                    pygame.draw.rect(screen, BaseColor[color-1], (j * 60, i * 60, 60, 60))
                elif color == 0 or color ==7:
                    pygame.draw.rect(screen, READYTOCHANGE, (j * 60, i * 60, 60, 60))
                else:
                    pygame.draw.rect(screen, BLACK, (j * 60, i * 60, 60, 60))
                pygame.draw.rect(screen, (255, 255, 255), (j * 60, i * 60, 60, 60), 1)

        # 绘制玩家路径
        for i in range(1, len(path)):
            pygame.draw.line(screen, (255, 255, 255), (path[i - 1][1] * 60 + 30, path[i - 1][0] * 60 + 30),
                            (path[i][1] * 60 + 30, path[i][0] * 60 + 30), 3)

        # 绘制玩家
        pygame.draw.circle(screen, PlayerColor, (player_position[0] * 60 + 30, player_position[1] * 60 + 30), 20)
        
        MonsterPosition = config["MonsterPosition"]
        

        for Pos in MonsterPosition:
                Center = [Pos[0] * Quad + 0.5*Quad, Pos[1] * Quad + 0.5*Quad]
                pygame.draw.circle(screen,MonsterColor, Center, 0.3*Quad)
        
        

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                print("KEYUP:",event.key)
                if event.key == K_ESCAPE :
                    editing_mode = not editing_mode
                    print("editing_mode:",editing_mode)
                    print("KEYUP:",event.key)
                elif event.key == K_q:
                    qskill_mode=not qskill_mode
                    print("qskill_mode:",qskill_mode)
                elif event.key == K_w:
                    wskill_mode=not wskill_mode
                    print("wskill_mode:",wskill_mode)
                elif event.key == K_e:
                    eskill_mode=not eskill_mode
                    print("eskill_mode:",eskill_mode)
                elif event.key == K_r:
                    rskill_mode=not rskill_mode
                    print("rskill_mode:",rskill_mode)
                elif event.key == K_t:
                    if CurrentIndex < len(quads_color_list):
                        CurrentIndex=CurrentIndex+1
                elif event.key == 32:
                    if(CurrentIndex>0):
                        CurrentIndex=CurrentIndex-1
                elif event.key == K_RETURN:
                    # 按下回车键，移动到连线终点并填充路径上的方块
                    player_position=WalkedPath[len(WalkedPath)-1]
                    WalkedPath.clear()
                    WalkedPath.append(player_position)
                    CurrentIndex=CurrentIndex+1
                    pygame.display.update()
                    pass  # 在这里实现移动和填充方块的逻辑
                if (editing_mode == True):
                        if event.key == K_1:
                            ChangeQuadColor(LastPos,init_quads,1)
                        if event.key == K_2:
                            ChangeQuadColor(LastPos,init_quads,2)
                        if event.key == K_3:
                            ChangeQuadColor(LastPos,init_quads,3)
                        if event.key == K_4:
                            ChangeQuadColor(LastPos,init_quads,4)
                        if event.key == K_5:
                            ChangeQuadColor(LastPos,init_quads,5)
                        if event.key == K_6:
                            ChangeQuadColor(LastPos,init_quads,6)
                        pygame.display.update()
                elif(qskill_mode == True):
                        if event.key == K_1:
                            skill_q(screen,(x,y),init_quads,4)
                        if event.key == K_2:
                            skill_q(screen,(x,y),init_quads,5)
                        if event.key == K_3:
                            skill_q(screen,(x,y),init_quads,6)
                        if event.key == K_4:
                            REskill_q(screen,init_quads)
                            qskill_mode=not qskill_mode
                            print("REskill_q")   
                        if event.key == K_5:
                            ENskill_q(screen,init_quads)
                            qskill_mode=not qskill_mode
                        pygame.display.update()
                elif(wskill_mode == True):
                        if event.key == K_1:
                            skill_w(screen,(x,y),init_quads,4)
                        if event.key == K_2:
                            skill_w(screen,(x,y),init_quads,5)
                        if event.key == K_3:
                            skill_w(screen,(x,y),init_quads,6)
                        if event.key == K_4:
                            REskill_w(screen,init_quads)
                            wskill_mode=not wskill_mode
                            print("REskill_w")   
                        if event.key == K_5:
                            ENskill_w(screen,init_quads)
                            wskill_mode=not wskill_mode
                            print("REskill_w") 
                        
                elif(eskill_mode == True):
                        if event.key == K_1:
                            skill_e(screen,(x,y),init_quads)
                        if event.key == K_2:
                            REskill_e(screen,(x,y),init_quads)
                            eskill_mode=not eskill_mode
                            print("REskill_e")   
                        if event.key == K_3:
                            ENskill_e(screen,init_quads)
                            eskill_mode=not eskill_mode
                            print("REskill_e") 
                        
                
                
            elif event.type == MOUSEBUTTONDOWN:
                LastPos = event.pos
                x = int(LastPos[0] / Quad)
                y = int(LastPos[1] / Quad)
                if event.button == 1:
                    print(event.pos)
                    if ((CurrentIndex < len(quads_color_list)) & (event.pos[0] < WIDTH) & (event.pos[1] < WIDTH) & (not editing_mode) & (not qskill_mode)& (not wskill_mode)& (not eskill_mode)& (not rskill_mode)):
                            
                            GoOneStep(screen,quads_color_list,event.pos,init_quads)
                    elif(rskill_mode):
                        rerskillrect[y][x]=init_quads[y][x]
                        ChangeQuadColor(LastPos,init_quads,bechangedcolorto)
                    elif ((event.pos[1] > 9*Quad) & (event.pos[1] < 11*Quad)):
                            OutputNewconfig(config, quads_color_list, init_quads)
                if event.button == 2:
                    if(not rskill_mode):
                        OutputNewconfig(config, quads_color_list, init_quads)
                        print("记录了当前情况到newconfig.json")
                    elif(rerskillrect[y][x]!=7):
                        ChangeQuadColor(LastPos,init_quads,rerskillrect[y][x])
                elif event.button == 3:
                    if ((len(WalkedPath) >= 2) & (not editing_mode)& (not qskill_mode)& (not wskill_mode)& (not eskill_mode)& (not eskill_mode)& (not rskill_mode)):
                            BackOneStep(screen,quads_color_list,init_quads)
                    elif(rskill_mode):
                        rerskillrect[y][x]=init_quads[y][x]
                        ChangeQuadColor(LastPos,init_quads,5)
        for i in range(0,9):
                if (i + CurrentIndex >= len(quads_color_list)):
                    pygame.draw.rect(screen, BLACK, pygame.Rect(i*Quad, WIDTH + 2*Quad, i*Quad+Quad, HEIGHT))
                else:
                    QuadColor = BaseColor[quads_color_list[CurrentIndex + i]-1]
                    pygame.draw.rect(screen, QuadColor, pygame.Rect(i*Quad, WIDTH + 2*Quad, i*Quad+Quad, HEIGHT))

        if (len(WalkedPath) >= 2):
                for i in range(0,len(WalkedPath)-1):
                    start = [WalkedPath[i][0] * Quad + 0.5 * Quad, WalkedPath[i][1] * Quad + 0.5 * Quad]
                    end = [WalkedPath[i+1][0] * Quad + 0.5 * Quad, WalkedPath[i+1][1] * Quad + 0.5 * Quad]
                    pygame.draw.line(screen, LineColor, start, end, 1)
                x = WalkedPath[len(WalkedPath) - 1][0]
                y = WalkedPath[len(WalkedPath) - 1][1]
                pygame.draw.rect(screen,BLACK,pygame.Rect(x*Quad, y*Quad, Quad, Quad))
                Length = len(WalkedPath) - 1
                LengthFont = pygame.font.SysFont("",32)
                LengthText = LengthFont.render(str(Length),True,RED,BLACK)
                screen.blit(LengthText,(x*Quad,y*Quad))
                
        pygame.display.update()

if __name__ == '__main__':
    main()