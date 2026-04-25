# AI Smart Surveillance System

## Overview

The AI Smart Surveillance System is a real-time object detection application that leverages deep learning techniques to monitor and analyze video input. It uses the YOLO (You Only Look Once) model for fast and accurate object detection and provides a web-based interface for visualization.

This project is designed to reduce manual monitoring efforts and enhance surveillance efficiency through automation.

---

## Features

* Real-time object detection using YOLOv8n
* Live video stream processing
* Web-based interface for monitoring
* Modular backend using Flask
* Scalable and extensible architecture

---

## Tech Stack

**Backend**

* Python
* Flask

**AI / ML**

* YOLOv8n (Ultralytics)
* OpenCV
* NumPy

**Frontend**

* HTML (Flask templates)

**Tools**

* Git & GitHub
* Docker

---

## Project Structure

```
smart-surveillance/
│
├── app/
│   ├── alerts/
│   ├── templates/
│   │   └── index.html
│   ├── detector.py
│   ├── server.py
│   └── yolov8n.pt
│
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── test.jpg
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Lahari-Bhairagoni/smart-surveillance.git
cd smart-surveillance
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the application

```bash
cd app
python server.py
```

---

## Usage

1. Start the server
2. Open a browser and go to:

   ```
   http://localhost:5000
   ```
3. The system will begin processing video input and displaying detected objects in real time

---

## How It Works

1. The system captures input (image/video stream)
2. Each frame is processed using the YOLOv8 model
3. Objects are detected and classified
4. Results are rendered on the web interface

---

## Future Enhancements

- Real-time alert system (email/SMS)
- Cloud deployment (AWS/GCP)
- Database integration for event logging
- Role-based authentication system
- Mobile app integration

---

## Author

Lahari Bhairagoni
B.Tech Student

---

## License

This project is developed for academic purposes.
