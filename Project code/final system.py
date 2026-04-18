from flask import Flask, request, jsonify, render_template_string, Response
import cv2
import os
import threading
import time
from datetime import datetime

app = Flask(__name__)

# --- ROBUST DIRECTORY SETUP ---
# This gets the exact folder where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
HISTORY_DIR = os.path.join(STATIC_DIR, 'history')

# Ensure folders exist using absolute paths
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# --- GLOBAL STORAGE ---
latest_data = {
    "temp": 0, "hum": 0, "gas": 0, "water": 0,
    "fire": "NO", "status": "System Clear", "locs": "None",
    "last_alert_time": "N/A",
    "alarm_active": False,
    "history": [] 
}

camera_lock = threading.Lock()
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
time.sleep(2) 

def gen_frames():
    while True:
        with camera_lock:
            success, frame = camera.read()
        if not success:
            time.sleep(0.1)
            continue
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

    latest_data.update({
        "temp": data.get('temp', 0),
        "hum": data.get('hum', 0),
        "gas": data.get('gas', 0),
        "water": data.get('water', 0),
        "fire": "YES" if data.get('fire') == 1 else "NO",
        "locs": data.get('locs', 'None')
    })

    if data.get('count', 0) > 0:
        latest_data["status"] = f"CRITICAL: {data.get('locs')}"
        ts_file = datetime.now().strftime("%H-%M-%S")
        latest_data["last_alert_time"] = ts_file.replace('-', ':')
        latest_data["alarm_active"] = True
        
        with camera_lock:
            success, frame = camera.read()
        
        if success:
            h, w, _ = frame.shape
            start_p = (w // 4, h // 4)
            end_p = (3 * w // 4, 3 * h // 4)
            cv2.rectangle(frame, start_p, end_p, (0, 0, 255), 8)
            cv2.rectangle(frame, (start_p[0], start_p[1] - 40), (start_p[0] + 350, start_p[1]), (0, 0, 255), -1)
            cv2.putText(frame, f"ALARM: {data.get('locs')}", (start_p[0] + 10, start_p[1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            
            # Use absolute paths for writing files
            roi_path = os.path.join(STATIC_DIR, 'roi_alert.jpg')
            cv2.imwrite(roi_path, frame)
            
            hist_filename = f"alert_{ts_file}.jpg"
            hist_path = os.path.join(HISTORY_DIR, hist_filename)
            cv2.imwrite(hist_path, frame)
            
            if hist_filename not in latest_data["history"]:
                latest_data["history"].insert(0, hist_filename)
                latest_data["history"] = latest_data["history"][:5]
    else:
        latest_data["status"] = "System Clear"
        latest_data["alarm_active"] = False

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
            <title>Edge AI-driven Incident Response System</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background: #0c0c0c; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; margin: 0; padding: 15px; }
                .container { max-width: 1200px; margin: auto; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; margin-bottom: 20px; }
                .card { background: #181818; padding: 15px; border-radius: 12px; border: 1px solid #333; }
                .status-bar { padding: 20px; margin-bottom: 20px; border-radius: 10px; font-weight: bold; font-size: 1.8em; text-transform: uppercase; }
                .safe { background: #1b4332; color: #b7e4c7; border: 2px solid #2d6a4f; }
                .alert { background: #641212; color: #ffb3b3; border: 2px solid #a4161a; animation: blink 0.8s infinite; }
                @keyframes blink { 50% { opacity: 0.5; } }
                img { width: 100%; border-radius: 8px; border: 2px solid #444; background: #000; min-height: 200px; }
                .telemetry-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 20px; }
                .stat-box { background: #222; padding: 10px; border-radius: 10px; border-top: 4px solid #555; }
                .stat-value { font-size: 1.2em; font-weight: bold; color: #00ff88; margin-top: 5px; }
                #history-container { display: flex; gap: 15px; overflow-x: auto; padding: 15px; margin-top: 10px; background: #111; border-radius: 10px; min-height: 180px; }
                .history-item { min-width: 180px; text-align: center; }
                .history-item img { border: 1px solid #555; width: 180px; height: 120px; object-fit: cover; min-height: auto; }
                #audio-btn { padding: 15px; background: #a4161a; color: white; border: none; border-radius: 8px; cursor: pointer; margin-bottom: 15px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>GOAL GETTER'S SECURITY HUB</h1>
                <button id="audio-btn">🔊 ACTIVATE SITE AUDIO ALARM</button>
                <div id="status-box" class="status-bar safe">SYSTEM CLEAR</div>
                
                <div class="grid">
                    <div class="card">
                        <h3>LIVE FEED</h3>
                        <img src="/video_feed">
                    </div>
                    <div class="card">
                        <h3>ROI ALARM SNAPSHOT</h3>
                        <img id="roi-img" src="/static/roi_alert.jpg" onerror="this.style.display='none'">
                        <div id="roi-placeholder" style="display:none; padding: 80px 0; color: #555;">AWAITING ALARM DATA</div>
                        <p style="color: #888; font-size: 0.9em;">Last Alert: <span id="cap-time">N/A</span></p>
                    </div>
                </div>

                <div class="telemetry-grid">
                    <div class="stat-box"><div>TEMP</div><div class="stat-value"><span id="t">0</span>°C</div></div>
                    <div class="stat-box"><div>HUMIDITY</div><div class="stat-value"><span id="h">0</span>%</div></div>
                    <div class="stat-box"><div>GAS</div><div class="stat-value"><span id="g">0</span> ppm</div></div>
                    <div class="stat-box"><div>WATER</div><div class="stat-value"><span id="w">0</span>%</div></div>
                    <div class="stat-box"><div>FIRE</div><div class="stat-value"><span id="f">NO</span></div></div>
                </div>

                <div class="card" style="margin-top: 30px;">
                    <h3>ALARM HISTORY (LAST 5 EVENTS)</h3>
                    <div id="history-container"></div>
                </div>
            </div>

            <script>
                let audioCtx = null;
                let oscillator = null;
                let audioActive = false;
                let lastAlertTime = "";

                document.getElementById('audio-btn').addEventListener('click', function() {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    audioActive = true;
                    this.innerText = "🔊 AUDIO SYSTEM ARMED";
                    this.style.background = "#1b4332";
                });

                function playAlarm() {
                    if (!audioActive || oscillator) return;
                    oscillator = audioCtx.createOscillator();
                    let gain = audioCtx.createGain();
                    oscillator.type = 'sawtooth';
                    oscillator.frequency.setValueAtTime(900, audioCtx.currentTime);
                    oscillator.connect(gain);
                    gain.connect(audioCtx.destination);
                    oscillator.start();
                    setTimeout(() => { oscillator.stop(); oscillator = null; }, 400);
                }

                function update() {
                    fetch('/data').then(res => res.json()).then(data => {
                        const sBox = document.getElementById('status-box');
                        sBox.innerText = data.status;
                        
                        if(data.alarm_active) {
                            sBox.className = 'status-bar alert';
                            playAlarm();
                            if (data.last_alert_time !== lastAlertTime) {
                                lastAlertTime = data.last_alert_time;
                                const roiImg = document.getElementById('roi-img');
                                roiImg.style.display = 'block';
                                // Cache buster with timestamp
                                roiImg.src = "/static/roi_alert.jpg?t=" + new Date().getTime();
                            }
                        } else {
                            sBox.className = 'status-bar safe';
                        }
                        
                        document.getElementById('t').innerText = data.temp;
                        document.getElementById('h').innerText = data.hum;
                        document.getElementById('g').innerText = data.gas;
                        document.getElementById('w').innerText = Math.round((data.water / 1023) * 100);
                        document.getElementById('f').innerText = data.fire;
                        document.getElementById('cap-time').innerText = data.last_alert_time;

                        const container = document.getElementById('history-container');
                        container.innerHTML = data.history.map(img => `
                            <div class="history-item">
                                <img src="/static/history/${img}?t=${new Date().getTime()}" alt="History">
                                <p style="font-size:0.7em; margin-top:5px;">${img.replace('alert_','').replace('.jpg','')}</p>
                            </div>
                        `).join('');
                    });
                }
                setInterval(update, 1000);
            </script>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)