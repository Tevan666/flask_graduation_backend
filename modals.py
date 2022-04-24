from sqlalchemy import null
from exts import db
from datetime import datetime

# 创建Model

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

#商品表
class goods(db.Model):
  __tablename__ = 'goods'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  type = db.Column(db.String(10), nullable=False)
  goods_id = db.Column(db.String(5))

#购买历史记录表  
class purchase_time(db.Model):
  __tablename__ = 'purchase_time'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  user_id = db.Column(db.String(5), db.ForeignKey('Demo_Login_Users.userId'), primary_key=True) #外键，用户表userid
  purchase_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
  available_time = db.Column(db.DateTime, nullable=False)
  goods_id = db.Column(db.String(50), db.ForeignKey('goods.goods_id'), primary_key=True ) #外键，商品表goods_id