import cv2
import time
import imutils
from helpers import save_video, save_snapshot, send_discord_alert
from config import DISCORD_WEBHOOK_URL

# Parameters
MIN_CONTOUR_AREA = 1000  # Ignore very small movements
MOTION_DETECTION_FRAMES = 3  # Frames where motion must be consistently detected
FRAME_UPDATE_INTERVAL = 30  # Update first_frame every 30 frames
VIDEO_FILE_PATH = "C:/Users/Abdullah Amer/Desktop/Intruder detection/Testing Dataset/3.mp4"  # Hardcoded video path

# Prompt user to choose an option
print("Choose an option:")
print("1. Use Webcam")
print("2. Test with Video File")
choice = input("Enter 1 or 2: ")

if choice == "1":
    # Option 1: Webcam Motion Detection
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Unable to access the webcam.")
        exit()

    first_frame = None
    motion_detected_count = 0
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame.")
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Initialize or periodically update the first frame
        if first_frame is None or frame_count % FRAME_UPDATE_INTERVAL == 0:
            first_frame = gray
            continue

        # Compute the absolute difference
        delta_frame = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue

            # Motion detected
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_detected:
            motion_detected_count += 1
        else:
            motion_detected_count = 0

        # Trigger alert only after consistent motion detection
        if motion_detected_count >= MOTION_DETECTION_FRAMES:
            print("Motion detected! Saving snapshot, video, and sending alert...")
            timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
            save_video(video_capture, frame, f"motion_{timestamp}.avi")
            save_snapshot(frame, f"snapshot_{timestamp}.jpg")
            send_discord_alert(DISCORD_WEBHOOK_URL, f"🚨 Motion detected! Snapshot and video saved as motion_{timestamp}")
            motion_detected_count = 0  # Reset after sending alert

        # Display the video feed
        cv2.imshow("Webcam Motion Detector", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
elif choice == "2":
    video_file = "C:\\Users\\Abdullah Amer\\Desktop\\Intruder detection\\Testing Dataset\\3.mp4" 
    video_capture = cv2.VideoCapture(video_file)  # Use video file
else:
    print("Invalid choice. Exiting program.")
    exit()

# Initialize variables
first_frame = None

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        print("End of video or no feed from webcam.")
        break

    frame = imutils.resize(frame, width=500)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    
    if first_frame is None:
        first_frame = gray_frame
        continue

    frame_delta = cv2.absdiff(first_frame, gray_frame)
    threshold_frame = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
    
    contours, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Ignore small movements
            continue
        
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion_detected = True
    
    if motion_detected:
        print("Motion detected!")
        send_discord_alert(DISCORD_WEBHOOK_URL, "🚨 Intruder Alert! Motion detected!")
        motion_detected = False

    # Show video feed
    cv2.imshow("Motion Detection", frame)
    cv2.imshow("Threshold Frame", threshold_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
