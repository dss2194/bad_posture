import cv2
import numpy as np
import mediapipe as mp
import time
from math import degrees, atan2
from playsound import playsound
from datetime import datetime

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Start capturing video from webcam
cap = cv2.VideoCapture(1) # 0 for internal camera, 1 for external camera

# Add these variables after the camera initialization
bad_posture_start_time = None
last_alert_time = None
ALERT_THRESHOLD = 10  # 10 seconds
SOUND_FILE = "bad_posture/soft-alert.mp3"  # Replace with path to your sound file

def calculate_neck_angle(landmarks):
    # Get coordinates for shoulder and ear
    shoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
    ear = (landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,
           landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y)
    
    # Calculate angle between shoulder and ear
    angle = degrees(atan2(ear[1] - shoulder[1], ear[0] - shoulder[0]))
    return angle

def check_posture(angle):
    global bad_posture_start_time, last_alert_time
    angle *= -1
    if 65 <= angle <= 100:
        bad_posture_start_time = None
        return "Good Posture"
    else:
        current_time = datetime.now()
        if bad_posture_start_time is None:
            bad_posture_start_time = current_time
        else:
            duration = (current_time - bad_posture_start_time).total_seconds()
            if duration >= ALERT_THRESHOLD:
                if last_alert_time is None or (current_time - last_alert_time).total_seconds() >= ALERT_THRESHOLD:
                    try:
                        playsound(SOUND_FILE)
                        last_alert_time = current_time
                    except Exception as e:
                        print(f"Error playing sound: {e}")
        return "Bad Posture! Please sit straight"

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video")
        break
        
    # Convert image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect pose
    results = pose.process(imgRGB)
    
    if results.pose_landmarks:
        # Draw pose landmarks
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Calculate neck angle
        angle = calculate_neck_angle(results.pose_landmarks.landmark)
        
        # Check posture and display message
        posture_status = check_posture(angle)
        cv2.putText(img, f"Status: {posture_status}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if "Good" in posture_status else (0, 0, 255), 2)
        cv2.putText(img, f"Neck Angle: {angle:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add timer display if in bad posture
        if bad_posture_start_time:
            duration = (datetime.now() - bad_posture_start_time).total_seconds()
            cv2.putText(img, f"Bad Posture Time: {int(duration)}s", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Display the image
    cv2.imshow("Posture Detection", img)
    
    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
