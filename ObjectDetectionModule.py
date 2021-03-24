# import cv2

# img = cv2.imread("../Resources/testPh1.jpg")

# faceCascade = cv2.CascadeClassifier("../Resources/haarcascade_frontalface_default.xml")
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
# for (x,y,w,h) in faces:
#     cv2.rectangle(img,(x,y), (x+w,y+h), (255,0,255),2)

# cv2.imshow("Output",img)
# cv2.waitKey(0)

'''
Object detection Module
Viola Jhones Method

by: jiafeng 2021/3/5
'''

import cv2


def findObjects(img, objectCascade, scaleF = 1.1, minN = 4):
    
    '''
    find objects using the haarcascade file

    :param img : Image in which the objects needs to be found
    :param objectCascade : Object Cascade created with Cascade Classifier
    :param scaleF : how mach the image size is reduced at each image scale
    :param minN : how many neighbours each rectangle should have to accept as valid
    :return : image with the rectangle draw and the bounding box info
    '''
    imgObjects = img.copy()
    imgGray = cv2.cvtColor(imgObjects, cv2.COLOR_BGR2GRAY)
    objects = objectCascade.detectMultiScale(imgGray, scaleF, minN)
    objectsOut = []  #创建空列表 
    for (x,y,w,h) in objects:
        cv2.rectangle(imgObjects,(x,y), (x+w,y+h), (255,0,255),2)
        objectsOut.append([[x,y,w,h],w*h])    #append方法用在列表末尾添加新的对象

    objecctsOut = sorted(objectsOut, key = lambda x: x[1], reverse = True)
    
    return imgObjects, objects


def main():
    img = cv2.imread("../Resources/testPh1.jpg")
    faceCascade = cv2.CascadeClassifier("../Resources/haarcascade_frontalface_default.xml")
    imgObjects, objects = findObjects(img, faceCascade)
    cv2.imshow("Output",imgObjects)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()




#笔记：
'''
append()方法语法结构
list.append(obj)   

参数 -- obj
添加到列表末尾的对象

返回值
该方法务返回值，但会修改原来的列表

实例
#/usr/bin/python

alist = [1234, 'jjp', 'love']
alist.append(900)
print("更新后的列表："，alist)

更新后的列表：[1234, 'jjp', 'love', 900]


sorted()函数
对所有可迭代的对象进行排序操作
sort应用在list上的方法，sorted可以对所有可迭代的对象进行排序操作
list中的sort方法，对已经存在的列表进行操作；内建函数sorted方法返回的是一个新的 list，而不是在原来的基础上进行的操作。

语法
sorted（iterable， key=None， reverse=False）

参数
iterable -- 可迭代对象
key -- 用来比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
reverse -- 排序规则，reverse = True降序，reverse=False升序（默认）
返回重新排序的列表

实例
jiafeng@jiafeng-nano:~$ python3
Python 3.6.9 (default, Oct  8 2020, 12:12:24) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> example_list = [3,5,2,7,11,1,0]
>>> result_list = sorted(example_list, key=lambda x:x*-1)
>>> print(result_list)
[11, 7, 5, 3, 2, 1, 0]
>>> 

'''