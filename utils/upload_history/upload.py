from modals import Demo_Login_Users, Animal, Purchase_history, Goods
from exts import db
from flask import Blueprint, jsonify, request
from restApp import class_to_dict
from sqlalchemy import func

upload_bp = Blueprint('upload_bp', __name__, url_prefix='/api/')


@upload_bp.route('/upload', methods = ['GET', 'POST', 'DELETE'])
def upload():
  name = request.values.get('name')
  status = request.values.get('status')
  type = request.values.get('type')
  per_page = int(request.values.get("pageSize") or 10)
  page = int(request.values.get("current") or 1)
  userId = request.headers.get('userId')
  square = request.values.get('square')
  access = request.values.get('access')
  if(square!=None ):
    if("省" in square):
            province = square.split("省")[0] + '省'
    else:
            province = square
  if request.method == 'GET':
       if(access == 'true'):
         group = db.session.query(Animal.userId,func.count(Animal.userId)).group_by(Animal.userId).all()
         user_group = []
         for row in group:
           queryname = db.session.query(Demo_Login_Users.name).filter(Demo_Login_Users.userId == row[0]).all()
           for item in queryname:
             data = {'username': item[0], 'value': row[1]}
             user_group.append(data)
         animals = db.session.query(Animal).all()
         count = db.session.query(Animal).count()
         animals_dict = class_to_dict(animals)
         return jsonify(status=200, data=animals_dict, total=count,group=user_group)
       if(name):
         animals = db.session.query(Animal).filter(db.and_(Animal.name == name,Animal.userId == userId)).all()
         count = db.session.query(Animal).filter(db.and_(Animal.type == type,Animal.userId == userId)).count()
         animals_dict = class_to_dict(animals)
         return jsonify(status=200, data=animals_dict, total=count)
       if(type):
         animals = db.session.query(Animal).filter(db.and_(Animal.type == type,Animal.userId == userId)).all()
         count = db.session.query(Animal).filter(db.and_(Animal.type == type,Animal.userId == userId)).count()
         animals_dict = class_to_dict(animals)
         return jsonify(status=200, data=animals_dict, total=count)
       if(page == None): 
         animals = db.session.query(Animal).filter(db.and_(Animal.userId == userId)).all()
         count = db.session.query(Animal).filter(db.and_(Animal.userId == userId)).count()
         print(count)
         animals_dict = class_to_dict(animals)
         return jsonify(status=200, data=animals_dict, total=count)
       if(per_page):
         count = db.session.query(Animal).filter(db.and_(Animal.userId == userId)).count()
         total = db.session.query(Animal).filter(db.and_(Animal.userId == userId)).paginate(page=page,per_page=per_page)
         obj_res = class_to_dict(total.items)
         return jsonify(status=200, data=obj_res,total=count)

       animals = db.session.query(Animal).filter(db.and_(Animal.userId == userId)).limit(per_page).offset((page-1) * per_page).all()
       count = db.session.query(Animal).filter(db.and_(Animal.userId == userId)).limit(per_page).offset((page-1) * per_page).count()
       
       animals_dict = class_to_dict(animals)
       return jsonify(status=200, data=animals_dict, total=count)
  elif(request.method == 'POST'):
       description = request.values.get('description')
       if("省" in square):
           province = square.split("省")[0] + '省'
       else:
           province = square
       baike_url = request.values.get('baike_url')
       type = request.values.get('type')
       img_url = request.values.get('img_url')
       upload = Animal(userId=userId, name=name, baike_url=baike_url, status = status, img_url=img_url, type=type, square=square, province=province, description=description)
       db.session.add(upload)
       db.session.commit()
       return jsonify(code=0, message='上传成功')

  elif(request.method == 'DELETE'):
       id = request.values.get('id')
       delete_history = Animal.query.get(id)
       if(delete_history):
         db.session.delete(delete_history)
         db.session.commit()
         return jsonify(code=0, message='删除成功')
       else:
          return jsonify(code=1, message='不存在此条记录')


@upload_bp.route('/recharge', methods = ['PUT'])
def recharge():
  userId = request.headers["userId"]
  amount = request.values.get('amount')
  current_user = class_to_dict(db.session.query(Demo_Login_Users).filter(Demo_Login_Users.userId == userId).first())
  new_balances = int(float(amount))  + current_user['balances']
  print(new_balances)

  update_balances = db.session.query(Demo_Login_Users).filter(Demo_Login_Users.userId == userId).update({'balances': new_balances})
  db.session.commit()
  return jsonify(code=0,message='修改成功')