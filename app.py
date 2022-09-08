
import json
from flask import Flask, render_template, request, Response, send_file,jsonify
import cv2
 
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


# def getCapture():
#         # read the camera frame
#         success, frame = camera.read()
#         if success:
#             print("shjasfhj")
#             # x, frame = cv2.imencode('.jpg', frame)
#             # cv2.imshow("", frame)
#             # cv2.imshow("", frame)
#             # cv2.waitKey(0)
#             # cv2.destroyWindow(frame)

#             return frame

@app.route('/', methods = ['POST','GET'])
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/Click', methods = ['POST','GET'])
# def snapshot():
#     img = getCapture()

#     # x, img = cv2.imencode('.jpg', img)
#     list = img.tolist()
#     # list = [1,2,3,4]
#     return jsonify(list)

@app.route('/send', methods = ['POST','GET'])
def send():
    return Response("hELLo")


if __name__ == "__main__":
    app.run(debug=True)

