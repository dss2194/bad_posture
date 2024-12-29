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
git clone https://github.com/your-username/posture-detection-system.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python bad_posture.py
```

2. Position yourself in front of the webcam
3. The program will:
   - Show your posture status (Good/Bad)
   - Display your current neck angle
   - Show a timer when in bad posture
   - Play an alert sound after 2 minutes of bad posture

4. Press 'q' to quit the program

## Configuration

You can modify these variables in `bad_posture.py`:

- `ALERT_THRESHOLD`: Time in seconds before alert (default: 120)
- `SOUND_FILE`: Path to alert sound file
- `cap = cv2.VideoCapture(1)`: Change to 0 for internal webcam

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


