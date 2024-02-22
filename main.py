# -*-coding: UTF-8 -*-
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import utils.config as cfg
import utils.logger as log
import utils.comm as comm
import uuid
import inference
import struct

app = Flask(__name__)
loggers = log.Loggers()


@app.route('/')
def index():
    return cfg.appname


@app.route('/api/v1/uploadinfer', methods=['POST'])
def upload_file_infer():
    try:
        if request.method == 'POST':
            f = request.files.get('myfile')
            if f is None:
                return retRes(-1, 'file not found')

            loggers.debug('file content type = {} ,filename = {}'.format(f.content_type, f.filename))
            file_ext = os.path.splitext(f.filename)[1]
            flag = False
            for key in comm.ftypelist:
                if file_ext == key:
                    flag = True

            if flag is False:
                return retRes(-1, 'file content type no match')

            root_path = comm.comm.createDir(cfg.upfiles)

            filename = '{}.{}'.format(str(uuid.uuid4()), file_ext)
            filepath = os.path.join(root_path, secure_filename(filename))
            f.save(filepath)
            loggers.info('upload file {} success.'.format(filepath))
            pre = inference.predict(filepath)
            return retRes(0, 'success', pre)
        else:
            return retRes(-1, 'request method no match')
    except Exception as ex:
        loggers.error(ex)
        return retRes(-1, 'error')


@app.route('/api/v1/infer', methods=['POST'])
def img_infer():
    try:
        if not request.json or 'imgurl' not in request.json:
            return retRes(-1, 'request is not json or imgurl not in json')
        else:
            loggers.info("[img_infer] [post] request.json:{}".format(request.json))
            imgurl = request.json["imgurl"]
            loggers.info("[img_infer] [post] imgurl:{}".format(imgurl))
            pre = inference.predict(imgurl)
            return retRes(0, 'success', pre)
    except Exception as ex:
        loggers.error(ex)
        return retRes(-1, 'error')


def retRes(code, msg, data=None):
    return jsonify({"code": code, "data": data, "msg": msg})


if __name__ == '__main__':
    app.run(host=cfg.host, port=cfg.port, debug=cfg.debug)
