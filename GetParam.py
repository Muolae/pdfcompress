# 测试综合压缩的预测数据
import os
from io import BytesIO

from PIL import Image

from compressEvaluate import GetPSNR, GetSSIM
import matplotlib.pyplot as plt
import numpy as np

# 生成随机数据


plt.show()
def GetCompressData():
    xlist=[]
    ylist=[]
    dpiloss = 0.1
    while dpiloss <= 0.99:
        # 计算24张图片的平均PSNR
        psnr = 0.0
        actsize=0.0
        cs=0.0
        for index in range(1, 25):
            path = f'src/Kodak-Lossless-True-Color-Image-Suite-master/PhotoCD_PCD0992/{index}.png'
            img = Image.open(path)
            a=img.width*img.height*3//1024
            actsize += a
            width, height = img.size
            n_w = int(width * dpiloss)
            n_h = int(height * dpiloss)
            new_size = (n_w, n_h)
            resized_img = img.resize(new_size, Image.LANCZOS)
            rgbimg = resized_img.convert('RGB')
            rgbimg.save('out/out.jpg', quality=38)

            c=os.path.getsize('out/out.jpg')//1024
            cs+=c
            p= GetPSNR(path, 'out/out.jpg',reshape=True)
            psnr +=p
            xlist.append(dpiloss)
            ylist.append(p)
        psnr = psnr / 24
        print(f"[{dpiloss},{psnr},{cs/actsize}],")
        dpiloss += 0.02

    np.random.seed(42)
    x =xlist
    y = ylist

    # 创建散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', alpha=0.7, label='Data Points')

    # 添加标题和标签
    plt.title('图片压缩率与quality的关系', fontsize=14)
    plt.xlabel('quality', fontsize=12)
    plt.ylabel('压缩率', fontsize=12)
    plt.legend()

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.show()

def compress_hybird(pic_path, out_path, compress_rate, step=8,eva=True,ssimon=True):
    quality = 95
    with open(pic_path, 'rb') as f:
        pic_byte = f.read()
        pic_bytetemp = pic_byte

    img = Image.open(pic_path)
    current_size = img.height * img.width * 3 // 1024
    target_size = current_size * compress_rate-0.4
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
        new_size = (n_w, n_h)
        resized_img = img.resize(new_size, Image.LANCZOS)
        rgbimg = resized_img.convert('RGB')
        rgbimg.save(out_path, quality=38)
        if os.path.getsize(out_path) // 1024 < target_size:
            break
        else:
            dpiloss -= 0.01*step
            if dpiloss <= 0.1:
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

GetCompressData()