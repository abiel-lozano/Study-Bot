import cv2

def detectMarkers(aruco_dict):
    cap = cv2.VideoCapture(0)

    while True:
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

        cv2.imshow('Frame', frame)
        # Check for 'Esc' key press
        key = cv2.waitKey(10) & 0xFF
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detectMarkers(aruco_dict)