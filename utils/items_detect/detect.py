import json
from flask import Blueprint
from flask import request
from utils.items_detect.result_views_util import *
from utils.items_detect.result_views_util import base64_2_array
from utils.items_detect.predect import pred  # 导入检测函数

from utils.items_detect.result_views_util import is_valid_json, get_require_data, result_data, wrong_request

detect_bp = Blueprint('detect_bp', __name__,url_prefix='/api/')


@detect_bp.route('/detect', methods=['GET', 'POST'])
def main_detect():
    # 1.获取请求数据并判断数据是否合法
    request_data = request.get_data()
    data = is_valid_json(get_require_data(), request_data)
    #print(data)
    if data:
        # 2.解析请求数据
        data = base64_2_array(data['data'])

        # 调用检测函数，传入解析完毕的请求数据，并获取调用检测函数返回的结果
        result = pred(data)
        response = result_data({'result_type': int(result)})
        return json.dumps(response)
    else:
        return json.dumps(wrong_request(400))
