# -*- coding: UTF-8 -*-
import json
import numbers
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer, String
from collections import Iterable
from modals import Demo_Login_Users, Animal
#导入配置
from utils.generate_userId.generate import general
import config
#导入蓝图
from common.bp_captcha import bp
from furl import furl
import rpa as r
from restApp import api_bp
# app.py 添加
from exts import db
# db绑定app
# app.py

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(bp)
app.register_blueprint(api_bp)

def class_to_dict(obj):
    
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            a = o.__dict__
            if "_sa_instance_state" in a:
                del a['_sa_instance_state']
            dict.update(a)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        a = obj.__dict__
        if "_sa_instance_state" in a:
            del a['_sa_instance_state']
        dict.update(a)
        return dict

@app.route('/')
def hello_world():
   return 'Hello World'


if __name__ == '__main__':
   app.run(port = 5500,debug=True)