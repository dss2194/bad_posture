# Posture Detection System

A real-time posture detection system using computer vision to help maintain good sitting posture and prevent neck strain.

## Features

- Real-time posture detection using webcam
- Neck angle calculation and monitoring
- Visual feedback with status and angles
- Audio alerts for prolonged bad posture
- Timer display for bad posture duration

## Requirements

- Python 3.8 or higher
- Webcam
- Audio output capability

## Installation

1. Clone this repository:

```bash
git clone https://github.com/JordiNeil/bad_posture.git
```

2. Create and activate a virtual environment:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

### Make sure you're in the backend directory and virtual environment is activated
```bash
cd backend
uvicorn main:app --reload
```
In a new terminal, navigate to the frontend directory
```bash
cd frontend
```

4. Run the frontend:
```bash
python -m http.server 3000
```

3. Open your web browser and navigate to:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

4. Click the "Start Detection" button and allow webcam access when prompted.

5. Position yourself in front of the webcam
6. The program will:
   - Show your posture status (Good/Bad)
   - Display your current neck angle
   - Show a timer when in bad posture
   - Play an alert sound after 2 minutes of bad posture

7. Press 'q' to quit the program

## Project Structure

The project has the following structure:

```
bad_posture/
├── backend/
│   ├── main.py            # FastAPI backend server
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── index.html        # Main HTML file
│   ├── styles.css        # Styles
│   ├── app.js            # Frontend JavaScript
│   └── sounds/
│       └── soft-alert.mp3 # Alert sound
└── README.md
```

## Posture Guidelines

- Good posture: Neck angle between 65° and 100°
- Bad posture: Neck angle outside this range
- Try to maintain your head aligned with your shoulders

## Troubleshooting

1. No webcam found:
   - Check webcam connection
   - Try changing camera index (0 or 1) in the code

2. Sound not playing:
   - Verify sound file exists in correct location
   - Check system audio settings
   - Try using winsound alternative (Windows only)

3. MediaPipe errors:
   - Ensure good lighting conditions
   - Check if camera is properly positioned

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


