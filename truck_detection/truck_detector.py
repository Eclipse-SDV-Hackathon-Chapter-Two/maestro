import cv2
import torch
import time

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # Use a pre-trained YOLOv5 model

# Configurable object type
object_to_detect = "truck"  # Change this to "truck", "bottle", etc., as needed

# Set the webcam index (0 is usually the default camera)
camera_index = 0

# Open the webcam
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: Unable to access the camera")
    exit()

print("Press 'q' to quit the application.")

# Function to call when a truck is detected for longer than 3 seconds
def truck_detected():
    print("truck detected")
    time.sleep(5)  

# Main loop for real-time detection
truck_detected_start_time = None
truck_detected_duration = 3  # seconds

# Main loop for real-time detection
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from camera")
        break

    # Perform inference
    results = model(frame)

    # Filter detections based on the object_to_detect
    filtered_results = results.pandas().xyxy[0]  # Get detection results as a Pandas DataFrame
    filtered_results = filtered_results[filtered_results['name'] == object_to_detect]

    # Check if a truck is detected
    if not filtered_results.empty:
        truck_detected()

    # Draw bounding boxes for filtered detections
    detection_frame = frame.copy()
    for _, row in filtered_results.iterrows():
        x_min, y_min, x_max, y_max = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        confidence = row['confidence']
        label = f"{row['name']} {confidence:.2f}"

        # Draw rectangle and label
        cv2.rectangle(detection_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(detection_frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the original camera feed and the detection frame side by side
    cv2.imshow('Camera Preview and Detection', detection_frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()