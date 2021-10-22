from PIL import Image
import os
import cv2
import numpy as np


Image.MAX_IMAGE_PIXELS = None


path = "D:/ceshi1/001.tif"

src = cv2.imread(path)
src2 = cv2.imread("D:/ceshi1/001.png")


print(src[1000][3000])
print(src2[1000][3000])
print(src.shape)



#
# def crop_heart(img_path,save_path):
#     #Build path
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     crop_region = (300,247,2942,1887)
#     path_list = os.listdir(img_path)
#     for i in path_list:
#         ori_path = os.path.join(img_path,str(i))
#         img_save_path = os.path.join(save_path,str(i))
#         img = Image.open(ori_path)
#         img2 = img.crop(crop_region)
#         img2.save(img_save_path)
#         print("{} Save sucessfully!".format(img_save_path))
#
#
# heart_path = "D:/ceshi1/Crop/Left"
# crop_heart_path = "D:/ceshi1/Crop/Left_croped"
#
#
# crop_heart(heart_path,crop_heart_path)
