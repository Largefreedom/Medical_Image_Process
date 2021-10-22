import itk
import math
import os

def ceshi_run(left_fix_file, left_mov_file,out_file):
        print('开始进行配准')
        print(left_fix_file, left_mov_file,out_file)
        ShrinkImageType = itk.Image[itk.F, 2]
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

        FixedImageReaderType = itk.ImageFileReader[ShrinkImageType]
        MovingImageReaderType = itk.ImageFileReader[ShrinkImageType]
        fixedImageReader = FixedImageReaderType.New()
        movingImageReader = MovingImageReaderType.New()

        fixedImageReader.SetFileName(left_fix_file)
        movingImageReader.SetFileName(left_mov_file)

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
        optimizer.SetLearningRate(1.0)
        optimizer.SetMinimumStepLength(0.0001)
        optimizer.SetNumberOfIterations(10000)

        registration.SetNumberOfLevels(1)
        registration.SetSmoothingSigmasPerLevel([0])
        registration.SetShrinkFactorsPerLevel([1])

        def iterationUpdate():
            currentParameter = transform.GetParameters()
            print('{} m:{}  P: {} {} {} {} {}'.format(optimizer.GetCurrentIteration(),optimizer.GetValue(),
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
        resampler.SetInput(movingImageReader.GetOutput())

        fixedImage = fixedImageReader.GetOutput()
        resampler.SetSize(fixedImage.GetLargestPossibleRegion().GetSize())
        resampler.SetOutputOrigin(fixedImage.GetOrigin())
        resampler.SetOutputSpacing(fixedImage.GetSpacing())
        resampler.SetOutputDirection(fixedImage.GetDirection())
        resampler.SetDefaultPixelValue(0)

        OutputImageType = itk.Image[itk.UC, 2]

        outputCast = itk.CastImageFilter[FixedImageType, OutputImageType].New()
        outputCast.SetInput(resampler.GetOutput())

        # 写入输出图片中；；
        writer = itk.ImageFileWriter[OutputImageType].New()
        writer.SetFileName(out_file)
        writer.SetInput(outputCast.GetOutput())
        writer.Update()




# if __name__ =='__main__':
#
#         img_path = "D:/ceshi1/Crop2/Regis/kidney_left"
#         save_path = "D:/ceshi1/Crop2/Regis/kidney_left_regised"
#
#
#         if not os.path.exists(save_path):
#             os.makedirs(save_path)
#         path_list = os.listdir(img_path)
#
#         len_image = len(path_list)
#         initial_index = int(len_image / 2)
#         left_fix_path = os.path.join(img_path, path_list[initial_index])
#         right_fix_path = os.path.join(img_path, path_list[initial_index])
#
#         left_index = initial_index - 1
#         right_index = initial_index + 1
#
#         while (left_index >= 0 or right_index < len_image):
#             if (left_index >= 0):
#                 left_mov_path = os.path.join(img_path, str(path_list[left_index]))
#                 left_save_path = os.path.join(save_path, str(path_list[left_index]))
#
#                 print("left----------------\n")
#                 #print(left_fix_path, left_mov_path, scale1_path, scale2_path, left_save_path)
#                 ceshi_run(left_fix_path, left_mov_path, left_save_path)
#                 left_index -= 1
#                 left_fix_path = left_save_path
#
#             if (right_index < len_image):
#                 right_mov_path = os.path.join(img_path, str(path_list[right_index]))
#                 right_save_path = os.path.join(save_path, str(path_list[right_index]))
#
#                 print("right------------------\n")
#                 #print(right_fix_path, right_mov_path, scale1_path, scale2_path, right_save_path)
#                 ceshi_run(right_fix_path, right_mov_path, right_save_path)
#                 right_index += 1
#                 right_fix_path = right_save_path
#



# fix_path = "D:/ceshi1/Crop/heart_ceshi/033.png"
# mov_path = 'D:/ceshi1/Crop/heart_ceshi/034.png'
# save = "D:/ceshi1/Crop/heart_ceshi/save.png"
#
# ceshi_run(fix_path,mov_path,save)




file_path ="D:/ceshi1/Crop2/Regis/bone_left"
origin_path = 'D:/ceshi1/Crop2/Regis/Bone_regised/004.png'
save_path = "D:/ceshi1/Crop2/Regis/Bone_regised"
file_list = os.listdir(file_path)
num_len = len(file_list)
initial_index = num_len - 1

while (initial_index >=0):
    file_name = file_list[initial_index]
    ori_mov_path = os.path.join(file_path, file_name)
    save_name = os.path.join(save_path, file_name)
    print(ori_mov_path)

    print(save_name)
    print('----------------'*20)
    # 开始配准
    ceshi_run(origin_path, ori_mov_path,save_name)

    initial_index -=1
    origin_path = save_name