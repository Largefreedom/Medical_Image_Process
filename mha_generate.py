import itk
import  os






'''
 mha 文件生成
'''
def generate_mha(origin_path, suffix_name,spacing):
    len_num = len([i for i in os.listdir(origin_path) if str(i).endswith(suffix_name)])
    # 确定最后索引
    if len_num < 10:
        end_index = '00{}'.format(len_num)
    elif len_num < 100:
        end_index = '0{}'.format(len_num)
    else:
        end_index = len_num
    print(end_index)
    Imagetype = itk.Image[itk.UC, 3]
    reader = itk.ImageSeriesReader[Imagetype].New()
    writer = itk.ImageFileWriter[Imagetype].New()
    writer2 = itk.ImageFileWriter[Imagetype].New()
    nameGenerator = itk.NumericSeriesFileNames.New()
    nameGenerator.SetSeriesFormat(str(os.path.join(origin_path, '%03d.{}'.format(suffix_name))))
    start_index = 1
    nameGenerator.SetStartIndex(start_index)
    nameGenerator.SetEndIndex(int(end_index))
    nameGenerator.SetIncrementIndex(1)

    reader.SetImageIO(itk.PNGImageIO.New())
    reader.SetFileNames(nameGenerator.GetFileNames())
    reader.Update()
    # 设置Spacing

    reader.GetOutput().SetSpacing(spacing)
    reader.Update()

    print("spacing is ------\n")
    print(spacing)
    print("start_index is ----------\n")
    print(start_index)
    print("end_index is --------\n")
    print(end_index)

    writer.SetFileName(os.path.join(origin_path, 'output.mha'))
    writer.SetInput(reader.GetOutput())
    writer.Update()

    writer2.SetFileName(os.path.join(origin_path, 'output.mhd'))
    writer2.SetInput(reader.GetOutput())
    writer2.Update()

origin_path ="D:/ceshi1/Crop2/Regis_2/Bone_regised"
suffix_name = "png"
spacing = [0.1,0.1,0.05]
generate_mha(origin_path,suffix_name,spacing)