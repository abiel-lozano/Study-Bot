# Script to test ArUco markers asociated with educational objects
# 

import cv2
import time

def detectMarkers(aruco_dict):
    obj = 'User is not holding any objects'

    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    start = time.time()
    elapsedTime = 0

    # Chemical compounds
    compoundDict = {
        0: 'Citrate',
        1: 'Isocitrate',
        2: 'Alpha-Ketoglutarate',
        3: 'Succinyl CoA',
        4: 'Succinate',
        5: 'Fumarate',
        6: 'Malate',
        7: 'Oxaloacetate'
    }

    # Try and detect markers for 5 seconds
    while elapsedTime < 5:
        ret, frame = cap.read()

        if not ret:
            print('Failed to capture frame.')
            break

        # Convert the frame to grayscale for marker detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect markers
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict)

        if ids is not None:
            # For each marker found in current frame, print ID
            for i in range(len(ids)):
                print('Detected marker with ID:', ids[i][0])

                try:
                    # Try to get the name of the object associated with the marker
                    compoundName = compoundDict[ids[i][0]]
                    print('Object:', compoundName)
                    
                    # Append compound to list while avoiding repeats
                    if obj == 'User is not holding any objects':
                        obj = compoundName
                    elif compoundName not in obj:
                        obj += ', ' + compoundName
                # If marker ID is not registered, print error message
                except KeyError:
                    print('Exception: Marker ID' + str(ids[i][0]) + ' not registered.')

        # Display the frame
        cv2.imshow('Frame', frame)

        elapsedTime = time.time() - start

        # Check for 'Esc' key press
        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    print('\n----------------------------------------\n')
    print('Objects held by user:', obj)

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detectMarkers(arucoDict)