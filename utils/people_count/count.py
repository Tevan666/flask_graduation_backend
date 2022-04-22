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


current_dir = dirname(__file__)
file_path = join(current_dir, "province.json")
with open(file_path, 'r', encoding="UTF-8") as load_file:
  json_obj = json.load(load_file)

@count_bp.route('/count', methods = ['GET'])
def count():
  animals = db.session.query(Animal.province, func.count(Animal.province)).group_by(Animal.province).all()
  print(animals)
  for row in animals:
    for item in json_obj["features"]:
      if(item["properties"]["name"]!=''):

        if(re.findall(item["properties"]["name"], row[0])):
          item["properties"]["adcode"]=row[1]
        else:
          item["properties"]["adcode"]=0
  return json_obj
