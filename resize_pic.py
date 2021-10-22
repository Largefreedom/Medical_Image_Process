from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None


def crop_bone(img_path,save_path):
    crop_region = (1150,11895,4200,20791)
    path_list = os.listdir(img_path)

    for i in path_list:
        ori_path = os.path.join(img_path,str(i))
        img_save_path = os.path.join(save_path,str(i))
        img = Image.open(ori_path)
        img2 = img.crop(crop_region)
        img2.save(img_save_path)
        print("{} Save sucessfully!".format(img_save_path))



def crop_heart(img_path,save_path):
    crop_region = (1895,11821,4556,15052)

    path_list = os.listdir(img_path)
    for i in path_list:
        ori_path = os.path.join(img_path,str(i))
        img_save_path = os.path.join(save_path,str(i))
        img = Image.open(ori_path)
        img2 = img.crop(crop_region)
        img2.save(img_save_path)
        print("{} Save sucessfully!".format(img_save_path))


def crop_left(img_path,save_path):
    crop_region = (2020,14652,5154,16816)

    path_list = os.listdir(img_path)
    for i in path_list:
        ori_path = os.path.join(img_path,str(i))
        img_save_path = os.path.join(save_path,str(i))
        img = Image.open(ori_path)
        img2 = img.crop(crop_region)
        img2.save(img_save_path)
        print("{} Save sucessfully!".format(img_save_path))



def crop_lung(img_path,save_path):
    crop_region = (1862,12887,6850,18049)

    path_list = os.listdir(img_path)
    for i in path_list:
        ori_path = os.path.join(img_path,str(i))
        img_save_path = os.path.join(save_path,str(i))
        img = Image.open(ori_path)
        img2 = img.crop(crop_region)
        img2.save(img_save_path)
        print("{} Save sucessfully!".format(img_save_path))


def crop_img_path(img_path,save_path,crop_region):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    path_list = os.listdir(img_path)
    for i in path_list:
        ori_path = os.path.join(img_path,str(i))
        img_save_path = os.path.join(save_path,str(i))
        img = Image.open(ori_path)
        img2 = img.crop(crop_region)
        img2.save(img_save_path)
        print("{} Save sucessfully!".format(img_save_path))



# origin_path = "D:/ceshi1/Crop2/Bone_resized"
# save_path = "D:/ceshi1/Crop2/Bone_crop"
#
# crop_origin = (0,230,366,700)
# crop_img_path(origin_path,save_path,crop_origin)
#
# origin_path1 = "D:/ceshi1/Crop2/liver_resized"
# save_path1 = "D:/ceshi1/Crop2/liver_crop"
#
# crop_origin = (0,230,366,700)
# crop_img_path(origin_path1,save_path1,crop_origin)
#
#
# origin_path2 = "D:/ceshi1/Crop2/kidney_resized"
# save_path2 = "D:/ceshi1/Crop2/kidney_crop"
#
# crop_origin = (0,230,366,700)
# crop_img_path(origin_path2,save_path2,crop_origin)

ori_path = "D:/ceshi1/Crop2/224.png"
img_save_path = "D:/ceshi1/Crop2/224.png"
img = Image.open(ori_path)
img2 = img.crop((0,230,366,700))
img2.save(img_save_path)
print("{} Save sucessfully!".format(img_save_path))


# img_path = "D:/ceshi1/ceshi"
#
# bone_path = "D:/ceshi1/Crop/Bone"
# heart_path = "D:/ceshi1/Crop/Heart"
# Left_path = "D:/ceshi1/Crop/Left"
# Lung_path = "D:/ceshi1/Crop/Lung"
#
# a_path = "D:/ceshi1/Crop/009.png"
# b_path = "D:/ceshi1/Crop/016.png"
# crop_region = (1062,12887,6050,18049)
#
# img = Image.open(a_path)
# img2 = img.crop(crop_region)
# img2.save(b_path)


# Croping Bone
# crop_bone(img_path,bone_path)

#Croping Heart
# crop_heart(img_path,heart_path)

#Croping Left
# crop_left(img_path,Left_path)

#Croping Lung
# crop_lung(img_path,Lung_path)

