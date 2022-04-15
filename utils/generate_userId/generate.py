import random

def general(): 
  origin_arr = []
  generate_arr = []
  #遍历5次，生成5个元素并插入列表origin_arr
  for i in range(5):
    origin_arr.append(random.randint(0,9))
    if (len(origin_arr) >= 5): 
      break
  #通过遍历将origin_arr的5个元素转为字符串并插入generate_arr
  for item in origin_arr:
    generate_arr.append(str(item))
  userId = ''.join(generate_arr)
  print(userId)

  return userId