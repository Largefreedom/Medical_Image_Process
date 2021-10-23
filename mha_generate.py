import itk
import os
import numpy as np
from PIL import Image
from medpy.io import load,save

# writer = sitk.ImageFileWriter()
# writer.SetFileName(outputImageFileName)
# writer.Execute(image)


'''
 mha 文件生成
'''
# def generate_mha(origin_path, suffix_name,spacing):
#     len_num = len([i for i in os.listdir(origin_path) if str(i).endswith(suffix_name)])
#
#     # 确定最后索引
#     if len_num < 10:
#         end_index = '00{}'.format(len_num)
#     elif len_num < 100:
#         end_index = '0{}'.format(len_num)
#     else:
#         end_index = len_num
#     print("end num is ",end_index,len_num)
#     Imagetype = itk.Image[itk.UC, 3]
#     reader = itk.ImageSeriesReader[Imagetype].New()
#     writer = itk.ImageFileWriter[Imagetype].New()
#     writer2 = itk.ImageFileWriter[Imagetype].New()
#     nameGenerator = itk.NumericSeriesFileNames.New()
#     nameGenerator.SetSeriesFormat(str(os.path.join(origin_path, '%03d.{}'.format(suffix_name))))
#     start_index = 1
#     nameGenerator.SetStartIndex(start_index)
#     nameGenerator.SetEndIndex(2)
#     # size = reader.GetOutput().GetLargestPossibleRegion().GetSize()
#     nameGenerator.SetIncrementIndex(1)
#
#     reader.SetImageIO(itk.PNGImageIO.New())
#     reader.SetFileNames(nameGenerator.GetFileNames())
#     reader.Update()
#     # 设置Spacing
#
#     reader.GetOutput().SetSpacing(spacing)
#     reader.Update()
#
#     print("spacing is ------\n")
#     print(spacing)
#     print("start_index is ----------\n")
#     print(start_index)
#     print("end_index is --------\n")
#     print(end_index)
#
#     writer.SetFileName(os.path.join(origin_path, 'output.mha'))
#     writer.SetInput(reader.GetOutput())
#     writer.Update()
#
#     writer2.SetFileName(os.path.join(origin_path, 'output.mhd'))
#     writer2.SetInput(reader.GetOutput())
#     writer2.Update()






origin_path =  "F:\lymph_1\ly_resize_10_png"
path_list = [i for i in os.listdir(origin_path) if(str(i).endswith(".tif"))]
if(len(path_list) > 0):
    img = Image.open(os.path.join(origin_path,path_list[0]))
    height,width = img.size
    result_arr = np.zeros((width, height, len(path_list)))
    for index in range(len(path_list)):
        print("propress image slice is ",index)
        #递归计算；
        img1 = Image.open(os.path.join(origin_path, path_list[index]))
        img_arr = np.array(img1).copy()
        result_arr[:,:,index] = img_arr
    img_save = np.array(result_arr, 'float32')
    save(img_save,os.path.join(origin_path,"result.mha"))


