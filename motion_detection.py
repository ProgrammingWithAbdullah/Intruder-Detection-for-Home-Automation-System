import cv2
import imutils

# Function to choose video source: webcam or video file
def get_video_source(video_file=None):
    if video_file:
        # Load video file for testing
        video_capture = cv2.VideoCapture(video_file)
    else:
        # Use webcam for live feed
        video_capture = cv2.VideoCapture(0)
    return video_capture

# Set your video file path (leave it None for webcam feed)
video_file = None  # Change to 'your_video_file.mp4' for testing with a video file

# Start video capture (webcam or video file)
video_capture = get_video_source(video_file)
first_frame = None

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        break
    
    # Resize frame for faster processing
    frame = imutils.resize(frame, width=500)
    
    # Convert frame to grayscale and blur it
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    
    # Initialize the first frame
    if first_frame is None:
        first_frame = gray_frame
        continue
    
    # Calculate frame difference
    frame_delta = cv2.absdiff(first_frame, gray_frame)
    threshold_frame = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)
    
    # Find contours of moving objects
    contours, _ = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Ignore small movements
            continue
        
        # Draw a rectangle around the moving object
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Display video feed and motion detection
    cv2.imshow("Motion Detection", frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    
    # Press 'q' to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
