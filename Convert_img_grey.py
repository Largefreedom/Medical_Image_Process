from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None


def convert_gray(origin_path,save_path):
    image = Image.open(origin_path)
    image1 = image.convert('L')
    image1.save(save_path)
    print("Convert {} Sucessfully ".format(save_path))





def change_gray(origin_path,save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for i in os.listdir(origin_path):
        open_path1 = os.path.join(origin_path,str(i))
        image = Image.open(open_path1)
        image1 = image.convert('L')
        image1.save(os.path.join(save_path,str(i)))
        print("Convert {} Sucessfully ".format(save_path) + i)


'''
    图片转化为灰度图
'''
origin_path = "D:/ceshi1/Data_10_31/linba_registrated/"
save_path1 = "D:/ceshi1/Data_10_31/linba_gray/"
change_gray(origin_path,save_path1)