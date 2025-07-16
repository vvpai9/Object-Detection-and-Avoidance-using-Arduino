import cv2
import numpy as np
import requests
from ultralytics import YOLO
from collections import defaultdict
from ultralytics.utils.plotting import Annotator, colors

# Connect to Arduino via WiFi
arduino_ip = "192.168.137.157"  # Replace with your Arduino's IP
url = f"http://{arduino_ip}/command"

def send_command(command):
    response = requests.get(f"{url}?cmd={command}")
    print(f"Sent command: {command}, Response: {response.text}")

# Initialize tracking history
track_history = defaultdict(lambda: [])

# Load the YOLO model
model = YOLO("yolov8n.pt")
names = model.model.names

# Connect to ESP32CAM (assuming it's accessible via local webcam index)
cap = cv2.VideoCapture(1)  # Replace with your ESP32CAM IP if different
print ("Camera On")
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
        target_center_x = None
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
                center_x = int((box[0] + box[2]) / 2)
                center_y = int((box[1] + box[3]) / 2)
                track.append((center_x, center_y))
                if len(track) > 30:
                    track.pop(0)

                # Plot tracking points
                points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                cv2.circle(frame, track[-1], 7, colors(int(cls), True), -1)
                cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)

                # Check for specific class (assuming class 0 is the object of interest)
                if cls == 0:  # Adjust based on your object of interest
                    target_center_x = center_x
                    detected = True

            if detected:
                # Determine movement direction based on object's position
                if target_center_x is not None:
                    frame_center_x = w // 2
                    threshold = w // 10  # Define a threshold for central region
                    if target_center_x < frame_center_x - threshold:
                        print ("Left")
                        send_command('l')  # Move left
                    elif target_center_x > frame_center_x + threshold:
                        print ("Right")
                        send_command('r')  # Move right
                    else:
                        print ("Forward")
                        send_command('f')  # Move forward
            else:
                print ("Not Detected")
                send_command('s')  # Stop if object not detected
        else:
            print ("Stop")
            send_command('s')  # Stop if no object is detected

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
    result.release()
    cap.release()
    cv2.destroyAllWindows()
    print("Serial connection closed.")
