# -*- coding: utf-8 -*-
from cmath import log
import smtplib
from email.mime.text import MIMEText # 构建邮件文本
from email.header import Header # 发送内容
import random
import string
from restApp import class_to_dict
from modals import Demo_Login_Users, Animal, Purchase_history, Goods
from exts import db
from flask import Blueprint, jsonify, request
from utils.generate_userId.generate import general
from urllib.parse import unquote
from utils.create_token.create_token import create_token

send_bp = Blueprint('send_bp', __name__, url_prefix='/api/')

email=''
def general_code(): 
  code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
  return code

def send_email(title,code,email):
  sender = '1759377257@qq.com' # 发送方
  receivers = [email]  # 接收邮件,可设置为你的QQ邮箱或者其他邮箱

  # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
  message = MIMEText('您的验证码为' + code, 'plain', 'utf-8')
  message['From'] = Header("物体分类平台", 'utf-8')     # 发送者
  message['To'] =  Header("用户", 'utf-8')      # 接收者
  subject = title
  message['Subject'] = Header(subject, 'utf-8')

  pwd = 'vlrigiptrbgadehg' # 邮箱授权码
  smtpObj = smtplib.SMTP('smtp.qq.com') # 链接服务器
  smtpObj.login(sender, pwd) # 登录发送方邮箱
  smtpObj.sendmail(sender, receivers, message.as_string()) # 发送邮件

code= ''
@send_bp.route('/bind', methods = ['PUT'])
def bind_email():
  email = request.values.get('email')
  userId = request.headers.get('userId')

  exist_account = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.userId == userId).first()
  if(exist_account):
    update_email = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.userId == userId).update({'email': email})
    db.session.commit()
    return jsonify(code=0,message='绑定成功')
  else:
    return jsonify(code=1,message='不存在此账号!')

@send_bp.route('/send', methods = ['GET'])
def send(): 
  type = request.values.get('type')
  global email
  email = request.values.get('email')
  if type == 'register':
    title = '邮箱注册'
  elif type == 'update':
    title = '修改密码'
  else:
    title = '登录'
  global code 
  code = general_code()
  send_email(title,code,email)
  return jsonify(code=0,message='邮件发送成功')

@send_bp.route('/email_regist', methods = ['POST'])
def register():
  userId = general()
  id = request.values.get('id')
  user = request.values.get('username')
  passwd = request.values.get('passwd')
  phone = request.values.get('phone')
  access_code = request.values.get('code')
  if(access_code == code):
    User = Demo_Login_Users(id=id,userId=userId,name=user, phone=phone, password= passwd, status=0, balances=0)
    db.session.add(User)
    db.session.commit()
    return jsonify(code=0,message='注册成功')
  else:
    return jsonify(code=1,message='验证码不正确!')


@send_bp.route('/update_password', methods = ['PUT'])
def update():
  access_code = request.values.get('code')
  new_password = request.values.get('password')
  if(access_code == code.lower()):
    exist_account = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.email == email).first()
    if(exist_account):
      update_password = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.email == email).update({'password': new_password})
      db.session.commit()
      return jsonify(code=0,message='修改成功')
    else: 
      return jsonify(code=1,message='不存在此账号!')
  else:
    return jsonify(code=1,message='验证码不正确!')

@send_bp.route('/email_login', methods = ['POST'])
def login():
  access_code = request.values.get('code')
  login_email = request.values.get('login_email')
  if(access_code == code.lower()):
    exist_account = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.email == login_email).first()
    if(exist_account):
      account_info = class_to_dict(exist_account)
      token = create_token(account_info['userId'])
      return jsonify(code=0,token=token)
    else: 
      return jsonify(code=1,message='不存在此账号!')
  else:
    return jsonify(code=1,message='验证码不正确!')