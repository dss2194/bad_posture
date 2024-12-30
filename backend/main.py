from fastapi import FastAPI, WebSocket
import cv2
import numpy as np
import mediapipe as mp
import base64
from math import degrees, atan2
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def calculate_neck_angle(landmarks):
    shoulder = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y)
    ear = (landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,
           landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y)
    
    angle = degrees(atan2(ear[1] - shoulder[1], ear[0] - shoulder[0]))
    return angle

def check_posture(angle):
    angle *= -1
    if 65 <= angle <= 100:
        return {"status": "Good Posture", "is_good": True}
    else:
        return {"status": "Bad Posture! Please sit straight", "is_good": False}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive base64 encoded image from client
            data = await websocket.receive_text()
            
            # Decode base64 image
            encoded_data = data.split(',')[1]
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert image to RGB
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Process the image and detect pose
            results = pose.process(imgRGB)
            
            if results.pose_landmarks:
                # Calculate neck angle
                angle = calculate_neck_angle(results.pose_landmarks.landmark)
                
                # Check posture
                posture_result = check_posture(angle)
                
                # Convert landmarks to list for JSON serialization
                landmarks = []
                for landmark in results.pose_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    })
                
                # Send results back to client
                await websocket.send_json({
                    "angle": angle,
                    "status": posture_result["status"],
                    "is_good": posture_result["is_good"],
                    "landmarks": landmarks
                })
            else:
                await websocket.send_json({
                    "error": "No pose detected"
                })
                
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()

@app.get("/")
async def root():
    return {"message": "Posture Detection API is running"} 