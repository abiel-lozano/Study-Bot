import cv2
import time

def detectMarkers(aruco_dict):
    obj = 'User is not holding any objects'

    cap = cv2.VideoCapture(0)

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
            for i in range(len(ids)):

                print('Detected marker with ID:', ids[i][0])
                try:
                    compound_name = compoundDict[ids[i][0]]
                    print('Object:', compound_name)
                    
                    if obj == 'User is not holding any objects':
                        obj = compound_name
                    elif compound_name not in obj:
                        obj += ', ' + compound_name
                except KeyError:
                    print('Exception: Marker ID' + str(ids[i][0]) + ' not registered.')

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