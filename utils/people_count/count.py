from flask import Blueprint, request, jsonify, make_response, send_from_directory
import json
import re
from os.path import dirname, join
from modals import Animal
from exts import db
from restApp import class_to_dict
from sqlalchemy import func
import numpy as np

count_bp = Blueprint('count', __name__, url_prefix='/api/')

num = [
    {
      "name": '云南省',
      "code": 530000,
      "value": 0
    },
    {
      "name": '黑龙江省',
      "code": 230000,
      "value": 0
    },
    {
      "name": '贵州省',
      "code": 520000,
      "value": 0
    },
    {
      "name": '北京市',
      "code": 110000,
      "value": 0
    },
    {
      "name": '河北省',
      "code": 130000,
      "value": 0
    },
    {
      "name": '山西省',
      "code": 140000,
      "value": 0
    },
    {
      "name": '吉林省',
      "code": 220000,
      "value": 0
    },
    {
      "name": '宁夏回族自治区',
      "code": 640000,
      "value": 0
    },
    {
      "name": '辽宁省',
      "code": 210000,
      "value": 0
    },
    {
      "name": '海南省',
      "code": 460000,
      "value": 0
    },
    {
      "name": '内蒙古自治区',
      "code": 150000,
      "value": 0
    },
    {
      "name": '天津市',
      "code": 120000,
      "value": 0
    },
    {
      "name": '新疆维吾尔自治区',
      "code": 650000,
      "value": 0
    },
    {
      "name": '上海市',
      "code": 310000,
      "value": 0
    },
    {
      "name": '陕西省',
      "code": 610000,
      "value": 0
    },
    {
      "name": '甘肃省',
      "code": 620000,
      "value": 0
    },
    {
      "name": '安徽省',
      "code": 340000,
      "value": 0
    },
    {
      "name": '香港特别行政区',
      "code": 810000,
      "value": 0
    },
    {
      "name": '广东省',
      "code": 440000,
      "value": 0
    },
    {
      "name": '河南省',
      "code": 410000,
      "value": 0
    },
    {
      "name": '湖南省',
      "code": 430000,
      "value": 0
    },
    {
      "name": '江西省',
      "code": 360000,
      "value": 0
    },
    {
      "name": '四川省',
      "code": 510000,
      "value": 0
    },
    {
      "name": '广西壮族自治区',
      "code": 450000,
      "value": 0
    },
    {
      "name": '江苏省',
      "code": 320000,
      "value": 0
    },
    {
      "name": '澳门特别行政区',
      "code": 820000,
      "value": 0
    },
    {
      "name": '浙江省',
      "code": 330000,
      "value": 0
    },
    {
      "name": '山东省',
      "code": 370000,
      "value": 0
    },
    {
      "name": '青海省',
      "code": 630000,
      "value": 0
    },
    {
      "name": '重庆市',
      "code": 500000,
      "value": 0
    },
    {
      "name": '福建省',
      "code": 350000,
      "value": 0
    },
    {
      "name": '湖北省',
      "code": 420000,
      "value": 0
    },
    {
      "name": '西藏自治区',
      "code": 540000,
      "value": 0
    },
    {
      "name": "台湾省",
      "code": 710000,
      "value": 0
    },
  
]

@count_bp.route('/count', methods = ['GET'])
def count():
  animals = db.session.query(Animal.province, func.count(Animal.province)).group_by(Animal.province).all()
  for row in animals:
    for item in num:
      if(re.findall(item['name'], row[0])):
        item['value'] = row[1]
  return jsonify(status=200,data=num)
