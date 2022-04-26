from modals import Demo_Login_Users, Animal, Purchase_history, Goods
from exts import db
from flask import Blueprint, jsonify, request
from restApp import class_to_dict
history_bp = Blueprint('history_bp', __name__, url_prefix='/api/')


@history_bp.route('/mart', methods = ['GET', 'POST'])
def mart():
  #查询所有用户的功能
  history = db.session.query(Demo_Login_Users.name,Goods.type).filter(Demo_Login_Users.userId == Purchase_history.user_id).filter(Goods.goods_id == Purchase_history.goods_id).all()
  arr = []
  for row in history:
    data={}
    data['name']=row[0]
    data['type']=row[1]
    arr.append(data)
  return jsonify(status=200,data=arr)

@history_bp.route('/history', methods = ['GET', 'POST'])
def history():
  if(request.method == 'GET'):
    #查询所有用户的购买历史
    history = db.session.query(Purchase_history).all()
    return jsonify(status=200,data=class_to_dict(history))
  else:
    #购买商品
    goods = request.get_json()
    if(goods['userId']):
      user_id = goods['userId']
      goods_id = goods['goods_id']
      purchase = Purchase_history(user_id=user_id,goods_id=goods_id)
      exist_user = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.userId == user_id).all()
      exist_goods = db.session.query(Goods).filter(Goods.goods_id == goods_id).all()
      if(exist_user):
        if(exist_goods == []):
          return jsonify(code=1,message='不存在当前商品')
        exist_history = db.session.query(Purchase_history).filter(Purchase_history.user_id==user_id).filter(Purchase_history.goods_id==goods_id).all()
        if(exist_history):
          return jsonify(code=1,message='已拥有该功能')
        db.session.add(purchase)
        db.session.commit()
        return jsonify(code=0,message='购买成功')
      else:
        return jsonify(code=1,message='不存在当前用户')