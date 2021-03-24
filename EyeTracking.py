import cv2
import ObjectDetectionModule as odm 
import SerialModule as sm 
import numpy as np 
import time

frameWidth = 640
frameHeight = 480

filp = 2

cap = cv2.VideoCapture('/dev/video0')
#window_handle = cv2.namedWindow("USB Camera", cv2.WINDOW_AUTOSIZE)

#cap.set(3,640)
#cap.set(4,320)
ser = sm.initConnection('/dev/ttyUSB0',9600)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

perrorLR, perrorUD = 0, 0
#查找人脸，并绘制方块及中心点，及x y线
def findCenter(imgObjects, objects):
    cx,cy = -1, -1
    if len(objects)!=0:
        x,y,w,h = objects[0]
        cx = x + w//2
        cy = y + h//2
        cv2.circle(imgObjects, (cx,cy), 2, (0,255,0),cv2.FILLED)
        ih,iw,ic = imgObjects.shape
        cv2.line(imgObjects,(iw//2,cy),(cx,cy),(0,255,0),1)
        cv2.line(imgObjects,(cx,ih//2),(cx,cy),(0,255,0),1)
    return cx,cy,imgObjects

#返回人脸中心点到，图像中间的距离
def trackObject(cx, cy, w, h):
    
    global perrorLR,perrorUD

    kLR = [0.5, 0.5]
    kUD = [0.5, 0.5]

    if cx!=-1:
        errorLR = w//2 - cx
        posX = kLR[0] * errorLR + kLR[1] * (errorLR-perrorLR)
        posX = np.interp(posX,[-w//2,w//2],[20,160])
        perrorLR = errorLR

        errorUD = h//2 - cy
        posY = kUD[0] * errorUD + kUD[1] * (errorUD-perrorUD)
        posY = np.interp(posY,[-w//2,w//2],[20,160])
        perrorUD = errorUD
        

        sm.sendData(ser, [posX,posY], 3)

while True:
    success, img = cap.read()
    #调整图像大小，先缩小，提高检测速度，之后在进行放大
    img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    imgObjects,objects = odm.findObjects(img,faceCascade,1.08,10)
    cx, cy, imgObjects = findCenter(imgObjects,objects)

    h,w,c = imgObjects.shape
    cv2.line(imgObjects,(w//2,0),(w//2,h),(255,0,255),1)
    cv2.line(imgObjects,(0,h//2),(w,h//2),(255,0,255),1)

    trackObject(cx, cy, w, h)

    img = cv2.resize(imgObjects, (0,0), None, 3, 3)

    cv2.imshow("Image",img)
    #当按下q键，退出循环，并发送复位给arduino uno 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sm.sendData(ser,[90, 90], 3)
        break



#笔记
'''
vs快捷键
ctrl + home/end 跳转文件头/尾
ctrl + k ctrl [ / ] 折叠/展开区域代码 
ctrl + / 行注释

F12 跳转到定义处
atl + F12 代码片段显示定义


匿名函数
不再使用def语句这样的标准的形式定义一个函数。
使用lambda来创建匿名函数

lambda只是一个表达式，函数体比def简单

语法
lambda函数语法
lambda [arg1[,arg2,......argn]]:expression

jiafeng@jiafeng-nano:~/pyTest/EyeTracking_Project$ python3
Python 3.6.9 (default, Oct  8 2020, 12:12:24) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> sum = lambda arg1,arg2: arg1+arg2
>>> print("sum = ",sum(20,30))
sum =  50
>>> 

'''