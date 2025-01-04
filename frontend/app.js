let config = {
    minAngle: 63,
    maxAngle: 80,
    alertInterval: 10000 // 10 seconds in milliseconds
};

let badPostureStartTime = null;
let lastAlertTime = null;
const ALERT_THRESHOLD = 10000; // 10 seconds in milliseconds
const cameraOverlay = document.querySelector('.camera-overlay');

async function startWebcam() {
    const video = document.getElementById('video');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.onloadedmetadata = () => {
            cameraOverlay.classList.add('hidden');
        };
    } catch (error) {
        console.error('Error accessing webcam:', error);
        cameraOverlay.textContent = 'Error accessing camera';
    }
}

async function sendFrame() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const frame = canvas.toDataURL('image/jpeg');
    const blob = await (await fetch(frame)).blob();
    const formData = new FormData();
    formData.append('file', blob, 'frame.jpg');
    
    try {
        const response = await fetch('/api/process-image', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error('Error sending frame:', error);
    }
}

function updateUI(data) {
    const statusElement = document.getElementById('status');
    const angleElement = document.getElementById('angle');
    const timerElement = document.getElementById('timer');
    
    if (data.error) {
        statusElement.textContent = `Status: ${data.error}`;
        statusElement.className = 'status-message';
        return;
    }
    
    // Update status with appropriate styling
    statusElement.textContent = data.status;
    statusElement.className = 'status-message ' + (data.is_good ? 'good-posture' : 'bad-posture');
    
    angleElement.textContent = `Neck Angle: ${data.angle.toFixed(2)}`;
    
    // Draw pose markers if landmarks are available
    if (data.landmarks) {
        drawPoseMarkers(data.landmarks);
    }
    
    if (!data.is_good) {
        if (!badPostureStartTime) {
            badPostureStartTime = Date.now();
        }
        
        const duration = Math.floor((Date.now() - badPostureStartTime) / 1000);
        timerElement.textContent = `Bad Posture Time: ${duration}s`;
        timerElement.classList.remove('hidden');
        
        if (duration >= config.alertInterval / 1000) {
            if (!lastAlertTime || (Date.now() - lastAlertTime) >= config.alertInterval) {
                playAlert();
                lastAlertTime = Date.now();
            }
        }
    } else {
        badPostureStartTime = null;
        timerElement.classList.add('hidden');
    }
}

function playAlert() {
    const audio = new Audio('sounds/soft-alert.mp3');
    audio.play().catch(e => console.log('Error playing sound:', e));
}

function drawPoseMarkers(landmarks) {
    const canvas = document.getElementById('pose-canvas');
    const ctx = canvas.getContext('2d');
    const video = document.getElementById('video');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw landmarks
    landmarks.forEach((landmark, index) => {
        if (landmark.visibility > 0.5) {
            ctx.beginPath();
            ctx.arc(
                landmark.x * canvas.width,
                landmark.y * canvas.height,
                3,
                0,
                2 * Math.PI
            );
            ctx.fillStyle = '#00FF00';
            ctx.fill();
        }
    });
    
    // Draw connections (simplified version - you can add more connections as needed)
    drawConnections(ctx, landmarks, canvas.width, canvas.height);
}

function drawConnections(ctx, landmarks, width, height) {
    // Define some basic connections (you can add more)
    const connections = [
        // Shoulders
        [11, 12],
        // Right arm
        [11, 13],
        [13, 15],
        // Left arm
        [12, 14],
        [14, 16],
        // Right ear to shoulder
        [8, 12],
        // Left ear to shoulder
        [7, 11]
    ];
    
    ctx.strokeStyle = '#00FF00';
    ctx.lineWidth = 2;
    
    connections.forEach(([i, j]) => {
        const start = landmarks[i];
        const end = landmarks[j];
        
        if (start.visibility > 0.5 && end.visibility > 0.5) {
            ctx.beginPath();
            ctx.moveTo(start.x * width, start.y * height);
            ctx.lineTo(end.x * width, end.y * height);
            ctx.stroke();
        }
    });
}

async function updateConfig() {
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                min_angle: config.minAngle,
                max_angle: config.maxAngle
            })
        });
        const data = await response.json();
        if (data.message === "Configuration updated") {
            console.log('Configuration updated successfully:', data.config);
        } else {
            console.error('Error updating configuration:', data);
        }
    } catch (error) {
        console.error('Error updating configuration:', error);
    }
}

document.getElementById('saveConfig').addEventListener('click', () => {
    const minAngle = parseInt(document.getElementById('minAngle').value);
    const maxAngle = parseInt(document.getElementById('maxAngle').value);
    const alertInterval = parseInt(document.getElementById('alertInterval').value) * 1000;

    if (minAngle >= maxAngle) {
        alert('Minimum angle must be less than maximum angle');
        return;
    }

    config.minAngle = minAngle;
    config.maxAngle = maxAngle;
    config.alertInterval = alertInterval;
    
    updateConfig();
});

document.getElementById('startBtn').addEventListener('click', async () => {
    const button = document.getElementById('startBtn');
    button.disabled = true;
    button.textContent = 'Starting...';
    
    await startWebcam();
    setInterval(sendFrame, 1000);
    
    button.textContent = 'Detection Running';
}); 