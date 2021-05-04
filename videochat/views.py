from django.shortcuts import render
import cv2
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseServerError
from django.views.decorators import gzip
import time
from django.http import HttpResponse


def index(request):
    
    return render(request,'index.html')
    

def get_frame():
    camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while True:
        ret,img = camera.read()
        img= cv2.flip(img, 1)
        imencdode = cv2.imencode('.jpeg', img)[1]
        stringData = imencdode.tostring()
        yield(b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
    camera.release()
    cv2.destroyAllWindows()
def dynamic_stream(request,stream_path='video'):
    try:
        return StreamingHttpResponse(get_frame(),content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        return "errror"
