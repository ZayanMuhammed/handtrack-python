import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Setup
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Mouse", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Mouse", 1280, 720)

# Cursor smoothing
x, y = screen_w // 2, screen_h // 2
smooth_factor = 0.33

# Click detection
pinching = False
last_click_time = 0
double_click_window = 0.5  # max time between clicks for double-click

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

        # Finger tips
        ix, iy = hand.landmark[8].x * screen_w, hand.landmark[8].y * screen_h
        tx, ty = hand.landmark[4].x * screen_w, hand.landmark[4].y * screen_h

        # Smooth cursor
        x += (ix - x) * smooth_factor
        y += (iy - y) * smooth_factor
        pyautogui.moveTo(int(x), int(y))

        # Detect pinch
        distance = math.hypot(ix - tx, iy - ty)
        if distance < 40:
            if not pinching:
                # Determine single or double click
                if time.time() - last_click_time < double_click_window:
                    pyautogui.doubleClick()  # double click
                else:
                    pyautogui.click()       # single click
                last_click_time = time.time()
                pinching = True
            else:
                pyautogui.drag()
        else:
            pinching = False

    cv2.imshow("Hand Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27: break  # ESC to quit

cap.release()
cv2.destroyAllWindows()