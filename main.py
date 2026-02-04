from tkinter import messagebox
import cv2
import mediapipe as mp
import pyautogui
import math
import time
import ctypes
import tkinter as tk
from tkinter import ttk

camera_Number = 0  # Default camera

root = tk.Tk()
root.title("Camera Selection")
root.geometry("350x200")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Cool.TCombobox",
    fieldbackground="#2b2b2b",
    background="#2b2b2b",
    foreground="white",
    arrowcolor="white",
    borderwidth=0,
    padding=6
)

style.map(
    "Cool.TCombobox",
    fieldbackground=[("readonly", "#2b2b2b")],
    foreground=[("readonly", "white")],
    background=[("readonly", "#2b2b2b")]
)

# Label
label = tk.Label(
    root,
    text="Select Camera",
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 12)
)
label.pack(pady=15)

# Dropdown values
options = ["0", "1", "2", "3"]

selected = tk.StringVar()
selected.set(options[0])

# Dropdown (Combobox)
dropdown = ttk.Combobox(
    root,
    textvariable=selected,
    values=options,
    state="readonly",
    style="Cool.TCombobox",
    font=("Segoe UI", 11)
)
dropdown.pack(pady=10)

def show_selection():
    global camera_Number
    print("Selected:", selected.get())
    camera_Number = int(selected.get())
    root.destroy()

btn = tk.Button(
    root,
    text="Confirm",
    command=show_selection,
    bg="#414449",
    fg="white",
    font=("Segoe UI", 10),
    relief="flat",
    padx=15,
    pady=6
)
btn.pack(pady=20)

root.mainloop()

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0) # Screen width.
screen_height = user32.GetSystemMetrics(1) # Screen height.

pyautogui.FAILSAFE = False

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0, 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(camera_Number)
cv2.namedWindow("Air Mouse", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Air Mouse", screen_width, screen_height)

# Cursor smoothing
x, y = screen_w // 2, screen_h // 2
smooth_factor = 0.15 

# Click & drag state
pinching = False
dragging = False
last_click_time = 0
double_click_window = 0.5

keyboard_cooldown = 0

last_scroll_y = None
scroll_cooldown = 0

while True:
    ret, frame = cap.read()
    if not ret:
        ctypes.windll.user32.MessageBoxW(
            0,
            "Failed to access the webcam.",
            "Error",
            0x10
        )
        
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

    cv2.imshow("Air Mouse", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
hands.close()