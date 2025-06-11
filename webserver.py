import json
import time
import uuid

from flask import Flask, send_from_directory, request, jsonify, send_file, make_response, Response
from flask_cors import CORS
import os
from flask_socketio import SocketIO, send
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from pdfHandler import *
from picCompress import compress_by_quality

app = Flask(__name__)
CORS(app)
sockets = Sockets(app)
# 设置要托管的文件夹路径
UPLOAD_FOLDER = './src/webfile'
webSocket_list = {}

import shutil


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


@app.route('/<filename>')
def serve_file(filename):
    print(filename)
    # 检查文件是否存在
    if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        return "File not found", 404


@app.route('/')
def main_page():
    # 检查文件是否存在
    if os.path.isfile(os.path.join(UPLOAD_FOLDER, 'index.html')):
        return send_from_directory(UPLOAD_FOLDER, 'index.html')
    else:
        return "File not found", 404


@app.route('/<path:subpath>')
def show_file(subpath):
    print(subpath)
    return send_from_directory(UPLOAD_FOLDER, subpath)


IMAGES_FOLDER = './src/webfile/images'


@app.route('/images/<filename>')
def serve_images(filename):
    # 检查文件是否存在
    if os.path.isfile(os.path.join(IMAGES_FOLDER, filename)):
        return send_from_directory(IMAGES_FOLDER, filename)
    else:
        return "File not found", 404


PDFIMG_FOLDER = './src/temp/'


@app.route('/pdfimg/<filename>')
def serve_pdf_images(filename):
    # 检查文件是否存在
    id = request.args.get('id')
    print(id)
    if os.path.isfile(os.path.join(PDFIMG_FOLDER+id, filename)):
        return send_from_directory(PDFIMG_FOLDER+id, filename)
    else:
        return "File not found", 404


# 设置上传文件的保存路径
PDF_FOLDER = './src/uploadfile'
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "没有文件上传"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "未选择文件"}), 400

    # 保存文件到指定路径
    # 生成唯一文件名
    pdfname = str(uuid.uuid4()) + '.pdf'
    file_path = os.path.join(PDF_FOLDER, pdfname)
    file.save(file_path)

    # todo 调用文件解析处理程序,由ws返回进度

    return jsonify({"message": f"文件 {file.filename} 上传成功！", "filename": pdfname}), 200


@app.route('/reqtest')
def reqtest():
    index=request.args.get('index')
    strat=time.time()
    compress_by_quality(f"src/Kodak-Lossless-True-Color-Image-Suite-master/Image_jpeg/{index}.jpg",
                        f"out/out{index}.jpg", 85)
    end=time.time()
    return jsonify({"start": strat, "end": end,"index":index}), 200


# 启动文件解析请求
@app.route('/parsefile')
def parsefile():
    uid = request.args.get('uid')
    filename = request.args.get('filename')
    t, p, picsize, esize = parse_pdf_file(webSocket_list[uid], filename)
    return jsonify({"message": f"完成解析", "filesize": t, "imgsize": p, "imgact": picsize, "emptysize": esize}), 200


# 启动文件图片解析请求
@app.route('/parseimage')
def parseimage():
    uid = request.args.get('uid')
    filename = request.args.get('filename')
    t, p, picsize, esize, imglist = parse_pdf_image(webSocket_list[uid], filename,uid)
    data = {"message": f"完成解析", "filesize": t, "imgsize": p, "imgact": picsize, "emptysize": esize,
            "imagelist": imglist}
    return Response(json.dumps(data), mimetype='application/json')


# 启动定率压缩解析请求
@app.route('/compressfile')
def compressfile():
    uid = request.args.get('uid')
    filename = request.args.get('filename')
    compressrate = int(float(request.args.get("compressrate")))
    print(uid, filename, compressrate)
    # pdf_compress("./src/uploadfile/"+filename, webSocket_list[uid],1.0-(int(compressrate) / 100))
    s, psnr, ssim = pdf_compress_by_quality("./src/uploadfile/" + filename, webSocket_list[uid], compressrate)
    return jsonify({"message": f"完成压缩", "size": s, "PSNR": psnr, "SSIM": ssim}), 200


# 启动定向压缩解析请求
@app.route('/compresstosize')
def compressfilebysize():
    uid = request.args.get('uid')
    filename = request.args.get('filename')
    compressrate = int(float(request.args.get("compressrate")))
    maxfilesize = float(request.args.get("maxsize"))
    imgrate = float(request.args.get("imgrate"))
    empty = float(request.args.get("emptysize"))
    limit=float(request.args.get("target"))
    mostcount=3
    onssim=False
    if request.args.get("ssimon")=='true':
        onssim=True
    s, psnr, ssim=(0,0,0)
    while mostcount>0:
        s, psnr, ssim = pdf_compress_by_size2(filename, webSocket_list[uid], compressrate=imgrate,ssimon= onssim)
        if s<limit:
            break
        else:
            mostcount-=1
            imgrate=imgrate*0.95
    if not onssim:
        ssim='未计算'
    if s > limit:
        return jsonify({"message": f"notget", "size": s, "PSNR": psnr, "SSIM": ssim}), 200
    return jsonify({"message": f"完成压缩", "size": s, "PSNR": psnr, "SSIM": ssim}), 200


@app.route('/compresstopsnr')
def compressfiletopsnr():
    uid = request.args.get('uid')
    filename = request.args.get('filename')
    psnr = float(request.args.get("psnr"))
    onssim=False
    if request.args.get("ssimon")=='true':
        onssim=True
    s, psnr, ssim = pdf_compress_by_psnr(filename, webSocket_list[uid], psnr,onssim=onssim)
    if not onssim:
        ssim='未计算'
    return jsonify({"message": f"完成压缩", "size": s, "PSNR": psnr, "SSIM": ssim}), 200


@app.route('/compresstoimage', methods=['POST'])
def compressfiletoimage():
    uid = request.json.get('uid')
    filename = request.json.get('filename')
    imgpath = request.json.get('imgurl')
    priority = request.json.get('priority')
    limit = float(request.json.get("maxsize"))
    mostcount = 5
    targetsize = request.json.get('maxsize') - request.json.get('emptysize')
    s, psnr, ssim = (0, 0, 0)
    while mostcount > 0:
        s, psnr, ssim = pdf_compress_by_priority(filename, webSocket_list[uid], imgpath, priority,targetsize,uid)
        if s<limit:
            break
        else:
            mostcount-=1
            print(targetsize,s)
            targetsize=targetsize*0.8
    if s>limit:
        return jsonify({"message": f"notget", "size": s, "PSNR": '未计算', "SSIM": '未计算'}), 200
    return jsonify({"message": f"完成压缩", "size": s, "PSNR": '未计算', "SSIM": '未计算'}), 200


@app.route('/download', methods=['GET'])
def download_file():
    # 指定文件的路径
    filename = request.args.get('name')
    file_path = "./out/" + filename  # 替换为实际文件路径
    # 发送文件
    return send_file(file_path, download_name=filename, as_attachment=True)


@app.route('/delfile', methods=['DELETE'])
def delete_file():
    # 指定文件的路径
    filename = request.args.get('filename')
    loc = request.args.get('loc')
    # print(filename,loc)
    if loc == "input":
        path = "./src/temp/" + filename
        if os.path.exists(path):
            os.remove(path)
        path = "./src/uploadfile/" + filename
        if os.path.exists(path):
            os.remove(path)
    path = "./out/" + filename
    if os.path.exists(path):
        os.remove(path)
    # 发送文件
    return jsonify({"message": "delete success", "filename": filename, "loc": loc}), 200


@sockets.route('/ws')
def echo_socket(ws):
    uid = str(uuid.uuid4())
    webSocket_list[uid] = ws
    while not ws.closed:
        now = "id:" + uid
        ws.send(now)  # 发送数据
        print("收到了连接", ws)
        msg = ws.receive()
        print(msg)
    # todo 清理产生的文件
    print("websocket连接已经断开",uid)
    webSocket_list.pop(uid)
    shutil.rmtree(f'./src/temp/{uid}/')


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=5000)
    clear_folder("./src/uploadfile")
    clear_folder("./src/temp")
    clear_folder("./src/temp2")
    clear_folder("./temp")
    clear_folder("./out")
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()
