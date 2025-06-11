import os
import shutil

import fitz
import numpy
import pymupdf
from PIL.Image import Image, fromarray
from PIL.Image import open as imgopen

import picCompress


def image_replace(page: pymupdf.Page, xref: int, *, filename=None, pixmap=None, stream=None):
    doc = page.parent  # the owning document
    if not doc.xref_is_image(xref):
        raise ValueError("xref not an image")  # insert new image anywhere in page
    if bool(filename) + bool(stream) + bool(pixmap) != 1:
        raise ValueError("Exactly one of filename/stream/pixmap must be given")
    new_xref = page.insert_image(
        page.rect, filename=filename, stream=stream, pixmap=pixmap
    )
    doc.xref_copy(new_xref, xref)  # copy over new to old
    page.delete_image(new_xref)
    last_contents_xref = page.get_contents()[-1]
    # new image insertion has created a new /Contents source,
    # which we will set to spaces now
    doc.update_stream(last_contents_xref, b" ")
    page._image_info = None  # clear cache of extracted image information


# pdf压缩的核心功能函数
def pdf_compress(filename, ws, compressRate):
    # 解析文件
    doc = fitz.open(filename)
    # doc = fitz.open('./paper/test.pdf')

    # 获取图片文件大小
    # pix_size = 0
    step = 0
    page_number = doc.page_count * 2
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            # pix_size += os.path.getsize(new_name)
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    # print("图片大小:", pix_size / 1024, "KB")
    imgcount = 0
    for page in doc.pages():
        imageList = page.get_images()

        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            #
            # # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            # with open(new_name, "wb") as img_file:
            #     img_file.write(image_info["image"])

            loc = page.get_image_rects(imginfo)
            doc._deleteObject(imginfo[0])
            jname = new_name.replace(new_name.split(".")[-1], 'jpg')

            picCompress.compress_by_size(new_name, jname, compress_rate=compressRate)
            # image_replace(page,xref,filename=jname)
            # page.get_image_rects(imginfo)
            page.insert_image(loc[0], filename=jname)
            imgcount += 1
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    doc.ez_save(filename='./out/out.pdf')


# 逐步解析pdf文件,并且反馈进度信息(主要是读取图片大小和占比)
def parse_pdf_file(ws, filename):
    fn = filename
    filename = "./src/uploadfile/" + filename
    # 获取文件总大小
    filesize = os.path.getsize(filename) / 1024
    print("初始文件大小:", filesize, "KB")

    # 解析文件
    doc = fitz.open(filename)
    # doc = fitz.open('./paper/test.pdf')

    # 获取图片文件大小
    pix_size = 0
    img_size = 0
    page_number = doc.page_count
    now_page = 0
    for page in doc.pages():
        imageList = page.get_images()

        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)

            # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            img = imgopen(new_name)
            pix_size += img.height * img.width * 3 // 1024
            img_size += os.path.getsize(new_name) / 1024
            page.delete_image(xref)
            img.close()
            os.remove(new_name)
        now_page += 1
        ws.send("reg:" + str(int(100 * now_page / page_number)))
    doc.ez_save("src/temp/" + fn,garbage=4,clean=True,pretty=True)
    emptypdf_size = os.path.getsize("src/temp/" + fn) // 1024
    doc.close()
    os.remove("src/temp/" + fn)
    return filesize, img_size, pix_size, emptypdf_size


# 逐步解析pdf文件,并且反馈进度信息(主要是读取图片大小和占比)
def parse_pdf_image(ws, filename,id):
    fn = filename
    dirname = str(filename).split('.')[0]
    filename = "./src/uploadfile/" + filename
    # 获取文件总大小
    filesize = os.path.getsize(filename) / 1024
    doc = fitz.open(filename)
    pix_size = 0
    img_size = 0
    page_number = doc.page_count
    now_page = 0
    imglist = []
    # todo 创建临时文件夹
    os.mkdir(f"src/temp/{id}")
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            # 保存图像到文件
            new_name = f"./src/temp/{id}/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            imglist.append(f"image_{xref}.{image_info['ext']}")
            img = imgopen(new_name)
            pix_size += img.height * img.width * 3 // 1024
            img_size += os.path.getsize(new_name) / 1024
            page.delete_image(xref)
        now_page += 1
        ws.send("reg:" + str(int(100 * now_page / page_number)))
    doc.ez_save(f"src/temp/" + fn,garbage=4,clean=True,pretty=True)
    emptypdf_size = os.path.getsize("src/temp/" + fn) // 1024
    doc.close()
    os.remove("src/temp/" + fn)
    return filesize, img_size, pix_size, emptypdf_size, imglist


# pdf压缩的核心功能函数
def pdf_compress_by_quality(filename, ws, quality):
    # 解析文件
    doc = fitz.open(filename)
    # doc = fitz.open('./paper/test.pdf')

    # 获取图片文件大小
    # pix_size = 0
    step = 0
    page_number = doc.page_count * 2
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            # pix_size += os.path.getsize(new_name)
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    # print("图片大小:", pix_size / 1024, "KB")
    imgcount = 0
    psnr = 0.0
    ssim = 0.0
    for page in doc.pages():
        imageList = page.get_images()

        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            #
            # # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            jname = new_name.replace(new_name.split(".")[-1], 'jpg')

            psnr_t, ssim_t = picCompress.compress_by_quality(new_name, jname, quality=quality)
            psnr += psnr_t
            ssim += ssim_t
            image_replace(page, xref, filename=jname)
            imgcount += 1
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    sfn = './out/' + os.path.basename(filename)
    doc.ez_save(filename=sfn,garbage=4,clean=True,pretty=True)
    return os.path.getsize(sfn) / 1024, psnr / imgcount, ssim / imgcount


# quality:预设压缩质量,imgrate:要求图片压缩率,maxsize:限定的最大大小
def pdf_compress_by_size(filename, ws, quality, imgrate, maxsize, emptysize=0):
    # 首先导出原始图片
    doc2 = fitz.open(filename)
    imagePathList = []
    cImageList = []
    ws.send("info:正在解析图片")
    step = 0
    page_number = doc2.page_count
    for page in doc2.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc2.extract_image(xref)
            # 保存图像到文件
            new_name = f"src/temp/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
                imagePathList.append(new_name)
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    # 然后先按照给定的压缩质量压缩
    img_size = 0
    psnr = 0.0
    ssim = 0.0
    ws.send("info:正在预压缩图片")
    step = 0
    for path in imagePathList:
        jname = path.replace(path.split(".")[-1], 'jpg')
        psnr_t, ssim_t = picCompress.compress_by_quality(path, jname, quality=quality)
        psnr += psnr_t
        ssim += ssim_t
        cImageList.append(jname)
        img_size += os.path.getsize(jname) / 1024
        step += 1
        ws.send("reg:" + str(int(100 * step / len(imagePathList))))
    # 判断大小是否符合体积要求(考虑误差)
    index = 0
    step = 0
    print(img_size, emptysize, maxsize, imgrate, quality, "---")
    if img_size + emptysize < maxsize:
        ws.send("info:正在生成文件")
        for page in doc2.pages():
            imageList = page.get_images()
            for imginfo in imageList:
                xref = imginfo[0]  # 获取图像的 xref
                image_replace(page, xref, filename=cImageList[index])
                index += 1
            step += 1
            ws.send("reg:" + str(int(100 * step / page_number)))
    else:
        # 如果不符合要求,就重新压缩一遍
        index = 0
        psnr = 0.0
        ssim = 0.0
        ws.send("info:正在压缩图片")
        for path in imagePathList:
            psnr_t, ssim_t = picCompress.compress_by_size(path, cImageList[index], compress_rate=imgrate,
                                                          quality=quality, step=1)
            psnr += psnr_t
            ssim += ssim_t
            index += 1
            ws.send("reg:" + str(int(100 * index / len(imagePathList))))
        index = 0
        step = 0
        ws.send("info:正在生成文件")
        for page in doc2.pages():
            imageList = page.get_images()
            for imginfo in imageList:
                xref = imginfo[0]  # 获取图像的 xref
                image_replace(page, xref, filename=cImageList[index])
                index += 1
            step += 1
            ws.send("reg:" + str(int(100 * step / page_number)))
    # 生成文件
    sfn = './out/' + os.path.basename(filename)
    doc2.ez_save(filename=sfn)
    psnr = psnr / len(imagePathList)
    ssim = ssim / len(imagePathList)
    return os.path.getsize(sfn) / 1024, psnr, ssim


# pdf压缩的核心功能函数
def pdf_compress_by_psnr(filename, ws, target_psnr,onssim=False):
    # 解析文件
    doc = fitz.open("./src/uploadfile/" + filename)
    dirname = str(filename).split('.')[0]
    step = 0
    page_number = doc.page_count * 2
    ws.send("info:解析图片")
    os.mkdir(f"src/temp/{dirname}")
    os.mkdir(f"src/temp2/{dirname}")
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            # 保存图像到文件
            new_name = f"./src/temp/{dirname}/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            # pix_size += os.path.getsize(new_name)
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    imgcount = 0
    psnr = 0.0
    ssim = 0.0
    ws.send("info:正在压缩图片")
    for page in doc.pages():
        imageList = page.get_images()

        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            #
            # # 保存图像到文件
            new_name = f"./src/temp/{dirname}/image_{xref}.{image_info['ext']}"
            jname = f"./src/temp2/{dirname}/image_{xref}.jpg"

            psnr_t, ssim_t = picCompress.compress_by_psnr(new_name, jname, target_psnr,onssim=onssim)
            psnr += psnr_t
            ssim += ssim_t
            image_replace(page, xref, filename=jname)
            imgcount += 1
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    sfn = './out/' + os.path.basename(filename)
    doc.ez_save(filename=sfn,garbage=4,clean=True,pretty=True)
    ws.send("info:文件压缩完成")
    # 清除数据
    shutil.rmtree(f"src/temp/{dirname}")
    shutil.rmtree(f"src/temp2/{dirname}")
    return os.path.getsize(sfn) / 1024, psnr / imgcount, ssim / imgcount


# pdf压缩的核心功能函数
def pdf_compress_by_size2(filename, ws, compressrate,ssimon=True):
    # 解析文件
    doc = fitz.open("./src/uploadfile/" + filename)
    dirname = str(filename).split('.')[0]
    step = 0
    page_number = doc.page_count * 2
    ws.send("info:正在解析图片")
    os.mkdir(f"src/temp/{dirname}")
    os.mkdir(f"src/temp2/{dirname}")
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            # 保存图像到文件
            new_name = f"./src/temp/{dirname}/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            # pix_size += os.path.getsize(new_name)
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    # print("图片大小:", pix_size / 1024, "KB")
    imgcount = 0
    psnr = 0.0
    ssim = 0.0
    ws.send("info:正在压缩图片")
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            new_name = f"./src/temp/{dirname}/image_{xref}.{image_info['ext']}"
            jname = f"./src/temp2/{dirname}/image_{xref}.jpg"

            psnr_t, ssim_t = picCompress.compress_hybird(new_name, jname, compress_rate=compressrate,ssimon=ssimon)
            # psnr_t, ssim_t = picCompress.min_compress(new_name, jname)
            psnr += psnr_t
            ssim += ssim_t
            image_replace(page, xref, filename=jname)
            imgcount += 1
        step += 1
        ws.send("reg:" + str(int(100 * step / page_number)))
    sfn = './out/' + os.path.basename(filename)
    doc.ez_save(filename=sfn,garbage=4,clean=True,pretty=True)
    ws.send("info:压缩完成")
    # 清除数据
    shutil.rmtree(f"src/temp/{dirname}")
    shutil.rmtree(f"src/temp2/{dirname}")
    return os.path.getsize(sfn) / 1024, psnr / imgcount, ssim / imgcount


def GetActSize(path):
    img = imgopen(path)
    return img.height * img.width * 3 // 1024


# 根据图片优先级压缩图片
# 对9优先级单独处理,剩余图片根据尺寸和优先级分配空间(pri*act)
def pdf_compress_by_priority(filename, ws, pathlist, prilist, targetsize,id):
    # todo 文件名转换
    outputpath = f'./src/temp2/{id}/'
    os.mkdir(outputpath)
    inputpath = f'./src/temp/{id}/'
    allstep = len(prilist) * 2
    step = 0
    # 计算总权重
    psnr = 23.0
    ssim = 0.87
    total_pri = 0
    index = 0
    imgpri = []
    ws.send("info:正在压缩图片")
    for i in prilist:
        imgpri.append(i * GetActSize(inputpath + pathlist[index]))
        total_pri += imgpri[index]
        index += 1
    index = 0
    for i in pathlist:
        rate = targetsize * prilist[index] / total_pri
        index += 1
        step += 1
        picCompress.compress_hybird(inputpath + i, outputpath + i, rate,eva=False)
        ws.send("reg:" + str(int(100 * step / allstep)))
    # 解析文件
    doc = fitz.open("./src/uploadfile/" +filename)
    imgcount = 0
    index = 0
    ws.send("info:正在生成文件")
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_replace(page, xref, filename=outputpath + pathlist[index])
            index += 1
            imgcount += 1
            step += 1
            ws.send("reg:" + str(int(100 * step / allstep)))
    sfn = './out/' + filename
    doc.ez_save(filename=sfn,garbage=4,clean=True,pretty=True)
    ws.send("info:文件压缩完成")
    # 清除文件
    shutil.rmtree(outputpath)
    return os.path.getsize(sfn) / 1024, 23, 0.9


# 测试pdf文件极限压缩
def pdf_compress_test(filename):
    fn = filename
    filename = 'src/' + filename
    # 获取文件总大小
    filesize = os.path.getsize(filename) / 1024
    doc = fitz.open(filename)
    pix_size = 0
    img_size = 0
    page_number = doc.page_count
    now_page = 0
    for page in doc.pages():
        imageList = page.get_images()

        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)

            # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            img = imgopen(new_name)
            pix_size += img.height * img.width * 3 // 1024
            img_size += os.path.getsize(new_name) / 1024
            page.delete_image(xref)
        now_page += 1
    doc.ez_save("src/temp/" + fn)
    emptypdf_size = os.path.getsize("src/temp/" + fn) // 1024
    print("图片绝对大小:", pix_size, "文件数据大小:", emptypdf_size, "图片文件大小:", img_size)
    # return filesize, img_size, pix_size, emptypdf_size
    for page in doc.pages():
        imageList = page.get_images()
        for imginfo in imageList:
            xref = imginfo[0]  # 获取图像的 xref
            image_info = doc.extract_image(xref)
            # 保存图像到文件
            new_name = f"./src/temp/image_{xref}.{image_info['ext']}"
            with open(new_name, "wb") as img_file:
                img_file.write(image_info["image"])
            jname = new_name.replace(new_name.split(".")[-1], 'jpg')
            picCompress.min_compress(new_name, jname)
            image_replace(page, xref, filename=jname)
            # pix_size += os.path.getsize(new_name)
    sfn = './out/' + os.path.basename(filename)
    doc.ez_save(filename=sfn)
    print(sfn, "最小文件大小:", os.path.getsize(sfn) // 1024)

# pdf_compress_test('ICML 2023.pdf')
