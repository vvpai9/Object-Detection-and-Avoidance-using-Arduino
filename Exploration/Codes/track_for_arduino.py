import cv2
import numpy as np
from ultralytics import YOLO
import serial
from collections import defaultdict
from ultralytics.utils.plotting import Annotator, colors

# Initialize tracking history
track_history = defaultdict(lambda: [])

# Load the YOLO model
model = YOLO("yolov8n.pt")
names = model.model.names

# Set up serial communication
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    print("Connected to Arduino")
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Function to send data to Arduino
def send_to_arduino(data):
    if arduino.is_open:
        arduino.write((data + '\n').encode())
    else:
        print("Arduino serial port is not open.")

# Open video file
# video_path = "/path/to/video/file.mp4" ------> Path to Video for Detection
cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"

# Get video properties
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Set up the video writer for the output video
result = cv2.VideoWriter("object_tracking.avi",
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         fps,
                         (w, h))

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Perform object tracking
        results = model.track(frame, persist=True, verbose=False)
        boxes = results[0].boxes.xyxy.cpu()

        detected = False
        if results[0].boxes.id is not None:
            # Extract prediction results
            clss = results[0].boxes.cls.cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confs = results[0].boxes.conf.float().cpu().tolist()

            # Initialize annotator
            annotator = Annotator(frame, line_width=2)

            for box, cls, track_id in zip(boxes, clss, track_ids):
                # Draw bounding box and label
                annotator.box_label(box, color=colors(int(cls), True), label=names[int(cls)])

                # Store tracking history
                track = track_history[track_id]
                track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                if len(track) > 30:
                    track.pop(0)

                # Plot tracking points
                points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                cv2.circle(frame, track[-1], 7, colors(int(cls), True), -1)
                cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)

                # Check for specific class (assuming class 0 is the object of interest)
                if cls == 0:  # Adjust based on your object of interest
                    send_to_arduino('detected')
                    detected = True

            if not detected:
                send_to_arduino('not_detected')
        else:
            send_to_arduino('not_detected')

        # Write the frame to the output video
        result.write(frame)

        # Display the frame (optional)
        cv2.imshow('Object Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Release resources
    if arduino.is_open:
        arduino.close()
    result.release()
    cap.release()
    cv2.destroyAllWindows()
    print("Serial connection closed.")
