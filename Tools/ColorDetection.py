# Script for color-based object detection
# Based on the tutorial by goodday451999, posted on GeeksforGeeks: https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/
# Use this to determine the color ranges for the objects to detect

import numpy as np
import cv2

# Capture video
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FPS, 60)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Color ranges           Hue 	Saturation  Value
stomachLower = np.array([90, 	80, 		100			], np.uint8)
stomachUpper = np.array([120, 	255, 		255			], np.uint8)
colonLower = np.array(	[10, 	255 * 0.55, 255 * 0.35	], np.uint8)
colonUpper = np.array(	[19.5, 	255, 		255			], np.uint8)
liverLower = np.array(	[38, 	225 * 0.22, 255 * 0.38	], np.uint8)
liverUpper = np.array(	[41, 	255, 		255			], np.uint8)
brainLower = np.array(	[161, 	255 * 0.50, 255 * 0.40	], np.uint8)
brainUpper = np.array(	[161, 	255, 		255			], np.uint8)
kidneyLower = np.array(	[26, 	255 * 0.60, 255 * 0.69	], np.uint8)
kidneyUpper = np.array(	[26, 	255, 		255			], np.uint8)
heartLower = np.array(	[177, 	255 * 0.50, 255 * 0.35	], np.uint8)
heartUpper = np.array(	[177, 	255 * 0.97, 255 * 0.69	], np.uint8)

while True:
    # Reading the video from the webcam in image frames
    _, imageFrame = cam.read()

    # Convert the frame from BGR color space to HSV color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set color ranges of the objects and define masks

    # Masks
    colonMask = cv2.inRange(hsvFrame, colonLower, colonUpper)
    liverMask = cv2.inRange(hsvFrame, liverLower, liverUpper)
    stomachMask = cv2.inRange(hsvFrame, stomachLower, stomachUpper)
    brainMask = cv2.inRange(hsvFrame, brainLower, brainUpper)
    kidneyMask = cv2.inRange(hsvFrame, kidneyLower, kidneyUpper)
    heartMask = cv2.inRange(hsvFrame, heartLower, heartUpper)

    # Create a 5x5 square-shaped filter called kernel
    # The filter is filled with ones and will be used for morphological transformations such as dilation for better detection
    kernel = np.ones((5, 5), "uint8")
    # Dilate the mask: Remove holes in the mask by adding pixels to the boundaries of objects in the mask
    colonMask = cv2.dilate(colonMask, kernel)
    stomachMask = cv2.dilate(stomachMask, kernel)
    brainMask = cv2.dilate(brainMask, kernel)
    # Use a larger filter for liver, heart, and kidney masks
    liverMask = cv2.dilate(liverMask, np.ones((12, 12), "uint8"))
    heartMask = cv2.dilate(heartMask, np.ones((13, 13), "uint8"))
    kidneyMask = cv2.dilate(kidneyMask, np.ones((12, 12), "uint8"))
    # Create a contour around the zone that matches the color range
    contours, _ = cv2.findContours(colonMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    # For each contour, check if the area is greater than 500 pixels
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 700:
            # Create a bounding rectangle with a title around the detected object
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 120, 255), 2)

    contours, _ = cv2.findContours(liverMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1300:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (86, 194, 0), 2)

    contours, _ = cv2.findContours(stomachMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1400:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (237, 117, 47), 2)

    contours, _ = cv2.findContours(brainMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 3000:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (204, 0, 255), 2)

    contours, _ = cv2.findContours(kidneyMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 50:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 255), 2)

    contours, _ = cv2.findContours(heartMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for _, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1400:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Display camera feed
    cv2.imshow("Color-Based Object Detection", imageFrame)

    # Close the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cam.release()
cv2.destroyAllWindows()