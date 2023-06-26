import cv2
import numpy as np


# Load the reference image of each model
modelTemplate1 = cv2.imread("D:\Study-Bot\ObjectIdentification\images\modelTemplate1.jpg", 0)
modelTemplate2 = cv2.imread("D:\Study-Bot\ObjectIdentification\images\modelTemplate2.jpg", 0)
modelTemplate3 = cv2.imread("D:\Study-Bot\ObjectIdentification\images\modelTemplate3.jpg", 0)
modelTemplate4 = cv2.imread("D:\Study-Bot\ObjectIdentification\images\modelTemplate4.jpg", 0)
modelTemplate5 = cv2.imread("D:\Study-Bot\ObjectIdentification\images\modelTemplate5.jpg", 0)

# modelTemplate1 = modelTemplate1.astype(np.uint8)
# modelTemplate2 = modelTemplate2.astype(np.uint8)
# modelTemplate3 = modelTemplate3.astype(np.uint8)
# modelTemplate4 = modelTemplate4.astype(np.uint8)
# modelTemplate5 = modelTemplate5.astype(np.uint8)
# modelTemplate6 = modelTemplate6.astype(np.uint8)


# print("modelTemplate1: ")
# print(modelTemplate1.dtype)

# Capture and process video
# To use the default camera, use index 0
capture = cv2.VideoCapture(0)

modelColors = {
    'model1': ((7, 100, 42), (15, 99, 70)),
    'model2': ((202, 98, 42), (200, 96, 55)),
    'model3': ((65,76,29), (59, 30, 62)),
    'model4': ((6, 89,22), (10, 89, 48)),
    'model5': ((348, 82, 52), (347, 72, 77))
}

while True:
	ret, frame = capture.read()
	if not ret:
		print('Video capture failed! :(')
		exit()

	# Convert the frame to grayscale
	# grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	for model, (lower, upper) in modelColors.items():
		mask = cv2.inRange(hsvFrame, lower, upper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		
		# Find contours in the mask
		contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		if len(contours) > 0:
			print(f'{model} detected')

	# Perform template matching for each model
	# result1 = cv2.matchTemplate(hsvFrame, modelTemplate1, cv2.TM_CCORR_NORMED)
	# result2 = cv2.matchTemplate(hsvFrame, modelTemplate2, cv2.TM_CCORR_NORMED)
	# result3 = cv2.matchTemplate(hsvFrame, modelTemplate3, cv2.TM_CCORR_NORMED)
	# result4 = cv2.matchTemplate(hsvFrame, modelTemplate4, cv2.TM_CCORR_NORMED)
	# result5 = cv2.matchTemplate(hsvFrame, modelTemplate5, cv2.TM_CCORR_NORMED)
	# result6 = cv2.matchTemplate(correctedColorFrame, modelTemplate6, cv2.TM_CCORR_NORMED)

	# threshold = 0.965 # Adjust this value to change the sensitivity of the detection

	# Check if the result is above the threshold
	# if np.max(result1) > threshold:
	# 	print('Model 1 detected')
	# elif np.max(result2) > threshold:
	# 	print('Model 2 detected')
	# elif np.max(result3) > threshold:
	# 	print('Model 3 detected')
	# elif np.max(result4) > threshold:
	# 	print('Model 4 detected')
	# elif np.max(result5) > threshold:
	# 	print('Model 5 detected')
	# elif np.max(result6) > threshold:
	# 	print('Blank model detected')
	# else:
	# 	print('No model detected')

capture.release()