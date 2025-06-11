import os

from PIL import Image

from compressEvaluate import GetPSNR


def compress_test_dpi(input_path, output_path, quality, target):
    dpiloss = 0.99
    while dpiloss >= 0.01:
        with Image.open(input_path) as img:
            width, height = img.size
            act=width*height*3
            new_size = (int(width * dpiloss), int(height * dpiloss))
            resized_img = img.resize(new_size, Image.LANCZOS)
            resized_img.save(output_path, quality=quality)
            if os.path.getsize(output_path) /act < target:
                break
            else:
                dpiloss -= 0.02
    return dpiloss


# spath = 'src/Kodak-Lossless-True-Color-Image-Suite-master/Image_jpeg/3.jpg'


def test2():
    i=94
    while i>=0:
        # 计算24张图片的平均PSNR
        psnr=0.0
        dpilos=0.0
        for index in range(1,25):
            path=f'src/Kodak-Lossless-True-Color-Image-Suite-master/Image_jpeg/{index}.jpg'
            dpilos+=compress_test_dpi(path, 'out/out.jpg', i, 0.015)
            psnr+=GetPSNR(path, 'out/out.jpg', reshape=True)
        psnr=psnr/24
        dpilos=dpilos/24
        print(f"{dpilos},{i},{psnr}")
        i-=4


test2()
"""0.693333333333333,34,28.646888936793314
0.6966666666666663,33,28.60867562154817
0.708333333333333,32,28.63413317147329
0.7133333333333329,31,28.611992672333006
0.7216666666666662,30,28.61614203084848
0.7333333333333331,29,28.63793647843637
0.7408333333333332,28,28.617307740602552
0.7508333333333331,27,28.59344630625736"""
