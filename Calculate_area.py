import cv2
import  numpy as np
import matplotlib.pyplot as plt

img_path  = "D:/ceshi1/001.png"



img = cv2.imread(img_path)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_gray,cv2.COLOR_RGB2GRAY)
cv2.imwrite("D:/contours_3.png",img_gray)
img_gray[img_gray>=254] = 0




contours,hierarchy =  cv2.findContours(img_gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_gray,contours,-1,(255,0,0),10)
plt.imshow(img_gray)
plt.show()

area = 0
for i in range(len(contours)):
    print(i)
    area += cv2.contourArea(contours[i])

print(area)

cv2.imwrite("D:/contours_1.png",img_gray)
