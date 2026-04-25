# app/detector.py
last_alert_time = 0
ALERT_COOLDOWN = 5  # seconds (you can keep 5–10)
from cProfile import label
import os
import time
import cv2
import requests
from ultralytics import YOLO

# ---------------- CONFIG ----------------
MODEL_PATH = "yolov8n.pt"               # change to your weapon-trained weights if you have one
SERVER_ALERT_URL = "http://127.0.0.1:5000/alert"
ALERTS_DIR = "alerts"
os.makedirs(ALERTS_DIR, exist_ok=True)

# suspicious / grouping labels
WEAPON_LIKE = ["knife", "scissors"]
COMMON_OBJECTS = ["bottle", "cup", "laptop", "book", "cell phone", "keyboard"]

# suspicious classes (lowercase). If your model doesn't have these names, change accordingly.
SUSPICIOUS_LABELS = []  # leave empty for now

# thresholds
WEAPON_CONF_THRESHOLD = 0.25
GENERAL_CONF_THRESHOLD = 0.35

# camera / source
VIDEO_SOURCE = 0
# ----------------------------------------

model = YOLO(MODEL_PATH)
print("MODEL CLASSES:", model.names)   # debug: shows class id -> name

def send_alert(payload):
    try:
        res = requests.post(SERVER_ALERT_URL, json=payload, timeout=3)
        if res.ok:
            print("[ALERT] Sent:", payload)
        else:
            print("[ALERT] Server returned:", res.status_code, res.text)
    except Exception as e:
        print("[ALERT] Failed to send:", e)

def save_snapshot(frame, prefix="weapon"):
    ts = int(time.time() * 1000)
    fname = f"{prefix}_{ts}.jpg"
    path = os.path.join(ALERTS_DIR, fname)
    cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

    # 🔥 ADD THIS 👇
    files = sorted(os.listdir(ALERTS_DIR))
    if len(files) > 30:
        for f in files[:len(files)-30]:
            try:
                os.remove(os.path.join(ALERTS_DIR, f))
            except:
                pass

    return fname, path

def main():
    global last_alert_time
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print("ERROR: Cannot open video source", VIDEO_SOURCE)
        return

    print("Detector started. Press 'q' in the video window to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Frame not received")
            break

        # run detection (can pass imgsz for speed/accuracy tradeoff)
        results = model(frame, imgsz=960)

        # loop results (usually one item)
        for r in results:
            boxes = getattr(r, "boxes", None)
            if boxes is None:
                continue

            suspicious_found = []
            for box in boxes:
                # safe extraction of values
                try:
                    cls_id = int(box.cls[0])
                except Exception:
                    cls_id = int(box.cls) if hasattr(box, "cls") else -1

                conf = float(box.conf[0]) if hasattr(box.conf, "__len__") else float(box.conf)
                label = model.names[cls_id].lower()
                # simulate missing classes (demo logic)
                if label == "toothbrush":
                    label = "pen"

                if label == "book":
                    label = "paper"

                # DEBUG print - shows every detection label + confidence
                print(f"[DEBUG] Detected: {label} conf={conf:.2f} cls={cls_id}")

                # convert tensor coords to ints safely
                try:
                    coords = box.xyxy[0].tolist()
                except Exception:
                    # fallback if xyxy is already list-like
                    coords = list(box.xyxy[0])
                x1, y1, x2, y2 = [int(v) for v in coords]

                # draw box & label (optional)
                color = (0, 0, 255) if label in WEAPON_LIKE else (0, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 8),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                # check suspicious labels
                if label in WEAPON_LIKE and conf >= 0.3:
                    category = "normal"

                    if label in WEAPON_LIKE:
                        category = "suspicious"

                    elif label in COMMON_OBJECTS:
                        category = "object"

                    suspicious_found.append({
                        "label": label,
                        "conf": conf,
                        "bbox": [x1, y1, x2, y2],
                        "type": category
                    })

            if suspicious_found and (time.time() - last_alert_time > ALERT_COOLDOWN):
                last_alert_time = time.time()
                # save snapshot and alert
                fname, fullpath = save_snapshot(frame, prefix="weapon")
                event_type = "weapon_detected" if any(d["type"] == "suspicious" for d in suspicious_found) else "object_detected"
                payload = {
                    "event": "weapon_detected",
                    "count": len(suspicious_found),
                    "detections": suspicious_found,
                    "image": fname,
                    "ts": time.time()
                }
                print("[DETECTOR] About to send payload:", payload)
                send_alert(payload)

        # show frame locally
        cv2.imshow("Smart Surveillance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# delete old files if more than 50 images
files = sorted(os.listdir(ALERTS_DIR))
if len(files) > 50:
    for f in files[:len(files)-50]:
        try:
            os.remove(os.path.join(ALERTS_DIR, f))
        except:
            pass