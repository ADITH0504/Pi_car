import cv2 # --- importing the file for video streaming---
from  flask import Flask,Response, request # --- import flask, response, request for web hosting
import serial # --- import serial communication for pi - arduino communication
 

# ------- INITIALIZE SERIAL COMMUNICATION AND VIDEO ------

ser = serial.Serial('/dev/ttyUSB0', 9600) # --- this is for serial communication between pi and arduino, make sure to change the port if needed
cap = cv2.VideoCapture(0)

# ------- CAMERA READ ------

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# --------- HOSTING THE WEB PAGE ------

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title> RC CAR LIVE CONTROL </title>
    </head>
    <body>
         </h1>RC CAR LIVE CONTROL</h1>
         <img src = "/video" width="500">

        <button
        onmousedown="send('F')"
        onmouseup = "send('S')"
        ontouchstart="send('F')"
        ontouchend = "send('S')" >
        Forward
        </button>

       <br><br>

        <button
        onmousedown="send('B')"
        onmouseup = "send('S')"
        ontouchstart="send('B')"
        ontouchend = "send('S')" >
        Backward
        </button>

        <br><br>

        <button
        onmousedown ="send('L')"
        onmouseup   = "send('S')"
        ontouchstart="send('L')"
        ontouchend  = "send('S')" >
        Left
        </button>

        <br><br>

        <button
        onmousedown="send('R')"
        onmouseup = "send('S')"
        ontouchstart="send('R')"
        ontouchend = "send('S')" >
        Right
        </button>

        <button
        onmousedown="send('S')"
        onmouseup = "send('S')"
        ontouchstart="send('S')"
        ontouchend = "send('S')" >
        Stop
        </button>
        
        <script>
        function send(cmd) {
              fetch ('/command?cmd=' + cmd);
        }
        </script>
    </body>
    </html>

    '''

@app.route('/command')
def command():
    cmd = request.args.get('cmd')
    print("command Recievd", cmd)

    ser.write((cmd + "\n").encode()) # --- DATA COMMNUNICATION - ARDUINO, "cmd" is the command received from the web page, and it is sent to the arduino through serial communication, make sure to handle this command in the arduino code to control the motors accordingly.

    return "OK"


    
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ---- RUN THE PAGE ----
if __name__ == '__main__': # -- this is the main function to run the web page on the local host, and port 5000 is the default port for flask, you can change it if needed
    app.run(host='0.0.0.0', port=5000)
