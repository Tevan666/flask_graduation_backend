# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText # 构建邮件文本
from email.header import Header # 发送内容
import random
import string
from modals import Demo_Login_Users, Animal, Purchase_history, Goods
from exts import db
from flask import Blueprint, jsonify, request
from restApp import class_to_dict
send_bp = Blueprint('send_bp', __name__, url_prefix='/api/')


def general(): 
  code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
  return code
def send(title,code):
  sender = '1759377257@qq.com' # 发送方
  receivers = ['1759377257@qq.com']  # 接收邮件,可设置为你的QQ邮箱或者其他邮箱

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

@send_bp.route('/send', methods = ['GET', 'POST', 'DELETE'])
def register(): 
  code = general()
  send('邮箱注册',code)
  return jsonify(code=0,message='邮件发送成功')

