import cv2 # --- importing the file for video streaming---
from  flask import Flask,Response, request # --- import flask, response, request for web hosting
import serial # --- import serial communication for pi - arduino communication
 

# ------- INITIALIZE SERIAL COMMUNICATION AND VIDEO ------

ser = serial.Serial('/dev/ttyUSB0', 9600)
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
        <title>RC CAR LIVE CONTROL</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #eef2f7, #dfe7f1);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            .panel {
                background: white;
                width: 90%;
                max-width: 700px;
                padding: 24px;
                border-radius: 18px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
                text-align: center;
            }

            h1 {
                margin-top: 0;
                margin-bottom: 20px;
                color: #1f2937;
                font-size: 28px;
            }

            .video-box img {
                width: 100%;
                max-width: 520px;
                border-radius: 14px;
                border: 3px solid #d1d9e6;
                margin-bottom: 24px;
            }

            .section-title {
                font-size: 18px;
                font-weight: bold;
                color: #374151;
                margin: 20px 0 12px;
            }

            .motor-grid {
                display: grid;
                grid-template-columns: repeat(3, 90px);
                grid-template-rows: repeat(3, 60px);
                gap: 12px;
                justify-content: center;
                margin-bottom: 24px;
            }

            .servo-row {
                display: flex;
                justify-content: center;
                gap: 14px;
                flex-wrap: wrap;
            }

            button {
                border: none;
                border-radius: 12px;
                background: #2563eb;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
                transition: 0.2s;
            }

            button:hover {
                background: #1d4ed8;
            }

            button:active {
                transform: scale(0.97);
            }

            .control-btn {
                width: 90px;
                height: 60px;
            }

            .stop-btn {
                background: #dc2626;
                box-shadow: 0 4px 10px rgba(220, 38, 38, 0.25);
            }

            .stop-btn:hover {
                background: #b91c1c;
            }

            .servo-btn {
                width: 140px;
                height: 52px;
                background: #059669;
                box-shadow: 0 4px 10px rgba(5, 150, 105, 0.25);
            }

            .servo-btn:hover {
                background: #047857;
            }

            .empty {
                visibility: hidden;
            }

            @media (max-width: 600px) {
                .motor-grid {
                    grid-template-columns: repeat(3, 80px);
                    grid-template-rows: repeat(3, 56px);
                    gap: 10px;
                }

                .control-btn {
                    width: 80px;
                    height: 56px;
                    font-size: 14px;
                }

                .servo-btn {
                    width: 120px;
                    height: 48px;
                    font-size: 14px;
                }

                h1 {
                    font-size: 24px;
                }
            }
        </style>
    </head>
    <body>
        <div class="panel">
            <h1>RC CAR LIVE CONTROL</h1>

            <div class="video-box">
                <img src="/video">
            </div>

            <div class="section-title">Motor Controls</div>

            <div class="motor-grid">
                <div class="empty"></div>

                <button class="control-btn"
                    onmousedown="send('F')"
                    onmouseup="send('S')"
                    ontouchstart="send('F')"
                    ontouchend="send('S')">
                    Forward
                </button>

                <div class="empty"></div>

                <button class="control-btn"
                    onmousedown="send('L')"
                    onmouseup="send('S')"
                    ontouchstart="send('L')"
                    ontouchend="send('S')">
                    Left
                </button>

                <button class="control-btn stop-btn"
                    onmousedown="send('S')"
                    onmouseup="send('S')"
                    ontouchstart="send('S')"
                    ontouchend="send('S')">
                    Stop
                </button>

                <button class="control-btn"
                    onmousedown="send('R')"
                    onmouseup="send('S')"
                    ontouchstart="send('R')"
                    ontouchend="send('S')">
                    Right
                </button>

                <div class="empty"></div>

                <button class="control-btn"
                    onmousedown="send('B')"
                    onmouseup="send('S')"
                    ontouchstart="send('B')"
                    ontouchend="send('S')">
                    Backward
                </button>

                <div class="empty"></div>
            </div>

            <div class="section-title">Servo Controls</div>

            <div class="servo-row">
                <button class="servo-btn" onclick="send('U')">Servo Up</button>
                <button class="servo-btn" onclick="send('D')">Servo Down</button>
            </div>
        </div>

        <script>
            function send(cmd) {
                fetch('/command?cmd=' + cmd);
            }
        </script>
    </body>
    </html>
    '''

@app.route('/command')
def command():
    cmd = request.args.get('cmd')
    print("command Recievd", cmd)

    ser.write((cmd + "\n").encode()) # --- DATA COMMNUNICATION - ARDUINO

    return "OK"


    
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ---- RUN THE PAGE ----
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
