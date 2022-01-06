from wsgiref.simple_server import make_server

from flask import Flask
from flask import jsonify
from flask import request

from gevent import pywsgi

from predict import Predictor

import pandas as pd
import numpy as np
import json

app = Flask(__name__)


@app.route('/api/air_conditioning_detection/', methods=['GET', 'POST'])
def air_conditioning_detection():
    """
    空调负荷检测接口，GET，返回此图片上的异常是那种类别
    """
    # 获取用户上传的空调数据
    # 解析传来的json数据中空调数据字符串内容
    air_datas = request.json["air_data"]
    air_dic = {}
    for i, air_data in enumerate(air_datas):
        air_dic[i] = air_data

    # 转化为DataFrame
    air_df = pd.DataFrame(air_dic, dtype=float).T

    # 使用三种数据分别进行预测，并返回是否报警的数据
    result_json = []
    data_type_list = ['electricCurrent', 'activePower', 'apparentPower']
    thresh = [0.14927437, 0.11817348, 0.0900907]
    # , 'activePower', 'apparentPower'
    for i, data_type in enumerate(data_type_list):
        model = Predictor(
            data_type=data_type,
            data_time=30,
            thresh=thresh[i],
            pd=air_df
        )
        y_pred, _ = model.predict()
        result_json.append(y_pred)

    is_air = max(result_json, key=result_json.count)
    # print("isAlarm: ", False if is_air else True)


    res = {
            "isok": True,                           # 操作结果  服务端返回正常true 异常为false
            "equipmentType": "KT",                  # 设备类型  KT 代表空调 其他自定义
            "isAlarm": False if is_air else True,   # 是否告警
            "matchingDegree": 0,                    # 匹配度 如果有就带过来, 没有就是0
            "errmsg": 200                           # isok 为false时这里说明错误的原因
    }

    # 返回json数据
    return jsonify(res)


if __name__ == '__main__':
    # from utils import openpic
    # ip, newPort = openpic()
    server = pywsgi.WSGIServer(('::', 80), app)
    server.serve_forever()
    app.run()
    