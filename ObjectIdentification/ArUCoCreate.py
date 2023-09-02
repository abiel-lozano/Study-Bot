# Script creates ArUco markers of a given size and number

import cv2

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

markerSize = int(input('Marker size: '))
numMarkers = int(input('Markers to generate: '))
markerImgs = []

for markerID in range(numMarkers):
	markerImg = cv2.aruco.generateImageMarker(arucoDict, markerID, markerSize)
	cv2.imwrite('marker_{}.png'.format(markerID), markerImg)
	markerImgs.append(cv2.imread('marker_{}.png'.format(markerID)))

for markerImg in markerImgs:
	print('Dimensions: ', markerImg.shape)
	cv2.waitKey(0)