import cv2
import math
import numpy
from skimage.metrics._structural_similarity import structural_similarity
from skimage.metrics.simple_metrics import peak_signal_noise_ratio


def psnr1(img1, img2):
    # compute mse
    # mse = np.mean((img1-img2)**2)
    mse = numpy.mean((img1 / 1.0 - img2 / 1.0) ** 2)
    # compute psnr
    if mse < 1e-10:
        return 100
    psnr1 = 20 * math.log10(255 / math.sqrt(mse))
    return psnr1


def psnr2(img1, img2):
    mse = numpy.mean((img1 / 255.0 - img2 / 255.0) ** 2)
    if mse < 1e-10:
        return 100
    psnr2 = 20 * math.log10(1 / math.sqrt(mse))
    return psnr2


"""
PSNR高于40dB说明图像质量极好（即非常接近原始图像），
在30—40dB通常表示图像质量是好的（即失真可以察觉但可以接受），
在20—30dB说明图像质量差；
最后，PSNR低于20dB图像不可接受
"""
def GetPSNR(imgPath1, imgPath2,reshape=False,gray=False):
    imag1 = cv2.imread(imgPath1)
    imag2 = cv2.imread(imgPath2)
    if reshape:
        image_size = [1024, 1024]  # 将图像转化为512*512大小的尺寸
        imag1 = cv2.resize(imag1, image_size, interpolation=cv2.INTER_CUBIC)
        imag2 = cv2.resize(imag2, image_size, interpolation=cv2.INTER_CUBIC)
    if gray:
        imag1 = cv2.cvtColor(imag1, cv2.COLOR_BGR2GRAY)#将图像转化为灰度图像，不是必须转，也可以使用原始的彩色图像
        imag2 = cv2.cvtColor(imag2, cv2.COLOR_BGR2GRAY)#将图像转化为灰度图像，不是必须转，也可以使用原始的彩色图像
    return peak_signal_noise_ratio(imag1, imag2, data_range=255)


"""
SSIM > 0.9：图像质量非常好，失真几乎不可察觉。
0.7 < SSIM < 0.9：图像质量较好，存在轻微失真，但通常可以接受。
SSIM < 0.7：图像质量较差，失真明显。
SSIM < 0.5：图像质量非常差，失真严重。
"""
def GetSSIM(imgPath1, imgPath2,reshape=False,gray=False):
    imag1 = cv2.imread(imgPath1)
    imag2 = cv2.imread(imgPath2)
    if reshape:
        image_size = [1024, 1024]  # 将图像转化为512*512大小的尺寸
        imag1 = cv2.resize(imag1, image_size, interpolation=cv2.INTER_CUBIC)
        imag2 = cv2.resize(imag2, image_size, interpolation=cv2.INTER_CUBIC)
    if gray:
        imag1 = cv2.cvtColor(imag1, cv2.COLOR_BGR2GRAY)  # 将图像转化为灰度图像，不是必须转，也可以使用原始的彩色图像
        imag2 = cv2.cvtColor(imag2, cv2.COLOR_BGR2GRAY)  # 将图像转化为灰度图像，不是必须转，也可以使用原始的彩色图像
    return structural_similarity(imag1, imag2, win_size=11, data_range=255, multichannel=True,channel_axis=-1)

inf = "./src/e017.jpg"
of = "./out/out.jpg"
# print(GetSSIM(inf,of))


