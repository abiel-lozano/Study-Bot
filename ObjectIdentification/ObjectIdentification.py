# Study-Bot: Object Identification
# Do not run, too many false positives and negatives, this is only for future reference

import cv2
import numpy as np

# Load the reference image of each model
modelTemplate1 = cv2.imread("D:\Edumakers\Study-Bot\ObjectIdentification\images\webcam-pics\modelTemplate1.jpg", 0)
modelTemplate2 = cv2.imread("D:\Edumakers\Study-Bot\ObjectIdentification\images\webcam-pics\modelTemplate2.jpg", 0)
modelTemplate3 = cv2.imread("D:\Edumakers\Study-Bot\ObjectIdentification\images\webcam-pics\modelTemplate3.jpg", 0)
modelTemplate4 = cv2.imread("D:\Edumakers\Study-Bot\ObjectIdentification\images\webcam-pics\modelTemplate4.jpg", 0)
modelTemplate5 = cv2.imread("D:\Edumakers\Study-Bot\ObjectIdentification\images\webcam-pics\modelTemplate5.jpg", 0)

modelTemplate1 = modelTemplate1.astype(np.uint8)
modelTemplate2 = modelTemplate2.astype(np.uint8)
modelTemplate3 = modelTemplate3.astype(np.uint8)
modelTemplate4 = modelTemplate4.astype(np.uint8)
modelTemplate5 = modelTemplate5.astype(np.uint8)


# print("modelTemplate1: ")
# print(modelTemplate1.dtype)

# Capture and process video
# To use the default camera, use index 0
capture = cv2.VideoCapture(0)

modelColors = {
    'model1': ((334, 59, 79), (333, 58, 61)),
    'model2': ((8, 78, 65), (1, 67, 27)),
    'model3': ((206, 58, 59), (213, 81, 26)),
    'model4': ((82, 15, 57), (74, 36, 24)),
    'model5': ((345, 77, 33), (343, 74, 17))
}

while True:
	ret, frame = capture.read()
	if not ret:
		print('Video capture failed! :(')
		exit()

	# Convert the frame to grayscale
	grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# for model, (lower, upper) in modelColors.items():
	# 	mask = cv2.inRange(grayFrame, lower, upper)
	# 	mask = cv2.erode(mask, None, iterations=2)
	# 	mask = cv2.dilate(mask, None, iterations=2)
		
	# 	# Find contours in the mask
	# 	contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# 	if len(contours) > 0:
	# 		print(f'{model} detected')

	# Perform template matching for each model
	result1 = cv2.matchTemplate(grayFrame, modelTemplate1, cv2.TM_CCORR_NORMED)
	result2 = cv2.matchTemplate(grayFrame, modelTemplate2, cv2.TM_CCORR_NORMED)
	result3 = cv2.matchTemplate(grayFrame, modelTemplate3, cv2.TM_CCORR_NORMED)
	result4 = cv2.matchTemplate(grayFrame, modelTemplate4, cv2.TM_CCORR_NORMED)
	result5 = cv2.matchTemplate(grayFrame, modelTemplate5, cv2.TM_CCORR_NORMED)
	# result6 = cv2.matchTemplate(correctedColorFrame, modelTemplate6, cv2.TM_CCORR_NORMED)

	threshold = 0.992 # Adjust this value to change the sensitivity of the detection

	# Check if the result is above the threshold
	if np.max(result1) > threshold:
		print('Model 1 detected')
	elif np.max(result2) > threshold:
		print('Model 2 detected')
	elif np.max(result3) > threshold:
		print('Model 3 detected')
	elif np.max(result4) > threshold:
		print('Model 4 detected')
	elif np.max(result5) > threshold:
		print('Model 5 detected')
	else:
		print('No model detected')

# capture.release()