import os
from PIL import Image
from PIL import ImageFile
from io import BytesIO

import cv2
import numpy as np
# 压缩图片文件
from PIL.Image import Resampling

# 图片压缩程序1:
# 有损压缩,压缩效率较高
# 支持分辨率和图片质量压缩
# TODO 无法压缩会进入死循环
from compressEvaluate import GetPSNR, GetSSIM


def compress_image(infile, outfile, mb=70, quality=85, k=0.9):  # 通常你只需要修改mb大小
    """不改变图片尺寸压缩到指定大小
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param k: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """

    o_size = os.path.getsize(infile) // 1024  # 函数返回为字节，除1024转为kb（1kb = 1024 bit）
    print('before_size:{} after_size:{}'.format(o_size, mb))
    if o_size <= mb:
        return outfile

    ImageFile.LOAD_TRUNCATED_IMAGES = True  # 防止图像被截断而报错

    while o_size > mb:
        im = Image.open(infile)
        # rgbim = im.convert('RGB')
        x, y = im.size
        out = im.resize((int(x * k), int(y * k)), Resampling.LANCZOS)  # 最后一个参数设置可以提高图片转换后的质量
        try:
            out = out.convert('RGB')  # 删除不支持的通道
            out.save(outfile, quality=quality)  # quality为保存的质量，从1（最差）到95（最好），此时为85
        except Exception as e:
            print(e)
            break
        o_size = os.path.getsize(outfile) // 1024
        print("本轮压缩后图片大小:", o_size)
    return outfile


def byte_compress(pic_path, out_path, target_size=199, quality=90, step=5, pic_type='.jpg'):
    # 读取图片bytes
    with open(pic_path, 'rb') as f:
        pic_byte = f.read()

    img_np = np.frombuffer(pic_byte, np.uint8)
    img_cv = cv2.imdecode(img_np, cv2.IMREAD_ANYCOLOR)

    img = Image.open(pic_path)
    current_size = img.height * img.width * 3 // 1024
    print("图片压缩前的大小为(KB)：", current_size)
    while current_size > target_size:
        pic_byte = cv2.imencode(pic_type, img_cv, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1]
        if quality - step < 0:
            break
        quality -= step
        current_size = len(pic_byte) / 1024

    print("图片压缩后的大小为(KB)：", current_size)
    # 保存图片
    with open(out_path, 'wb') as f:
        f.write(BytesIO(pic_byte).getvalue())

    return len(pic_byte) / 1024


# todo 采用渐变步长技术提高压缩效率
def compress_by_size(pic_path, out_path, compress_rate=1.0, quality=95, step=3):
    # 读取图片bytes
    with open(pic_path, 'rb') as f:
        pic_byte = f.read()
        pic_bytetemp = pic_byte

    img = Image.open(pic_path)
    current_size = img.height * img.width * 3 // 1024
    target_size = current_size * compress_rate
    # print("图片压缩前的大小为(KB)：", current_size)
    while current_size > target_size:  # 当达到目标压缩大小后退出循环
        img = Image.open(BytesIO(pic_byte))
        buf = BytesIO()
        rgbimg = img.convert('RGB')
        rgbimg.save(buf, format="JPEG", quality=quality, subsampling=0)
        pic_bytetemp = buf.getvalue()
        if quality - step < 0:  # 以降低到最小质量
            # print("已经无法继续压缩")
            break
        quality -= step
        current_size = len(pic_bytetemp) / 1024
        # print(quality,current_size)
    # print("图片压缩后的大小为(KB)：", current_size)
    # 保存图片
    with open(out_path, 'wb') as f:
        f.write(pic_bytetemp)
    psnr = GetPSNR(pic_path, out_path)
    ssim = GetSSIM(pic_path, out_path)

    return psnr, ssim


def compress_by_quality(pic_path, out_path, quality):
    img = Image.open(pic_path)
    rgbimg = img.convert('RGB')
    rgbimg.save(out_path, format="JPEG", quality=quality, subsampling=2)
    psnr = GetPSNR(pic_path, out_path)
    ssim = GetSSIM(pic_path, out_path)
    return psnr, ssim

# 将图片压缩到指定的大小
def compress_hybird(pic_path, out_path, compress_rate, step=8,eva=True,ssimon=True):
    quality = 95
    with open(pic_path, 'rb') as f:
        pic_byte = f.read()
        pic_bytetemp = pic_byte

    img = Image.open(pic_path)
    current_size = img.height * img.width * 3 // 1024
    target_size = current_size * compress_rate
    while current_size > target_size:  # 当达到目标压缩大小后退出循环
        img = Image.open(BytesIO(pic_byte))
        buf = BytesIO()
        rgbimg = img.convert('RGB')
        rgbimg.save(buf, format="JPEG", quality=quality, subsampling=0)
        pic_bytetemp = buf.getvalue()
        if quality - step < 38:  # 改用分辨率进一步压缩
            break
        quality -= step
        current_size = len(pic_bytetemp) / 1024
    with open(out_path, 'wb') as f:
        f.write(pic_bytetemp)
    dpiloss = 0.98
    while current_size > target_size:
        width, height = img.size
        n_w=int(width * dpiloss)
        n_h=int(height * dpiloss)
        if n_w<8:
            n_w=8
        if n_h<8:
            n_h=8
        new_size = (n_w, n_h)
        resized_img = img.resize(new_size, Image.LANCZOS)
        rgbimg = resized_img.convert('RGB')
        rgbimg.save(out_path, quality=38)
        if os.path.getsize(out_path) // 1024 < target_size:
            break
        else:
            dpiloss -= 0.02*step
            if dpiloss <= 0.05:
                break
    if eva:
        psnr=GetPSNR(pic_path,out_path,reshape=True)
        if ssimon:
            ssim=GetSSIM(pic_path,out_path,reshape=True)
        else:
            ssim=0.8
        return psnr, ssim
    else:
        return 23.0,0.8

# 将图片压缩到指定的psnr
def compress_by_psnr(pic_path, out_path, psnr, step=5,onssim=False):
    qual=38
    if psnr>29.2:
        while qual<100:
            img = Image.open(pic_path)
            rgbimg = img.convert('RGB')
            rgbimg.save(out_path, format="JPEG", quality=qual, subsampling=0)
            current_psnr=GetPSNR(pic_path,out_path)
            if current_psnr>psnr:
                break
            qual+=step
    else:
        dpiloss = 0.1
        img = Image.open(pic_path)
        while dpiloss<1:
            width, height = img.size
            n_w = int(width * dpiloss)
            n_h = int(height * dpiloss)
            if n_w < 8:
                n_w = 8
            if n_h < 8:
                n_h = 8
            new_size = (n_w, n_h)
            resized_img = img.resize(new_size, Image.LANCZOS)
            rgbimg = resized_img.convert('RGB')
            rgbimg.save(out_path, quality=38)
            current_psnr = GetPSNR(pic_path, out_path,reshape=True)
            if current_psnr>psnr:
                break
            dpiloss+=0.01*step
    psnr = GetPSNR(pic_path, out_path, reshape=True)
    if onssim:
        ssim = GetSSIM(pic_path, out_path, reshape=True)
    else:
        ssim=0
    return psnr, ssim

def min_compress(pic_path, out_path):
    dpiloss = 0.1
    img = Image.open(pic_path)
    width, height = img.size
    n_w = int(width * dpiloss)
    n_h = int(height * dpiloss)
    if n_w < 8:
        n_w = 8
    if n_h < 8:
        n_h = 8
    new_size = (n_w, n_h)
    resized_img = img.resize(new_size, Image.LANCZOS)
    rgbimg = resized_img.convert('RGB')
    rgbimg.save(out_path, quality=38)
    return 1.0,1.0

# spath = 'src/Kodak-Lossless-True-Color-Image-Suite-master/Image_jpeg/3.jpg'
# print(compress_by_psnr(spath,'out/out.jpg',23))

# for i in range(1,25):
# i=11
# inf = f"./src/Kodak-Lossless-True-Color-Image-Suite-master/PhotoCD_PCD0992/{i}.png"
# of = "./out/out.jpg"
#
# lossness_compress(inf, of, compress_rate=0,quality=95,step=5)
# print(os.path.getsize(of)/os.path.getsize(inf))
# compress_image("./src/p1.png",r"",quality=60)
# img=Image.open("./src/Kodak-Lossless-True-Color-Image-Suite-master/PhotoCD_PCD0992/11.png")
# img.save(of,quality=1)
