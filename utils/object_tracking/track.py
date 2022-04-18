from flask import Blueprint, request, jsonify, make_response, send_from_directory
import os
import glob 
import numpy as np
import re

import cv2

track_bp = Blueprint('track', __name__, url_prefix='/api/')

def resize(img):
  return cv2.resize(img,(512,512)) # arg1- input image, arg- output_width, output_height

def object_tracking(filepath):
  cap=cv2.VideoCapture(filepath)
  fourcc = cv2.VideoWriter_fourcc(*'MPEG')
  out = cv2.VideoWriter('output.avi',fourcc, 20.0, (1920,1080))

  ret,frame=cap.read()
  l_b=np.array([0,230,170])# lower hsv bound for red
  u_b=np.array([255,255,220])# upper hsv bound to red

  while ret & frame.any()!= None:
      ret,frame=cap.read()
      print(frame)
      hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
      mask=cv2.inRange(hsv,l_b,u_b)
      contours,_= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      max_contour = contours[0]
      for contour in contours:
        if cv2.contourArea(contour)>cv2.contourArea(max_contour):
          max_contour = contour

          approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
          x,y,w,h=cv2.boundingRect(approx)
          cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)

          M=cv2.moments(contour)

      cx=int(M['m10']//M['m00'])
      cy=int(M['m01']//M['m00'])
      cv2.circle(frame, (cx,cy), 3,(255,0,0),-1)
      out.write(frame)
      cv2.imshow("frame",resize(frame))

      key=cv2.waitKey(1)
      if key==ord('q') | frame.all() is None:
          break
  cv2.waitKey(0)
  cap.release()
  out.release()
  cv2.destroyAllWindows()
@track_bp.route('/trackfile', methods = ['POST'])
def trackfile():
  video_files = request.files.getlist('video')
   # 从文件列表依次取出并保存，文件名与上传时一致
  if not video_files:
        return jsonify({
            "code": -1,
            "message": "No upload images or videos."
        })

  for video_file in video_files:
      video_file.save(video_file.filename)
      filename=video_file.filename
  return jsonify({
        "code": 0,
        "message": "上传成功"
    })

@track_bp.route('/object_track', methods = ['POST'])
def object_track():
  test_dir = os.path.abspath(os.path.join(os.getcwd()))
  files = glob.glob(test_dir + '/' + "*.mp4")
  object_tracking(files[0])
  return jsonify(code=0, msg='成功生成检测视频')
  
def gen_frames(filepath):
    while True:
        cap=cv2.VideoCapture(filepath)
        ret,frame=cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@track_bp.route('/get_video', methods = ['GET'])
def get_video():
  test_dir = os.path.abspath(os.path.join(os.getcwd()))
  print(test_dir)
  files = glob.glob(test_dir + '/' + "*.avi")
  filename = re.sub(r'.+\/', '', files[0])
  print(filename)
  try:
      response = make_response(
          send_from_directory(test_dir, filename, as_attachment=True))
      return response
  except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


