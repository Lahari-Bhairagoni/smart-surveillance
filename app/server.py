# app/server.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from collections import deque
import time
import os

app = Flask(__name__, template_folder="templates")

# Absolute path to alerts folder
ALERTS_FOLDER = os.path.join(app.root_path, "alerts")

# Make sure folder exists
os.makedirs(ALERTS_FOLDER, exist_ok=True)

events = deque(maxlen=500)

@app.route("/")
def index():
    return render_template("index.html", events=list(events))

@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json() or {}
    data["received_at"] = time.time()
    events.appendleft(data)
    print("[SERVER] Event received:", data)
    return jsonify({"ok": True}), 200

# The correct route to serve images
@app.route('/alerts/<filename>')
def alert_image(filename):
    print("[SERVER] IMAGE REQUEST:", filename)
    return send_from_directory(ALERTS_FOLDER, filename)
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("[SERVER] Alerts folder path:", ALERTS_FOLDER)
    app.run(host="0.0.0.0", port=port, debug=True)
