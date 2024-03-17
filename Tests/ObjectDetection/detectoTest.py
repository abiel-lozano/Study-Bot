import cv2
import torch
from detecto.core import Model

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load pretrained model (for example, Faster R-CNN) and move it to the appropriate device
model = Model(device=device)

# Access webcam
cap = cv2.VideoCapture(0)  # 0 for the first webcam

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Perform object detection
    labels, boxes, scores = model.predict(frame)
    
    # Draw bounding boxes
    for label, box, score in zip(labels, boxes, scores):
        # if the score is above 0.8, draw the bounding box
        if score > 0.8:
            xMin, yMin, xMax, yMax = box
            xMin, yMin, xMax, yMax = int(xMin), int(yMin), int(xMax), int(yMax) # Convert to integers
            confidence = round(float(score), 2)
            if confidence > 0.5:  # Adjust threshold as needed
                cv2.rectangle(frame, (xMin, yMin), (xMax, yMax), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {confidence}', (xMin, yMin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    
    # Display the resulting frame
    cv2.imshow('Object Detection', frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
