import cv2

# Start video capture (0 for webcam, or provide IP camera URL)
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        break
    
    # Display the video feed
    cv2.imshow("Video Feed", frame)
    
    # Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
