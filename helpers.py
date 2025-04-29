import cv2
import requests

def save_snapshot(frame, path):
    """Save a snapshot image to the given path."""
    try:
        cv2.imwrite(path, frame)
        print(f"Snapshot saved: {path}")
    except Exception as e:
        print(f"Error saving snapshot: {e}")

def save_video(video_capture, frame, path):
    """Save a 5-second video clip when motion is detected."""
    try:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        for _ in range(100):  # 5 seconds at 20 FPS
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to capture frame for video.")
                break
            out.write(frame)
        out.release()
        print(f"Video saved: {path}")
    except Exception as e:
        print(f"Error saving video: {e}")

def send_discord_alert(webhook_url, message):
    """Send an alert message to a Discord channel via webhook."""
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Alert sent to Discord!")
        else:
            print(f"Failed to send alert: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord alert: {e}")
