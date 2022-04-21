import json
import re
from os.path import dirname, join
current_dir = dirname(__file__)
file_path = join(current_dir, "province.json")
with open(file_path, 'r', encoding="UTF-8") as load_file:
  json_obj = json.load(load_file)
# print(json_obj)
count="6"
square = "北京市"
for item in json_obj["features"]:
  if(item["properties"]["name"]!=''):
    if(re.findall(item["properties"]["name"], square)):
      item["properties"]["adcode"]=count