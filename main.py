import cv2
import mediapipe as mp
import pyautogui
import math
import time

pyautogui.FAILSAFE = False

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Mouse", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hand Mouse", 1280, 720)

# Cursor smoothing
x, y = screen_w // 2, screen_h // 2
smooth_factor = 0.15

# Click & drag state
pinching = False
dragging = False
last_click_time = 0
double_click_window = 0.5

keyboard_cooldown = 0

# 🔹 Scroll state (NEW)
last_scroll_y = None
scroll_cooldown = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        ix, iy = hand.landmark[8].x * screen_w, hand.landmark[8].y * screen_h
        tx, ty = hand.landmark[4].x * screen_w, hand.landmark[4].y * screen_h
        mx, my = hand.landmark[12].x * screen_w, hand.landmark[12].y * screen_h

        # 🔹 Fist landmarks (NEW)
        ry = hand.landmark[16].y * screen_h
        py = hand.landmark[20].y * screen_h

        ix = max(0, min(screen_w - 1, ix))
        iy = max(0, min(screen_h - 1, iy))

        # Smooth cursor movement
        x += (ix - x) * smooth_factor
        y += (iy - y) * smooth_factor
        pyautogui.moveTo(int(x), int(y), duration=0)

        distance_index = math.hypot(ix - tx, iy - ty)
        distance_middle = math.hypot(ix - mx, iy - my)

        # Win + H
        if distance_middle < 40 and time.time() - keyboard_cooldown > 1:
            pyautogui.hotkey("win", "h")
            keyboard_cooldown = time.time()

        # 🔹 Fist closed scroll (NEW)
        fist_closed = max(iy, my, ry, py) - min(iy, my, ry, py) < 25

        if fist_closed:
            if last_scroll_y and time.time() - scroll_cooldown > 0.15:
                if iy < last_scroll_y - 10:
                    pyautogui.scroll(100)      # scroll up
                    scroll_cooldown = time.time()
                elif iy > last_scroll_y + 10:
                    pyautogui.scroll(-100)     # scroll down
                    scroll_cooldown = time.time()
            last_scroll_y = iy
        else:
            last_scroll_y = None

        # Click & drag
        if distance_index < 40:
            if not pinching:
                if time.time() - last_click_time < double_click_window:
                    pyautogui.doubleClick()
                else:
                    pyautogui.click()
                last_click_time = time.time()
                pyautogui.mouseDown()
                dragging = True
                pinching = True
        else:
            if dragging:
                pyautogui.mouseUp()
            dragging = False
            pinching = False

    cv2.imshow("Hand Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
