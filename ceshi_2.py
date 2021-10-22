import itk
import  os
import math


def regist_zompile(left_fix_file, left_mov_file, scale_fix_file, scale_mov_file, out_file):
    print('开始进行配准')
    print(left_fix_file, left_mov_file, scale_fix_file, scale_mov_file, out_file)
    ShrinkImageType = itk.Image[itk.UC, 2]
    ShringImageReaderType = itk.ImageFileReader[ShrinkImageType]

    shrinkImageReader = ShringImageReaderType.New()
    shrinkImageReader.SetFileName(left_fix_file)

    # 缩小更改图片的比例；
    shrinkImageReader2 = ShringImageReaderType.New()
    shrinkImageReader2.SetFileName(left_mov_file)

    ShrinkImageFilterType = itk.ShrinkImageFilter[ShrinkImageType, ShrinkImageType]
    shrinkFilter = ShrinkImageFilterType.New()

    # 比例进行缩小
    shrinkFilter.SetInput(shrinkImageReader.GetOutput())
    shrinkFilter.SetShrinkFactor(0, 10)
    shrinkFilter.SetShrinkFactor(1, 10)
    shrinkFilter.Update()

    # mov进行比例缩小
    shrinkFilter2 = ShrinkImageFilterType.New()
    shrinkFilter2.SetInput(shrinkImageReader2.GetOutput())
    shrinkFilter2.SetShrinkFactor(0, 10)
    shrinkFilter2.SetShrinkFactor(1, 10)
    shrinkFilter2.Update()

    ShrinkImageWriterType = itk.ImageFileWriter[ShrinkImageType]

    shrinkImageWriter = ShrinkImageWriterType.New()
    shrinkImageWriter.SetFileName(scale_fix_file)
    shrinkImageWriter.SetInput(shrinkFilter.GetOutput())
    shrinkImageWriter.Update()

    shrinkImageWriter2 = ShrinkImageWriterType.New()
    shrinkImageWriter2.SetFileName(scale_mov_file)
    shrinkImageWriter2.SetInput(shrinkFilter2.GetOutput())
    shrinkImageWriter2.Update()

    FixedImageType = itk.Image[itk.F, 2]
    MovingImageType = itk.Image[itk.F, 2]

    TransformType = itk.CenteredRigid2DTransform[itk.D]
    OptimizerType = itk.RegularStepGradientDescentOptimizerv4[itk.D]
    MetricType = itk.MeanSquaresImageToImageMetricv4[FixedImageType, MovingImageType]
    RegistrationType = itk.ImageRegistrationMethodv4[FixedImageType, MovingImageType]

    # 变换矩阵，最优值，配准；；；
    metric = MetricType.New()
    optimizer = OptimizerType.New()
    registration = RegistrationType.New()

    registration.SetMetric(metric)
    registration.SetOptimizer(optimizer)

    transform = TransformType.New()

    FixedImageReaderType = itk.ImageFileReader[FixedImageType]
    MovingImageReaderType = itk.ImageFileReader[MovingImageType]
    fixedImageReader = FixedImageReaderType.New()
    movingImageReader = MovingImageReaderType.New()

    fixedImageReader.SetFileName(scale_fix_file)
    movingImageReader.SetFileName(scale_mov_file)

    registration.SetFixedImage(fixedImageReader.GetOutput())
    registration.SetMovingImage(movingImageReader.GetOutput())

    TransformInitializerType = itk.CenteredTransformInitializer[TransformType, FixedImageType, MovingImageType]
    initializer = TransformInitializerType.New()
    initializer.SetTransform(transform)
    initializer.SetFixedImage(fixedImageReader.GetOutput())
    initializer.SetMovingImage(movingImageReader.GetOutput())

    initializer.MomentsOn()
    initializer.InitializeTransform()

    transform.SetAngle(0.0)

    registration.SetInitialTransform(transform)
    registration.InPlaceOn()

    translationScale = 1.0 / 1000.0

    optimizerScales = itk.OptimizerParameters[itk.D](transform.GetNumberOfParameters())
    optimizerScales.SetElement(0, 1.0)
    optimizerScales.SetElement(1, translationScale)
    optimizerScales.SetElement(2, translationScale)
    optimizerScales.SetElement(3, translationScale)
    optimizerScales.SetElement(4, translationScale)

    optimizer.SetScales(optimizerScales)
    optimizer.SetLearningRate(0.5)
    optimizer.SetMinimumStepLength(0.00001)
    optimizer.SetNumberOfIterations(50000)
    #optimizer.SetRelaxationFactor(0.8)

    registration.SetNumberOfLevels(1)
    registration.SetSmoothingSigmasPerLevel([0])
    registration.SetShrinkFactorsPerLevel([1])

    def iterationUpdate():
        currentParameter = transform.GetParameters()
        print('{},m:{}  P: {} {} {} {} {}'.format(optimizer.GetCurrentIteration(),optimizer.GetValue(),
                                            currentParameter.GetElement(0),
                                            currentParameter.GetElement(1),
                                            currentParameter.GetElement(2),
                                            currentParameter.GetElement(3),
                                            currentParameter.GetElement(4)
                                            ))

    iterationCommand = itk.PyCommand.New()
    iterationCommand.SetCommandCallable(iterationUpdate)
    optimizer.AddObserver(itk.IterationEvent(), iterationCommand)
    registration.Update()
    finalParameters = registration.GetOutput().Get().GetParameters()

    finalAngle = finalParameters[0]
    finalRotationCenterX = finalParameters[1]
    finalRotationCenterY = finalParameters[2]
    finalTranslationX = finalParameters[3]
    finalTranslationY = finalParameters[4]

    numberOfIterations = optimizer.GetCurrentIteration()
    bestValue = optimizer.GetValue()

    finalAngleInDegrees = finalAngle * 180.0 / math.pi
    print('Result :')
    print('Angle(radians):{}\n  Angle(degrees):{}\n   Center X:{}\n   Center Y:{} \n   '.format(finalAngle,
                                                                                                finalAngleInDegrees,
                                                                                                finalRotationCenterX,
                                                                                                finalRotationCenterY

                                                                                                ))

    print(
        'Translation X = {}  \nTranslation Y = {}\n  Iterations= {}\n  Metric value ={} '.format(
            finalTranslationX,
            finalTranslationY,
            numberOfIterations,
            bestValue
        ))
    matrix = transform.GetMatrix()
    offset = transform.GetOffset()

    print('matric ={}'.format(matrix))
    print('offset ={}'.format(offset))

    fixedImageReader_1 = FixedImageReaderType.New()
    movingImageReader_1 = MovingImageReaderType.New()

    fixedImageReader_1.SetFileName(left_fix_file)
    movingImageReader_1.SetFileName(left_mov_file)

    fixedImageReader_1.Update()
    movingImageReader_1.Update()

    rotationCenter = []
    rotationCenter.append(finalParameters[1])
    rotationCenter.append(finalParameters[2])

    finalTranslation = []
    finalTranslation.append(finalParameters[3])
    finalTranslation.append(finalParameters[4])

    transform_Final = TransformType.New()

    transform_Final.SetAngle(finalParameters[0])
    transform_Final.SetCenter(rotationCenter)
    transform_Final.SetTranslation(finalTranslation)

    ResampleFilterType = itk.ResampleImageFilter[MovingImageType, FixedImageType]
    resampler = ResampleFilterType.New()

    resampler.SetTransform(transform_Final)
    resampler.SetInput(movingImageReader_1.GetOutput())

    fixedImage = fixedImageReader_1.GetOutput()
    resampler.SetSize(fixedImage.GetLargestPossibleRegion().GetSize())
    resampler.SetOutputOrigin(fixedImage.GetOrigin())
    resampler.SetOutputSpacing(fixedImage.GetSpacing())
    resampler.SetOutputDirection(fixedImage.GetDirection())
    resampler.SetDefaultPixelValue(255)

    OutputImageType = itk.Image[itk.UC, 2]

    outputCast = itk.CastImageFilter[FixedImageType, OutputImageType].New()
    outputCast.SetInput(resampler.GetOutput())

    # 写入输出图片中；；
    writer = itk.ImageFileWriter[OutputImageType].New()
    writer.SetFileName(out_file)
    writer.SetInput(outputCast.GetOutput())
    writer.Update()


# save_path = "D:/ceshi1/Crop2/Registrated_2"
# ori_fix_path = "D:/ceshi1/Crop2/Registrated_2/355.png"
# file_path = "D:/ceshi1/Crop2/right"
# scale_fix_path = "D:/ceshi1/scale_fix.png"
# scale_mov_path = "D:/ceshi1/scale_mov.png"
#
#
#
# file_list = os.listdir(file_path)
# num_len = len(file_list)
# initial_index = 0
#
#
#
# while (initial_index <num_len):
#     file_name = file_list[initial_index]
#     ori_mov_path = os.path.join(file_path, file_name)
#     save_name = os.path.join(save_path, file_name)
#     print(ori_fix_path)
#     print(ori_mov_path)
#     print(scale_fix_path)
#     print(scale_mov_path)
#     print(save_name)
#     print('----------------'*20)
#     # 开始配准
#     regist_zompile(ori_fix_path, ori_mov_path, scale_fix_path, scale_mov_path, save_name)
#     initial_index +=1
#     ori_fix_path = save_name




ori_fix_path = "D:/ceshi1/Crop2/171.png"
ori_mov_path = "D:/ceshi1/Crop2/172.png"
scale_fix_path = "D:/ceshi1/Crop/555.png"
scale_mov_path = "D:/ceshi1/Crop/5555.png"
save_path = "D:/ceshi1/Crop2/save.png"

regist_zompile(ori_fix_path,ori_mov_path,scale_fix_path,scale_mov_path,save_path)



# file_path ="D;/ceshi1/Crop/Bone_ceshi1/left_ceshi"
#
#
# file_list = os.listdir(file_path)
#
# num_len = len(file_list)
# initial_index = num_len-1
#
# while (initial_index >= 0):
#     file_name = file_list[initial_index]
#     ori_mov_path = os.path.join(file_path, file_name)
#     save_name = os.path.join(save_path, file_name)
#     print(ori_fix_path)
#     print(ori_mov_path)
#     print(scale_fix_path)
#     print(scale_mov_path)
#     print(save_name)
#     print('----------------'*20)
#     # 开始配准
#     regist_zompile(ori_fix_path, ori_mov_path, scale_fix_path, scale_mov_path, save_name)
#
#     initial_index -=1
#     ori_fix_path = save_name



# if __name__ =='__main__':
#     img_path = "D:/ceshi1/Crop2/Raw_Pic"
#     save_path = "D:/ceshi1/Crop2/Registrated_2"
#     scale1_path = "D:/ceshi1/Crop/1.png"
#     scale2_path = "D:/ceshi1/Crop/2.png"
#
#
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     path_list = os.listdir(img_path)
#
#     len_image = len(path_list)
#     initial_index = int(len_image/2)
#     left_fix_path = os.path.join(img_path,path_list[initial_index])
#     right_fix_path = os.path.join(img_path,path_list[initial_index])
#
#     left_index = initial_index-1
#     right_index = initial_index +1
#
#     while(left_index>=0 or right_index<len_image):
#         if (left_index>=0):
#             left_mov_path  = os.path.join(img_path,str(path_list[left_index]))
#             left_save_path = os.path.join(save_path,str(path_list[left_index]))
#
#
#             print("left----------------\n")
#             print(left_fix_path,left_mov_path,scale1_path,scale2_path,left_save_path)
#             regist_zompile(left_fix_path,left_mov_path,scale1_path,scale2_path,left_save_path)
#             left_index -=1
#             left_fix_path = left_save_path
#
#         if(right_index<len_image):
#
#             right_mov_path = os.path.join(img_path, str(path_list[right_index]))
#             right_save_path = os.path.join(save_path, str(path_list[right_index]))
#
#             print("right------------------\n")
#             print(right_fix_path, right_mov_path, scale1_path, scale2_path, right_save_path)
#             regist_zompile(right_fix_path, right_mov_path, scale1_path, scale2_path, right_save_path)
#             right_index += 1
#             right_fix_path = right_save_path
#
#         #删除存放的文件；；；
#         os.remove(scale1_path)
#         os.remove(scale2_path)