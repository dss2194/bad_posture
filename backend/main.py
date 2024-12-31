from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import cv2
import numpy as np
import mediapipe as mp
from math import degrees, atan2
from fastapi.middleware.cors import CORSMiddleware
import os
from io import BytesIO
from PIL import Image

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the frontend directory
# When running in Docker, the frontend will be in /app/frontend
if os.path.exists("/app/frontend"):
    frontend_dir = "/app/frontend"
else:
    # For local development
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# Create a sub-application for API routes
api_app = FastAPI()

@api_app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
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
        
        return {
            "angle": angle,
            "status": posture_result["status"],
            "is_good": posture_result["is_good"],
            "landmarks": landmarks
        }
    else:
        return {"error": "No pose detected"}

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
    if 60 <= angle <= 80:
        return {"status": "Good Posture", "is_good": True}
    else:
        return {"status": "Bad Posture! Please sit straight", "is_good": False}

# Mount the API routes under /api
app.mount("/api", api_app)

# Verify frontend directory exists
if not os.path.exists(frontend_dir):
    raise RuntimeError(f"Frontend directory not found at: {frontend_dir}")

# Serve static files
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend") 