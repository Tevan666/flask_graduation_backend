from email.policy import default
from sqlalchemy import null
from exts import db
from datetime import datetime

# 创建Model

#购买历史记录表  
class Purchase_history(db.Model):
  __tablename__ = 'purchase_history'
  id = db.Column('id',db.Integer, primary_key=True, autoincrement=True, nullable=False)
  user_id = db.Column('user_id',db.String(5))
  purchase_time = db.Column('purchase_time',db.DateTime, nullable=False, default=datetime.now)
  available_time = db.Column('available_time',db.DateTime, nullable=False, default="9999-12-31 12:00:00")
  goods_id = db.Column('goods_id',db.String(50))

#商品表
class Goods(db.Model):
  __tablename__ = 'goods'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  type = db.Column(db.String(10), nullable=False)
  goods_id = db.Column(db.String(5))
  
#用户表
class Demo_Login_Users(db.Model):
  __tablename__ = 'demo_login_users'
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  userId = db.Column(db.String(50), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  phone = db.Column(db.String(50))
  password = db.Column(db.String(50))
  create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
  update_time = db.Column(db.DateTime)
  status = db.Column(db.Integer, nullable=False)
  square = db.Column(db.String(10))
  description = db.Column(db.String(255))
  balances = db.Column(db.Integer, nullable=False)
  email = db.Column(db.String(20))

#上传历史记录表
class Animal(db.Model):
  __tablename__ = 'animal'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  type = db.Column(db.String(50), nullable=False) 
  name = db.Column(db.String(50), nullable=False)
  status = db.Column(db.String(50), nullable=False)
  baike_url = db.Column(db.String(50))
  img_url = db.Column(db.String(50))
  userId = db.Column(db.String(5))
  upload_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
  description = db.Column(db.String(255), nullable=False)
  square = db.Column(db.String(15), nullable=True)
  province = db.Column(db.String(15), nullable = True)

