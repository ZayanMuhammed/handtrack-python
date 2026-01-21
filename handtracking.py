import cv2
import mediapipe as mp
import pyautogui
import math
import time
import ctypes


screen_w, screen_h = pyautogui.size()

# Setup
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Mouse", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Mouse", 1280, 720)

# Cursor smoothing
x, y = screen_w // 2, screen_h // 2
smooth_factor = 0.2

# Click & drag detection
pinching = False
dragging = False
last_click_time = 0
double_click_window = 0.5  # seconds

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

        ix = hand.landmark[8].x * screen_w
        iy = hand.landmark[8].y * screen_h
        tx = hand.landmark[4].x * screen_w
        ty = hand.landmark[4].y * screen_h

        ix = min(max(0, ix), screen_w-1)
        iy = min(max(0, iy), screen_h-1)

        x += (ix - x) * smooth_factor
        y += (iy - y) * smooth_factor
        pyautogui.moveTo(int(x), int(y))

        distance = math.hypot(ix - tx, iy - ty)
        if distance < 40:
            if not pinching:
                if time.time() - last_click_time < double_click_window:
                    pyautogui.doubleClick()
                else:
                    pyautogui.click()
                last_click_time = time.time()
                pinching = True
                dragging = True
                pyautogui.mouseDown()  
        else:
            if dragging:
                pyautogui.mouseUp()  
                dragging = False
            pinching = False

    cv2.imshow("Hand Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27: break  # ESC to quit

cap.release()
cv2.destroyAllWindows()
