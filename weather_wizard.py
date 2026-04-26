import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import random

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Start webcam
cap = cv2.VideoCapture(0)

# Function to count fingers
def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    fingers = []

    # Thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

# Weather effects
def draw_rain(frame):
    for _ in range(100):
        x = random.randint(0, frame.shape[1])
        y = random.randint(0, frame.shape[0])
        cv2.line(frame, (x, y), (x, y + 10), (255, 255, 255), 1)

def draw_snow(frame):
    for _ in range(80):
        x = random.randint(0, frame.shape[1])
        y = random.randint(0, frame.shape[0])
        cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)

def draw_lightning(frame):
    start_x = random.randint(100, frame.shape[1] - 100)
    points = [(start_x, 0)]
    for _ in range(8):
        x = points[-1][0] + random.randint(-20, 20)
        y = points[-1][1] + random.randint(30, 50)
        points.append((x, y))
    for i in range(len(points) - 1):
        cv2.line(frame, points[i], points[i + 1], (255, 255, 0), 2)

# Main loop
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(handLms)

            if finger_count == 1:
                draw_rain(frame)
                cv2.putText(frame, "RAIN ☔", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            elif finger_count == 2:
                draw_snow(frame)
                cv2.putText(frame, "SNOW ❄️", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            elif finger_count == 3:
                draw_lightning(frame)
                cv2.putText(frame, "LIGHTNING ⚡", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                cv2.putText(frame, "CLEAR SKY 🌤️", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)

    cv2.imshow("Weather Wizard 🌦️", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
