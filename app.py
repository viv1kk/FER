import io
import base64
from random import random
from flask import Flask, render_template, request, Response, send_file,jsonify
import cv2
import numpy as np
from PIL import Image

import face
 
app = Flask(__name__)

camera = cv2.VideoCapture(0)

def generate_frames():
    while(True):
        # read the camera frame
        success, frame = camera.read()
        if not success:
            break   
        else:
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/png\r\n\r\n'+frame+b'\r\n') 
        yield(frame) 


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

@app.route('/', methods = ['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/send', methods = ['POST','GET'])
def send():

    #getting the data in byte64
    data = request.data
    # print(data)
    #converted the data in image
    img = stringToImage(data)
    #converted to opencv compatible image
    img = toRGB(img)
    img = face.compareImagefromKnownFaces(img)
    # print(a)
    # cv2.imshow("", img)
    # cv2.waitKey(0)
    # cv2.destroyWindow(img)
    r, img = cv2.imencode('.png', img)
    img = base64.b64encode(img)
    return Response(img, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)

