import os
import shutil
from math import inf

import fitz
from PIL import Image
from PIL.Image import open as imgopen

from compressEvaluate import GetPSNR


def clear_folder(folder_path):
    """
    清空指定文件夹下的所有文件和子文件夹
    :param folder_path: 文件夹路径
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在")
        return

    # 遍历文件夹中的所有内容
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)  # 获取文件或文件夹的完整路径

        try:
            # 如果是文件，则删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或符号链接
                print(f"已删除文件: {file_path}")
            # 如果是文件夹，则递归删除
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除文件夹及其内容
                print(f"已删除文件夹: {file_path}")
        except Exception as e:
            print(f"删除 {file_path} 时出错: {e}")
# 测试压缩后的文件与原文件对比的图像PSNR
# 逐步解析pdf文件,并且反馈进度信息(主要是读取图片大小和占比)
def parse_pdf_file(filepath,outpath):
    filename = filepath
    # 获取文件总大小
    filesize = os.path.getsize(filename) / 1024
    # 解析文件
    doc = fitz.open(filename)
    # doc = fitz.open('./paper/test.pdf')
    # 获取图片文件大小
    pix_size = 0
    img_size = 0
    page_number = doc.page_count
    now_page = 0
    count=0
    img_list=[]
    for page in doc.pages():
        imageList = page.get_images()

        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)

            # 保存图像到文件
            new_name = f"{outpath}/image_{count}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            img = imgopen(new_name)
            pix_size += img.height * img.width * 3 // 1024
            img_size += os.path.getsize(new_name) / 1024
            page.delete_image(xref)
            img.close()
            if os.path.getsize(new_name)<100:
                os.remove(new_name)
            else:
                img_list.append(new_name)
                count += 1

        now_page += 1
    doc.close()
    print("图片文件总大小:",img_size)
    return img_list

def parse_pdf_file_repalce(filepath,outpath):
    file_paths = []
    # 遍历文件夹
    for item in os.listdir(outpath):
        # 拼接完整路径
        full_path = os.path.join(outpath, item)
        # 判断是否是文件（不是文件夹）
        if os.path.isfile(full_path):
            file_paths.append(full_path)
    return file_paths


def GetPdfQualLoss():
    clear_folder("./src/temp")
    clear_folder("./src/temp2")
    ls1=parse_pdf_file("src/imageData/d5595ebb-e479-4e49-909a-b348182282b0.pdf", "src/temp")
    ls2=parse_pdf_file("src/IJCV-xianzhu.pdf", "src/temp2")
    i=0
    sum=0.0
    count=0
    while i<len(ls2):
        img = Image.open(ls1[i])
        actsize=img.height*img.width*3
        cr=os.path.getsize(ls2[i])
        psnr=GetPSNR(ls1[i],ls2[i],reshape=True)
        print(psnr,",",cr/actsize)
        if psnr<60:
            sum+=psnr
            count+=1
        i+=1
    print('文件平均PSNR:',sum/count)

GetPdfQualLoss()
#476 25.81
#465 30.11

#xz 281 27.28
