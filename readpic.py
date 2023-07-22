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
#PicPath = os.getcwd() + "\IMGNEXT.png"
IMGPATH=os.getcwd() + "\IMG.png"
UsedColorQueue = []
WalkedPath = []
# 游戏窗口大小
Quad=60
WIDTH = 9 * Quad
HEIGHT = 12 * Quad
# 定义全局变量记录当前图像索引
current_img_index = 0

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

import cv2
import json
import os
import numpy as np
from math import pi

def evaluate_color_around_pixel(image, x, y, window_size=5, max_threshold=255*0.8):
    """
    计算某个像素点周围区域的颜色评价值，排除RGB值高于阈值的像素点
    参数：
    image: 输入图像
    x, y: 像素点的坐标
    window_size: 窗口大小，即在(x, y)周围取的区域大小
    max_threshold: RGB值的最大阈值，高于该值的像素点将被忽略
    返回：
    color_value: 像素点周围区域的颜色评价值，可以是颜色的平均值或其他统计量
    """
    h, w, _ = image.shape
    half_window = window_size // 2

    # 确保窗口不超出图像边界
    x_start = max(x - half_window, 0)
    x_end = min(x + half_window, w - 1)
    y_start = max(y - half_window, 0)
    y_end = min(y + half_window, h - 1)

    # 提取像素点周围区域的颜色值
    region_colors = image[y_start:y_end+1, x_start:x_end+1]

    # 排除RGB值高于阈值的像素点
    region_colors = region_colors[np.all(region_colors <= max_threshold, axis=-1)]

    # 如果周围没有符合条件的像素点，则返回None
    if len(region_colors) == 0:
        return None

    # 计算颜色评价值，这里简单地使用颜色的平均值作为评价值
    color_value = np.mean(region_colors, axis=(0,))

    return color_value

def read_pic_set(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            init_point_ratio = data["init_point_ratio"]
            step_ratio = data["step_ratio"]
            xfixset=data["xfixset"]
            yfixset=data["yfixset"]
            fixlinestartpoint=data["fixlinestartpoint"]
            picturename=data["picturename"]
            pictureformat=data["picture format"]
    except:
            init_point_ratio = [0.415, 0.09]
            step_ratio = 0.05
            xfixset=1
            yfixset=1
            fixlinestartpoint=1
            picturename="IMG"
            pictureformat="png"
    return init_point_ratio, step_ratio,yfixset,xfixset,fixlinestartpoint, picturename, pictureformat

def ReadInPic():
    global current_img_index
    init_point_ratio, step_ratio,yfixset,xfixset,fixlinestartpoint, picturename, pictureformat = read_pic_set("readpicset.json")
    # 拼接当前图像文件名
    img_path = f"{picturename}{current_img_index}.{pictureformat}"
    img = cv2.imread(img_path)
    # 从指定路径（PicPath）读取图像并存储在img变量中
    #img = cv2.imread(PicPath)
    
    # 尝试从另一个指定路径（IMGPATH）读取图像，并将其缩放为原尺寸的一半后显示在屏幕上
    # 如果在读取第二个图像时出现异常（错误），则从函数中返回
    try:
        img2 = cv2.imread(IMGPATH)
        img2 = cv2.resize(img2, None, fx=0.5, fy=0.5)
        cv2.imshow("output2", img2)
    except:
       pass
    
    # 检查图像"img"是否具有正确的形状（非空）
    # 如果在访问图像形状时出现异常（错误），则从函数中返回
    try:
        img.shape
    except:
        return
    
    # 获取图像"img"的高度（HEIGHT）和宽度（WIDTH）
    HEIGHT, WIDTH = img.shape[:2]

    
    # 定义初始点"initpoint"，从这个点开始处理图像
    initpoint = (int(WIDTH * init_point_ratio[0]), int(HEIGHT * init_point_ratio[1]))
    # 计算步长"deltax"，用于沿x轴移动的大小，基于图像宽度的5%
    deltax = WIDTH * step_ratio
    
    
    
    # 定义一个包含不同角度（以度为单位）的列表"k"
    k = [30, 30.75, 31.5, 32.25, 33, 33.75, 34.5, 35.25, 36]
    
    # 计算tan(pi/6)（30度）的值，并存储在"k2"变量中
    k2 = np.math.tan(pi * 5 / 6)
    

    
    # 初始化一个空列表"SquareColor"，用于存储格子的颜色信息
    SquareColor = []
    
    # 循环遍历9x9格子中的每一行
    for i in range(0, 9):
        # 计算每一行的起始点"linestartpoint"
        linestartpoint = (int(initpoint[0] - deltax * i*fixlinestartpoint), int(initpoint[1] - deltax * i * k2*fixlinestartpoint))
        
        # 计算角度"k[i]-2"的tan值，并存储在"k1"变量中
        k1 = np.math.tan((k[i]) / 180 * pi)
        
        # 计算直线的截距"b"，基于起始点和"k1"
        b = linestartpoint[1] - linestartpoint[0] * k1
        
        # 初始化一个空列表"LineColor"，用于存储每一行格子的颜色信息
        LineColor = []
        
        # 循环遍历每一行格子中的每一列
        for j in range(0, 9):
            # 计算每个格子的x和y坐标，基于起始点和步长"deltax"//现在为step_ratio
            pointx = int(linestartpoint[0] + j * deltax*xfixset)
            pointy = int(linestartpoint[1] + j * deltax * k1*yfixset)
            
            # 确保计算得到的坐标不超过图像的尺寸范围
            if pointx > WIDTH or pointy > HEIGHT:
                LineColor.append(6)
            else:
            # 创建一个元组"point"，用于存储当前格子的(x, y)坐标
                point = (pointx, pointy)
            
            # 获取当前格子在图像中的颜色
                #color = img[pointy, pointx]
                color = evaluate_color_around_pixel(img, pointx, pointy, 5 , 255*0.95)
            # 检查格子的颜色，以确定格子类型，并将对应的值添加到"LineColor"列表中
                if(color is not None):
                    isBlue = (color[0] > (color[1] * 1.3)) & (color[0] > (color[2] * 1.3))
                    isGreen = (color[1] > (color[0] * 1.3)) & (color[1] > (color[2] * 1.3))
                    isRed = (color[2] > (color[0] * 1.3)) & (color[2] > (color[1] * 1.4))
                    isYellow = (color[2] > (color[0] * 1.3)) & (color[1] > (color[0] * 1.3))
            
            # 根据颜色类型设置当前格子的颜色，并将对应的值添加到"LineColor"列表中
                PointColor = (0, 0, 0)
                if isBlue:
                    PointColor = (255, 0, 0)
                    LineColor.append(1)
                elif isRed:
                    PointColor = (0, 0, 255)
                    LineColor.append(2)
                elif isGreen:
                    PointColor = (0, 255, 0)
                    LineColor.append(4)
                elif isYellow:
                    PointColor = (0, 255, 255)
                    LineColor.append(3)
                else:
                    LineColor.append(6)
                
                # 在当前格子的位置绘制一个小圆圈，使用确定的颜色进行可视化
                cv2.circle(img, point, 2, PointColor, 4)
        
        # 将当前行格子的颜色信息添加到"SquareColor"列表中
        SquareColor.append(LineColor)
    
    # 读取"config.json"文件的内容，并将其存储在变量"Config"中
    Config = None
    with open(ConfigPath, 'r') as f:
        Config = json.load(f)
    
    # 使用格子的颜色信息更新"Config"中的"InitQuads"属性
    Config["InitQuads"] = SquareColor
    
    # 创建临时文件路径和最终文件路径，用于存储更新后的配置
    NewConfigPathTmp = os.getcwd() + "\\NewConfigTmp.txt"
    NewConfigPath = os.getcwd() + "\picconfig.json"
    
    # 将更新后的配置以JSON格式写入临时文件
    f = open(NewConfigPathTmp, 'w+')
    json.dump(Config, f, indent=0, separators=(",", ":"))
    f.close()
    
    # 将临时文件的内容复制到最终文件中，并进行适当的格式化（删除换行符）
    with open(NewConfigPathTmp, "r") as fin:
        with open(NewConfigPath, "w+") as fout:
            for line in fin:
                if not (",]" in line):
                    fout.write(line.replace("\n", ""))
                else:
                    fout.write(line)
    
    # 删除临时文件
    os.remove(NewConfigPathTmp)
    
    # 将图像"img"缩放为原尺寸的一半，并使用OpenCV显示在屏幕上
    img.resize()
    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    # 在initpoint位置绘制一个圆圈来高亮显示
    scaled_initpoint = (int(initpoint[0] * 0.5), int(initpoint[1] * 0.5))
    cv2.circle(img, scaled_initpoint, 15, (255, 255, 255), -1)
    cv2.imshow("output", img)

    # 定义一个函数用于切换到下一个图像
def switch_to_next_img():
    global current_img_index
    current_img_index += 1

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

def configread():
    Config = None
    with open(ConfigPath, 'r') as f:
        NewColorListjson = json.load(f)
    SquareColor = NewColorListjson["InitQuads"] 
    return NewColorListjson,SquareColor

def main():
    print(cv2.__file__)

    ReadInPic()

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Alchemy star sim')

    NewColorListjson,SquareColor=configread()
    # Config = None
    # with open(ConfigPath, 'r') as f:
    #     NewColorListjson = json.load(f)
    # SquareColor = NewColorListjson["InitQuads"]
    #print(Config)
    editing_mode = False
    
    
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
                elif event.key == 13:  # 按下回车键
                    switch_to_next_img()
                    ReadInPic()
                    NewColorListjson,SquareColor=configread()
                    WalkedPath.clear()
                    #CurrentIndex=CurrentIndex+1
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