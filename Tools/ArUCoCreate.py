# Script creates ArUco markers of a given size and number
# Images are dumped in the working directory, move them later

# Size: size of the generated images in pixels, image is 1:1 (min 6, recommended 300)
# Number: number of markers to generate (max 50)

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