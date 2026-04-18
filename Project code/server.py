from flask import Flask, request, jsonify, render_template_string, Response
import cv2
import os
import threading
import time

app = Flask(__name__)

# Ensure folder for alert images exists
if not os.path.exists('static'):
    os.makedirs('static')

# Global storage for Arduino data
latest_data = {
    "temp": 0, "hum": 0, "gas": 0, "water": 0,
    "fire": "NO", "status": "System Clear", "locs": "None"
}

# WINDOWS 11 FIX: Use CAP_DSHOW to prevent camera initialization lag
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
time.sleep(2) # Give Windows time to grant permission

def gen_frames():
    """Generates the live video stream."""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/trigger', methods=['POST'])
def trigger():
    global latest_data
    data = request.json
    if not data: return jsonify({"status": "no_data"}), 400

    # Update global sensor values
    latest_data.update({
        "temp": data.get('temp', 0),
        "hum": data.get('hum', 0),
        "gas": data.get('gas', 0),
        "water": data.get('water', 0),
        "fire": "YES" if data.get('fire') == 1 else "NO",
        "locs": data.get('locs', 'None')
    })

    # If Arduino reports an alarm (count > 0), capture ROI image
    if data.get('count', 0) > 0:
        latest_data["status"] = f"CRITICAL: {data.get('locs')}"
        ret, frame = camera.read()
        if ret:
            h, w, _ = frame.shape
            # Draw Red ROI Box (Center)
            cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 0, 255), 3)
            cv2.putText(frame, f"ALARM: {data.get('locs')}", (40, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imwrite('static/roi_alert.jpg', frame)
    else:
        latest_data["status"] = "System Clear"

    return jsonify({"status": "success"}), 200

@app.route('/data')
def get_data():
    return jsonify(latest_data)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Shield-X Windows Dashboard</title>
            <style>
                body { background: #0c0c0c; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; margin: 0; padding: 20px; }
                .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1200px; margin: auto; }
                .card { background: #181818; padding: 20px; border-radius: 15px; border: 1px solid #333; }
                .status-bar { padding: 15px; margin-bottom: 20px; border-radius: 10px; font-weight: bold; font-size: 1.5em; }
                .safe { background: #1b4332; color: #b7e4c7; }
                .alert { background: #641212; color: #ffb3b3; animation: blink 1s infinite; }
                @keyframes blink { 50% { opacity: 0.7; } }
                img { width: 100%; border-radius: 10px; border: 2px solid #222; }
                .telemetry { display: flex; justify-content: space-around; margin-top: 20px; background: #222; padding: 15px; border-radius: 10px; }
            </style>
        </head>
        <body>
            <h1>SECURITY HUB INTERFACE</h1>
            <div id="status-box" class="status-bar safe">SYSTEM CLEAR</div>
            
            <div class="grid">
                <div class="card">
                    <h3>LIVE CAMERA STREAM</h3>
                    <img src="/video_feed">
                </div>
                <div class="card">
                    <h3>ROI ALARM CAPTURE</h3>
                    <img id="roi-img" src="/static/roi_alert.jpg" onerror="this.src='https://placehold.co/640x480/111/333?text=Awaiting+Trigger'">
                </div>
            </div>

            <div class="telemetry card" style="width: 90%; margin: 20px auto;">
                <div>TEMP: <b id="t">0</b>°C</div>
                <div>HUM: <b id="h">0</b>%</div>
                <div>GAS: <b id="g">0</b></div>
                <div>WATER: <b id="w">0</b></div>
                <div>FIRE: <b id="f">NO</b></div>
            </div>

            <script>
                function update() {
                    fetch('/data').then(res => res.json()).then(data => {
                        const sBox = document.getElementById('status-box');
                        sBox.innerText = data.status;
                        sBox.className = data.status.includes('CRITICAL') ? 'status-bar alert' : 'status-bar safe';
                        
                        document.getElementById('t').innerText = data.temp;
                        document.getElementById('h').innerText = data.hum;
                        document.getElementById('g').innerText = data.gas;
                        document.getElementById('w').innerText = data.water;
                        document.getElementById('f').innerText = data.fire;

                        if(data.status.includes('CRITICAL')) {
                            document.getElementById('roi-img').src = "/static/roi_alert.jpg?t=" + new Date().getTime();
                        }
                    });
                }
                setInterval(update, 1000);
            </script>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
    