from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import os
import cv2
import shutil
import numpy as np
from PIL import Image

import threading


Image.MAX_IMAGE_PIXELS = None
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)




origin_path = "F:/2021_10_18/"
save_path = "F:/Linba_Pic/PNG_Dir/"


#  the file not exit, create new path
if not os.path.exists(save_path):
    os.makedirs(save_path)
path_list = [ i for i in os.listdir(origin_path)]
print(path_list)
#  tif path tif 路径地址，number_path  编号地址;;;
tif_path = []
number_path = []

for i in path_list:
    if str(i).endswith('.tif'):
        tif_path.append(os.path.join(origin_path,str(i)))
        number_path.append(os.path.join(save_path,str(i).split('_')[0]+'.png'))


max_width,max_height = 0,0

for index,j in enumerate(tif_path):
    tif_pic = cv2.imdecode(np.fromfile(str(j),dtype = np.uint8),-1)
    gray_image = cv2.cvtColor(tif_pic,cv2.COLOR_BGR2GRAY)
    if max_width < gray_image.shape[1]:
        max_width = gray_image.shape[1]

    if max_height < gray_image.shape[0]:
        max_height = gray_image.shape[0]

    save_path_1 = number_path[index]
    cv2.imwrite(save_path_1,gray_image)

    print(f'{save_path_1} save sucessfully !')


for i in os.listdir(save_path):
    new_image = Image.new('L', (max_width, max_height), (255))  # 创建一张图片，以白色为底；
    init_img = Image.open(os.path.join(save_path,str(i)))  # 打开初始化照片
    new_image.paste(init_img,
                    (int((max_width - init_img.size[0]) / 2), int((max_height - init_img.size[1]) / 2)))

    new_image.save(os.path.join(save_path,str(i)))
