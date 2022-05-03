import json
import cv2
import numpy as np
import base64
#状态码集
RESULTS={
    200:{'code':200,'msg':'success'},
    400:{'code':400,'msg':'require paremeter'}
}
"""
   describe:指定请求数据的必需格式
   args：无
   return：指定数据形式(dict类型)
"""
def get_require_data():
    request_type={
      #值为false的key，代表该key没有子key
      'type':False,
      'data':False,
    }
    return request_type
"""
   describe:指定返回数据的格式
   args：无
   return：指定数据形式（dict类型）
"""
def get_result_model():
   return {
      'code':'',
      'msg':'',
      'data':{},
      'cost_time':0
       }
"""
   describe:判断请求数据是否符合项目所指定的数据形式
   args：require _data,指定请求数据的必须附带的参数，data，请求的数据
   return:若请求数据合法，则返回数据（dict类型），若不合法，则返回False（Boolean类型）
"""
def is_valid_json(require_data,data):
  try:
      data=json.loads(data)
      tag=True
      for key in require_data:
        if key in data.keys():
           if require_data[key]!=False:
               tag=is_valid_json(require_data[key],data[key])
        else:
               return False
        if not tag:
               return False
      return data
  except:
         return False
"""
    describe:包装返回的响应数据格式
    args：data,返回的主要数据(dict类型)
          cost_time,调用检测函数所耗时间(int类型)
    return:指定数据形式(dict类型)
"""
def result_data(data,cost_time=0):
    result=get_result_model()
    result['msg']=RESULTS[200]['msg']
    result['code']=RESULTS[200]['code']
    result['data']=data
    result['cost_time']=cost_time
    return result
"""
    describe:包装返回的错误响应格式
    args：无
    return:状态和提示语（dict类型）
"""
def wrong_request(code):
    return RESULTS[code]

"""
   describe:将base64格式图片数据转化为numpy.ndarray格式
   args：base64_data,base64格式图片数据
   return:numpy.ndarray格式数据
"""


def base64_2_array(base64_data):
    im_data = base64.b64decode(base64_data) #经过base64编码的bytes-like对象或者ASCII字符串进行解码
    im_array = np.frombuffer(im_data, np.uint8) # 将缓冲区解释为一维数组
    im_array = cv2.imdecode(im_array, cv2.COLOR_RGB2BGR) #从指定的内存缓存中读取数据，并把数据转换 (解码)成图像格式;主要用于从网络传输数据中恢复出图像。 
    return im_array
