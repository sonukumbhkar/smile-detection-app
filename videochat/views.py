from django.shortcuts import render
import cv2
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseServerError
from django.views.decorators import gzip
import time
from django.http import HttpResponse


def index(request):
    
    return render(request,'index.html')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_smile.xml')

    

def get_frame():
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        _, frame = camera.read()
        frame= cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = detect(gray, frame)
        
        imencdode = cv2.imencode('.jpeg', image)[1]
        stringData = imencdode.tostring()
        yield(b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    camera.release()
    cv2.destroyAllWindows()

def detect(gray, frame):
    faces = face_cascade.detectMultiScale(gray, 1.8, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
            
        eye = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eye:
            cv2.rectangle(roi_color, (ex, ey), ((ex + ew), (ey + eh)), (0,255,0), 2)
    
            
    return frame


def dynamic_stream(request,stream_path='video'):
    try:
        return StreamingHttpResponse(get_frame(),content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        return "errror"
