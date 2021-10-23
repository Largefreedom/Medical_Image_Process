from PIL import Image
import os
Image.MAX_IMAGE_PIXELS = None


'''
    缩放图片
'''
def resize_image(ori_path,save_path,scale_fator):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path_list = os.listdir(ori_path)
    for i in path_list:
        img_path = os.path.join(ori_path,str(i))
        save_img_path = os.path.join(save_path,str(i))
        img = Image.open(img_path)
        w,h = img.size
        out = img.resize((int(w/scale_fator),int(h/scale_fator)),Image.ANTIALIAS)
        out.save(save_img_path)
        print("{} saving sucessfully!".format(save_img_path))


# bone_path = "D:/ceshi1/Crop2/Bone"
# bone_save = "D:/ceshi1/Crop2/Bone_resized"
# resize_image(bone_path,bone_save,3)
#
# liver_path = "D:/ceshi1/Crop2/lung"
# liver_save = "D:/ceshi1/Crop2/lung_resized"
# resize_image(liver_path,liver_save,3)
#
#
lung_path = "F:\lymph_1\ly_re"
lung_save = "F:\lymph_1\ly_resize_10"
resize_image(lung_path,lung_save,10)



# scale_fator = 3
#
# img_path = "D:/ceshi1/Crop2/224.png"
# save_img_path = "D:/ceshi1/Crop2/224.png"
#
# img = Image.open(img_path)
# w,h = img.size
# out = img.resize((int(w/scale_fator),int(h/scale_fator)),Image.ANTIALIAS)
# out.save(save_img_path)
# print("{} saving sucessfully!".format(save_img_path))







