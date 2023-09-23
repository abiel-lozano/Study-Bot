# Study-Bot: Color Detection for Human Body Models
# Based on the tutorial by goodday451999, posted on GeeksforGeeks: https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/

import numpy as np
import cv2

# Capture video
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.CAP_PROP_FPS, 60)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Color ranges
stomachLower = np.array([90, 	80, 		100			], np.uint8)
stomachUpper = np.array([120, 	255, 		255			], np.uint8)
colonLower = np.array(	[10, 	255 * 0.55, 255 * 0.35	], np.uint8)
colonUpper = np.array(	[20.5, 	255, 		255			], np.uint8)
liverLower = np.array(	[38, 	225 * 0.22, 255 * 0.38	], np.uint8)
liverUpper = np.array(	[41, 	255, 		255			], np.uint8)
brainLower = np.array(	[163, 	255 * 0.50, 255 * 0.40	], np.uint8)
brainUpper = np.array(	[163, 	255, 		255			], np.uint8)
kidneyLower = np.array(	[24, 	255 * 0.60, 255 * 0.49	], np.uint8)
kidneyUpper = np.array(	[24, 	255, 		255			], np.uint8)
heartLower = np.array(	[170, 	255 * 0.50, 255 * 0.35	], np.uint8)
heartUpper = np.array(	[170, 	255 * 0.97, 255 * 0.69	], np.uint8)

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

    # For colon
    # Dilate the mask: Remove holes in the mask by adding pixels to the boundaries of objects in the mask
    colonMask = cv2.dilate(colonMask, kernel)
    # Apply the mask to the frame using a bitwise AND operation
    resColon = cv2.bitwise_and(imageFrame, imageFrame, mask=colonMask)

    # For liver
    liverMask = cv2.dilate(liverMask, kernel)
    resliver = cv2.bitwise_and(imageFrame, imageFrame, mask=liverMask)

    # For stomach
    stomachMask = cv2.dilate(stomachMask, kernel)
    resStomach = cv2.bitwise_and(imageFrame, imageFrame, mask=stomachMask)

    # For brain
    brainMask = cv2.dilate(brainMask, kernel)
    resBrain = cv2.bitwise_and(imageFrame, imageFrame, mask=brainMask)

    # For heart
    heartMask = cv2.dilate(heartMask, np.ones((12, 12), "uint8"))
    resHeart = cv2.bitwise_and(imageFrame, imageFrame, mask=heartMask)
    
    # For kidney use a more aggressive kernel for dilation
    kidneyMask = cv2.dilate(kidneyMask, np.ones((12, 12), "uint8"))
    resKidney = cv2.bitwise_and(imageFrame, imageFrame, mask=kidneyMask)

    # Create a contour around the zone that matches the color range
    contours, hierarchy = cv2.findContours(colonMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    # For each contour, check if the area is greater than 500 pixels
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 700:
            # Create a bounding rectangle with a title around the detected object
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 120, 255), 2)
            # cv2.putText(imageFrame, "COLON", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 120, 255))
            # print("Colon detected")

    contours, hierarchy = cv2.findContours(liverMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (86, 194, 0), 2)
            # cv2.putText(imageFrame, "LIVER", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (86, 194, 0))
            # print("Liver detected")

    contours, hierarchy = cv2.findContours(stomachMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1400:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (237, 117, 47), 2)
            # cv2.putText(imageFrame, "STOMACH", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (237, 117, 47))
            # print("Stomach detected")

    contours, hierarchy = cv2.findContours(brainMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 2500:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (204, 0, 255), 2)
            # cv2.putText(imageFrame, "BRAIN", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255))
            # print("Brain detected")

    contours, hierarchy = cv2.findContours(kidneyMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 50:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            # cv2.putText(imageFrame, "KIDNEY", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255))
            # print("Kidney detected")

    contours, hierarchy = cv2.findContours(heartMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 650:
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv2.putText(imageFrame, "HEART", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0))
            # print("Heart detected")

    # Display camera feed
    cv2.imshow("Color-Based Object Detection", imageFrame)

    # Close the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cam.release()
cv2.destroyAllWindows()