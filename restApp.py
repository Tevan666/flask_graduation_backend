# -*- coding: UTF-8 -*-
from email import message
import json
from lib2to3.pgen2 import token
import re
import numbers
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer, String
from collections import Iterable
from modals import Demo_Login_Users, Animal
#restful
from flask_restful import Resource, Api
#导入配置
from utils.generate_userId.generate import general
import config
#导入蓝图
from common.bp_captcha import bp
from furl import furl
import rpa as r
# app.py 添加
from exts import db
# db绑定app
# app.py
from flask import Blueprint, make_response
from utils.captcha import Captcha
from utils.create_token.create_token import create_token, verify_token
from io import BytesIO
import json

api_bp = Blueprint('api', __name__, url_prefix='/api/')

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

@api_bp.route('/welcome')
def welcome():
    name = request.values.get('name')
    r.init()
    r.url('https://image.baidu.com/')
    r.type('//*[@id="kw"]', name)
    r.type('//*[@id="kw"]','[enter]')
    r.wait(2)
    r.snap('page', 'results.png')
    return 'hello'

@api_bp.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        userId = general()
        id = request.values.get('id')
        user = request.values.get('username')
        passwd = request.values.get('passwd')
        phone = request.values.get('phone')
        User = Demo_Login_Users(id=id,userId=userId,name=user, phone=phone, password= passwd, status=0, balances=0)
        print(User)
        db.session.add(User)
        db.session.commit()
        return jsonify(code=0, message="注册成功")
      
@api_bp.route('/user_info', methods = ['GET', 'POST', 'DELETE'])
def user():
    token = request.headers["token"]
    userId = verify_token(token)
    queryUser = db.session.query(Demo_Login_Users).filter(db.and_(Demo_Login_Users.userId == userId)).first()

    if request.method == 'GET':
        userInfo = class_to_dict(queryUser)
        return jsonify(status=200, data=userInfo)
    elif request.method == 'POST': 
        audit_info = request.get_json()
        if(userId):
            queryUser = db.session.query(Demo_Login_Users).filter(db.and_(Demo_Login_Users.userId == userId)).first()
            username = audit_info['username']
            square = audit_info['square']
            description = audit_info['description']
            if(username):
                queryUser.name = username
            if(square):
                queryUser.square = square
            if(description):
                queryUser.description = description
            db.session.commit()
            return jsonify(code=0,message='修改成功')
        else:
            return jsonify(code=1,message='不存在此用户!')
    elif request.method == 'DELETE':
        db.session.delete(queryUser)
        db.session.commit()


@api_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.values.get('username')
        email = request.values.get('email')
        phone = request.values.get('phone')
        passwd = request.values.get('password')
        code = request.values.get('code')
        #try:
        queryAccount = db.session.query(Demo_Login_Users).filter(db.or_(Demo_Login_Users.name == user,Demo_Login_Users.email == email, Demo_Login_Users.phone == phone )).filter(Demo_Login_Users.password == passwd).first()
        with open('temp.json', 'r') as f:
            temp = f.read()
        #print(type(q1))
        #print(q1 != None)
        
        if queryAccount != None:
          if code.lower() == json.loads(temp):
            account_info = class_to_dict(queryAccount)
            if account_info.get('userId'):
              token = create_token(account_info['userId'])
              return jsonify(code=0,token=token)
          else:
            return jsonify(code=1,message="验证码错误")

        else:
            return jsonify(code=1,message="账号或密码错误")

# 两把钥匙
client_id = 'b4a6925a59570ab8a4ca'
client_secret = '065deb294c29841f8d122603656103d7140ed0dd'
# github登录路由
@api_bp.route('/redirect_github/')
def redirect_github():
    url = 'https://github.com/login/oauth/authorize'
    params = {
        'client_id' : client_id,
        'scope': 'read:user',
        'allow_signup': 'true'
    }
    url = furl(url).set(params)
    print(url)
    return redirect(url.url, 302)