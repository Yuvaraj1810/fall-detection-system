import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.title("Fall Detection System for Elderly (Demo)")

run = st.checkbox('Start Camera')

FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def detect_fall(landmarks):
    try:
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

        # Calculate vertical angle (basic logic for fall detection)
        if left_shoulder and left_hip and left_ankle:
            shoulder_y = left_shoulder.y
            hip_y = left_hip.y
            ankle_y = left_ankle.y

            if abs(hip_y - shoulder_y) < 0.1 and abs(ankle_y - hip_y) < 0.1:
                return True
    except:
        return False
    return False

while run:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if detect_fall(results.pose_landmarks.landmark):
            cv2.putText(frame, 'Fall Detected!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
else:
    st.write('Stopped')
    camera.release()