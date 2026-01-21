🖐️ Hand Tracking with Python
Real-time hand tracking using MediaPipe and OpenCV in Python. Detect and track hand landmarks with ease — perfect for gesture control, virtual drawing, or AI-based input systems.

🚀 Features
Real-time hand detection and tracking

21 hand landmarks (fingers, joints, wrist)

Detects both left and right hands

Visualizes hand connections using OpenCV

Lightweight and works on CPU

🛠️ Requirements
bash
Copy code
pip install mediapipe opencv-python
💻 How to Run
bash
Copy code
python handtrack.py
Make sure your webcam is connected and accessible.

🧠 How It Works
This project uses:

MediaPipe Hands: For detecting and tracking hands + landmarks

OpenCV: For webcam access and drawing results

MediaPipe returns 21 landmark points per detected hand, which can be used for gesture recognition, finger counting, and more.

