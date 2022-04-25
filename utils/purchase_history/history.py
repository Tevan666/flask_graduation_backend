from modals import Demo_Login_Users, Animal, Purchase_history, Goods
from exts import db
from flask import Blueprint, jsonify
from restApp import class_to_dict
history_bp = Blueprint('history_bp', __name__, url_prefix='/api/')


@history_bp.route('/history', methods = ['GET', 'POST'])
def history():
  history = db.session.query(Demo_Login_Users.name,Goods.type).filter(db.and_(Demo_Login_Users.userId == Purchase_history.user_id and Goods.goods_id == Purchase_history.goods_id))
  arr = []
  print(history)
  for row in history:
    data={}
    data['name']=row[0]
    data['type']=row[1]
    arr.append(data)
  return jsonify(data=arr)
