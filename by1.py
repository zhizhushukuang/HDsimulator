from ast import If
#from curses import KEY_BACKSPACE
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
#line_break=True

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
font_size = 36
bechangedcolorforskillq1=2
bechangedcolorforskillq2=9
bechangedcolorforskillw1=3
bechangedcolorforskillw2=2
bechangedcolorto=4#1是蓝色，2是红色，3是黄色，4是绿色
LastPos = []
rexcolor=[]
reycolor=[]
BaseColor = [BLUE,RED,YELLOW,GREEN,RAINBOW,BLACK]
PlayerColor = pygame.Color(114,51,4)
MonsterColor = pygame.Color(255,255,255)
LineColor = pygame.Color(128,0,128)
UsedColorQueue = []
CurrentIndex = 0
rerskillrect=[[7]*9 for i in range(9)]
new_collected_color_order=[]
# 读取配置文件

def ChangeQuadColor(Position, SquareColor, NewColor):
    x = int(Position[0] / Quad)
    y = int(Position[1] / Quad)
    SquareColor[y][x] = NewColor

def write_to_file(colors_list):
    file_path = 'new_collected_color_order.txt'
    with open(file_path, 'a') as file:
        colors_str = ','.join(map(str, colors_list))
        if  colors_list:
            file.write(colors_str + '\n')   

def GoOneStep(screen, ColorList, Position, SquareColor):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    
    PathLength = len(WalkedPath)
    x = int(Position[0] / Quad)
    y = int(Position[1] / Quad)
    WalkedPath.append([x,y])
    pos = WalkedPath[PathLength-1]
    x = pos[0]
    y = pos[1]
    UsedColorQueue.append(SquareColor[y][x])
    if (CurrentIndex < len(ColorList)) and (ColorList[CurrentIndex]!=6):
        QuadColor = BaseColor[ColorList[CurrentIndex]]
        SquareColor[y][x] = ColorList[CurrentIndex]
    else:
        QuadColor=BaseColor[5]
        SquareColor[y][x] = 6
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
    QuadColor = UsedColorQueue.pop()
    WalkedPath.pop()
    LastPos = WalkedPath[len(WalkedPath) - 1]
    x = LastPos[0]
    y = LastPos[1]
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
    if(math.atan2(x,y)<=0):
        arc=math.atan2(x,y)+2*math.pi
    else:
        arc=math.atan2(x,y)
    return arc

def youxianjipaixu(list1, player_position):
    sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (player_position[0],player_position[1])), -fixmathatan2(player_position[0]-point[0],player_position[1]-point[1])))
    return sorted_points

# def skill_w(screen, position, init_quads,changenumber):
#     global CurrentIndex
#     global UsedColorQueue
#     global WalkedPath
#     global reinit_quads
#     global bechangedcolorforskillq1
#     global bechangedcolorforskillq2
#     global READYTOCHANGEcolor
#     reinit_quads=init_quads
#     list1=[]
#     player_position=position
#     x=player_position[0]
#     y=player_position[1]
#     for i in range(0,9):
#          for j in range(0,9):
#             if(init_quads[i][j]==bechangedcolorforskillq1) or (init_quads[i][j]==bechangedcolorforskillq2):
#                 list1.append([j,i])
             
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(point[1]-player_position[1],point[0]-player_position[0])))    
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(point[0]-player_position[0],point[1]-player_position[1])))    
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(player_position[1]-point[1],player_position[0]-point[0])))    
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), fixmathatan2(player_position[0]-point[0],player_position[1]-point[1]))) 
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(point[1]-player_position[1],point[0]-player_position[0])))    
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(point[0]-player_position[0],point[1]-player_position[1])))    
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(player_position[1]-point[1],player_position[0]-point[0])))    
#     #sorted_points = sorted(list1, key=lambda point: (distance_from_given_point(point, (x,y)), -fixmathatan2(player_position[0]-point[0],player_position[1]-point[1])))         
#     sorted_points=youxianjipaixu(list1, player_position)
#     k=0          
#     for i in range(0,min(changenumber,len(list1))):
#         obj1=sorted_points[i+k]
#         x1=obj1[0]
#         y1=obj1[1]
#         if(x==x1 and y==y1):
#             k=1
#             obj1=sorted_points[i+k]
#             x1=obj1[0]
#             y1=obj1[1]
        
#         init_quads[y1][x1]=READYTOCHANGEcolor
#     print(sorted_points)

# def REskill_w(screen, init_quads):
#     global bechangedcolorforskillq1
#     global READYTOCHANGEcolor
#     for i in range(0,9):
#          for j in range(0,9):
#             if(init_quads[i][j]==READYTOCHANGEcolor):
#                 init_quads[i][j]=bechangedcolorforskillq1

# def ENskill_w(screen, init_quads):
#     global bechangedcolorto
#     global READYTOCHANGEcolor
    
#     for i in range(0,9):
#          for j in range(0,9):
#             if(init_quads[i][j]==READYTOCHANGEcolor):
#                 init_quads[i][j]=bechangedcolorto
    
def skill_w(screen, position, init_quads,changenumber,bechangedcolor1,bechangedcolor2):
    global CurrentIndex
    global UsedColorQueue
    global WalkedPath
    global reinit_quads
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

def REskill_w(screen, init_quads,bechangedcolor1,bechangedcolor2):
    global READYTOCHANGEcolor
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

def skill_e(screen, position, init_quads,x_judge,y_judge):
    global reinit_quads
    global READYTOCHANGEcolor
    global rexcolor
    global reycolor
    reinit_quads=init_quads
    player_position=position
    y=player_position[0]
    x=player_position[1]
    for i in range(0,9):
        if(i!=y and init_quads[x][i]!=6 and x_judge):
            rexcolor.append(init_quads[x][i])
            init_quads[x][i]=READYTOCHANGEcolor   
    for i in range(0,9):
        if(i!=x and init_quads[i][y]!=6 and y_judge):
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
    Newconfig["PlayerPosition"] = [x,y]
    Newconfig["MonsterPosition"] = Config["MonsterPosition"]
    Newconfig["new_collected_color_order"]=new_collected_color_order
    Newconfig["bechangedcolorforskillq1"]=[bechangedcolorforskillq1]
    Newconfig["bechangedcolorforskillq2"]=[bechangedcolorforskillq2]
    Newconfig["bechangedcolorforskillw1"]=[bechangedcolorforskillw1]
    Newconfig["bechangedcolorforskillw2"]=[bechangedcolorforskillw2]
    Newconfig["bechangedcolorto"]=bechangedcolorto
    Newconfig["QuadsColorList"] = NewColorList

    f = open(NewconfigPathTmp,'w+')
    json.dump(Newconfig, f, indent = 0, separators = (",",":"))
    f.close()
    with open(NewconfigPathTmp,"r") as fin:
        with open(NewconfigPath, "w+") as fout:
            for line in fin:
                line = line.rstrip()  # 去掉行末的空格和换行符
                fout.write(line + "\n")  # 在每一行的末尾添加换行符"\n"
    #             if not ("]," in line):
    #                 fout.write(line.replace("\n",""))
    #             else:
    #                 fout.write(line)
    # os.remove(NewconfigPathTmp)

def main():
    global CurrentIndex
    global bechangedcolorto
    global bechangedcolorforskillq1
    global bechangedcolorforskillq2
    global bechangedcolorforskillw1
    global bechangedcolorforskillw2
    temp=[]
    config_path = "config.json"
    global new_collected_color_order
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            init_quads = config["InitQuads"]
            reinit_quads=[]
            quads_color_list = config["QuadsColorList"]
            player_position =config["PlayerPosition"]
            q1=config["bechangedcolorforskillq1"]
            bechangedcolorforskillq1=q1[0]
            q2=config["bechangedcolorforskillq2"]
            bechangedcolorforskillq2=q2[0]
            w1=config["bechangedcolorforskillw1"]
            bechangedcolorforskillw1=w1[0]
            w2=config["bechangedcolorforskillw2"]
            bechangedcolorforskillw2=w2[0]
            colorto=config["bechangedcolorto"]
            bechangedcolorto=colorto[0]
            WalkedPath.append(player_position)
    except FileNotFoundError:
        print("无法加载盘面。请确保有名为 'board.json' 的正确格式的文件。")
        return

    # 初始化Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect the Dots")
    global font_size
    font = pygame.font.Font(None, font_size)
    # 游戏状态
    editing_mode = False
    qskill_mode=False
    wskill_mode=False
    eskill_mode=False
    rskill_mode=False
    fskill_mode=False
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
        char_width = font.size("5")[0]
        max_chars_per_line = WIDTH // char_width
        text_lines = '\n'.join(str(item) for item in new_collected_color_order)
        # 假设new_collected_color_order是过长的列表
        text_lines = []
        current_line = ""
        
        # global line_break
        text_lines = [f"edit: {editing_mode},skill: q: {qskill_mode}, w: {wskill_mode}, e: {eskill_mode}",f"r:{rskill_mode},f:{fskill_mode},collectcolor: "]
        for item in new_collected_color_order:
            
            item_str = str(item)
            if len(current_line) + len(item_str) <= max_chars_per_line:
                current_line += item_str
            else:
                text_lines.append(current_line)
                current_line = item_str
                # line_break=not line_break
                # if(line_break):
                #     font_size -= 2
                #     font = pygame.font.SysFont(None, font_size)
        if current_line:
            text_lines.append(current_line)
        # max_lines=4
        # text_lines_list = text_lines.split('\n')
        # if len(text_lines_list) > max_lines:
        #     # 如果文本行数超过四行，则缩小字号
        #     
        #     
        #     max_lines+=1
        #     text_surfaces.clear()
        # else:
        #     pass

        text_surfaces = [font.render(line, True, (255, 255, 255)) for line in text_lines]  # 文本内容、是否抗锯齿、字体颜色
        text_height = sum(surface.get_height() for surface in text_surfaces)
        text_y = (20.5*Quad - text_height) // 2
        for surface in text_surfaces:
            text_rect = surface.get_rect(center=(4.5*Quad, text_y))
            screen.blit(surface, text_rect)
            text_y += surface.get_height()
        # text_rect = text_surface.get_rect()
        # text_rect.center = (4*Quad, 10*Quad)
        # screen.blit(text_surface,text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                x=WalkedPath[len(WalkedPath)-1][0]
                y=WalkedPath[len(WalkedPath)-1][1]
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
                elif event.key == K_f:
                    fskill_mode=not fskill_mode
                    print("fskill_mode:",fskill_mode)
                elif event.key == K_t:
                    if CurrentIndex < len(quads_color_list):
                        CurrentIndex=CurrentIndex+1
                    elif (CurrentIndex > len(quads_color_list))&(editing_mode):
                        new_collected_color_order.append(6)
                        quads_color_list.append(6)
                        print(new_collected_color_order)
                elif event.key == 32:
                    if(CurrentIndex>0)&(CurrentIndex < len(quads_color_list)):
                        CurrentIndex=CurrentIndex-1
                    elif CurrentIndex > len(quads_color_list):
                        new_collected_color_order.pop()
                        quads_color_list.pop()
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
                        if event.key == K_BACKSPACE:
                            if(len(new_collected_color_order)>0):
                                quads_color_list.pop()
                                new_collected_color_order.pop()
                                print(new_collected_color_order)
                        pygame.display.update()
                elif(qskill_mode == True):
                        if event.key == K_1:
                            skill_w(screen,WalkedPath[len(WalkedPath)-1],init_quads,4,bechangedcolorforskillq1,bechangedcolorforskillq2)
                        if event.key == K_2:
                            skill_w(screen,WalkedPath[len(WalkedPath)-1],init_quads,5,bechangedcolorforskillq1,bechangedcolorforskillq2)
                        if event.key == K_3:
                            skill_w(screen,WalkedPath[len(WalkedPath)-1],init_quads,6,bechangedcolorforskillq1,bechangedcolorforskillq2)
                        if event.key == K_4:
                            REskill_w(screen,init_quads,bechangedcolorforskillq1,bechangedcolorforskillq2)
                            qskill_mode=not qskill_mode
                            print("REskill_w")   
                        if event.key == K_5:
                            ENskill_w(screen,init_quads)
                            qskill_mode=not qskill_mode
                        pygame.display.update()
                elif(wskill_mode == True):
                        if event.key == K_1:
                            skill_w(screen,WalkedPath[len(WalkedPath)-1],init_quads,4,bechangedcolorforskillw1,bechangedcolorforskillw2)
                        if event.key == K_2:
                            skill_w(screen,WalkedPath[len(WalkedPath)-1],init_quads,5,bechangedcolorforskillw1,bechangedcolorforskillw2)
                        if event.key == K_3:
                            skill_w(screen,WalkedPath[len(WalkedPath)-1],init_quads,6,bechangedcolorforskillw1,bechangedcolorforskillw2)
                        if event.key == K_4:
                            REskill_w(screen,init_quads,bechangedcolorforskillw1,bechangedcolorforskillw2)
                            wskill_mode=not wskill_mode
                            print("REskill_w")   
                        if event.key == K_5:
                            ENskill_w(screen,init_quads)
                            wskill_mode=not wskill_mode
                            print("REskill_w") 
                        
                elif(eskill_mode == True):
                        if event.key == K_1:
                            skill_e(screen,WalkedPath[len(WalkedPath)-1],init_quads,1,1)
                        if event.key == K_2:
                            skill_e(screen,WalkedPath[len(WalkedPath)-1],init_quads,0,1)
                        if event.key == K_3:
                            skill_e(screen,WalkedPath[len(WalkedPath)-1],init_quads,1,0)
                        if event.key == K_4:
                            REskill_e(screen,WalkedPath[len(WalkedPath)-1],init_quads)
                            eskill_mode=not eskill_mode
                            print("REskill_e")   
                        if event.key == K_5:
                            ENskill_e(screen,init_quads)
                            eskill_mode=not eskill_mode
                            print("REskill_e") 
                        
                
                
            elif event.type == MOUSEBUTTONDOWN:
                LastPos = event.pos
                x = int(LastPos[0] / Quad)
                y = int(LastPos[1] / Quad)
                if event.button == 1:
                    print(event.pos)
                    if ((event.pos[0] < WIDTH) & (event.pos[1] < WIDTH) & (not editing_mode) & (not qskill_mode)& (not wskill_mode)& (not eskill_mode)& (not rskill_mode)&(not fskill_mode)):
                            
                            GoOneStep(screen,quads_color_list,event.pos,init_quads)
                    elif(rskill_mode):
                        rerskillrect[y][x]=init_quads[y][x]
                        ChangeQuadColor(LastPos,init_quads,bechangedcolorto)
                    elif(fskill_mode):
                        try:
                            MonsterPosition.remove([x,y])
                        except:
                            MonsterPosition.append([x,y])
                    # elif ((event.pos[1] > 9*Quad) & (event.pos[1] < 11*Quad)):
                    #         OutputNewconfig(config, quads_color_list, init_quads)
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
                    elif(editing_mode):#&(CurrentIndex>len(quads_color_list))
                        quads_color_list.append(init_quads[y][x])
                        new_collected_color_order.append(init_quads[y][x])
                        print(new_collected_color_order)
        for i in range(0,9):
                if(i + CurrentIndex >= len(quads_color_list)):
                    pygame.draw.rect(screen, BLACK, pygame.Rect(i*Quad, WIDTH + 2*Quad, i*Quad+Quad, HEIGHT))
                elif  CurrentIndex >= len(quads_color_list):
                    QuadColor = BaseColor[new_collected_color_order[CurrentIndex + i-len(quads_color_list)-1]-1]
                    pygame.draw.rect(screen, QuadColor, pygame.Rect(i*Quad, WIDTH + 2*Quad, i*Quad+Quad, HEIGHT))
                
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
    pygame.quit()
    write_to_file(new_collected_color_order)

if __name__ == '__main__':
    main()