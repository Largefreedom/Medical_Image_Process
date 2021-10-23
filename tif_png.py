import cv2
import numpy as np
import os


path = "F:/lymph_1/ly_resize_10_png"


file_path_list = [i for i in os.listdir(path) if str(i).endswith(".tif")]

for i in file_path_list:
    tif_path = os.path.join(path,str(i).replace(".tif",".png"))
    tif_pic = cv2.imdecode(np.fromfile(os.path.join(path,i), dtype=np.uint8), -1)
    cv2.imwrite(tif_path, tif_pic)
    print("save file successfullty ---",tif_path)
# gray_image = cv2.cvtColor(tif_pic, cv2.COLOR_BGR2GRAY)

# save_path = path.replace(".tif",".png")
# cv2.imwrite(save_path,tif_pic)
# print("gray_image is ",tif_pic)