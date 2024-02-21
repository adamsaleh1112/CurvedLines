# IMPORT NUMPY AND CV2
import numpy as np # importing numpy, a library that allows for complex data structures
import cv2 # importing opencv, a image processing library for python

# VIDEO = VIDEO CAPTURE
vid = cv2.VideoCapture(0) # setting vid equal to index 0 capture (default webcam)

# WHILE TRUE
while (True):

    # IMAGE PROCESSING
    ret, img = vid.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)

    # INITIALIZE VARS FOR MASK
    x = 150
    y = 100
    w = 350
    h = 250
    mask = np.zeros(edges.shape[:2], np.uint8)
    mask[y:y + h, x:x + w] = 255
    maskimg = cv2.bitwise_and(edges, edges, mask=mask)

    # DETECT LINES
    lines = cv2.HoughLinesP(maskimg, rho=1, theta=np.pi / 180, threshold=5, minLineLength=15, maxLineGap=20)


    # IF LINES NOT NONE
    if lines is not None:

        midlines = []  # List to store midlines between lines


        # FOR LINE IN LINES
        for line1 in lines:
            x1_1, y1_1, x2_1, y2_1 = line1[0]

            if x2_1 - x1_1 == 0:
                slope1 = 100
            else:
                slope1 = (y2_1 - y1_1) / (x2_1 - x1_1)

            cv2.line(img, (x1_1, y1_1), (x2_1, y2_1), (255, 0, 0), 6)


            for line2 in lines:
                x1_2, y1_2, x2_2, y2_2 = line2[0]

                if x2_2 - x1_2 == 0:
                    slope2 = 100
                else:
                    slope2 = (y2_2 - y1_2) / (x2_2 - x1_2)

                slopedifference = abs(slope2 - slope1)

                if slopedifference > 0.2:
                    pass
                else:
                    x1avg = int((x1_1 + x1_2) / 2)
                    y1avg = int((y1_1 + y1_2) / 2)
                    x2avg = int((x2_1 + x2_2) / 2)
                    y2avg = int((y2_1 + y2_2) / 2)

                    midlines.append(((x1avg, y1avg), (x2avg, y2avg)))


        # DRAW MIDLINES
        for midline in midlines:
            cv2.line(img, midline[0], midline[1], (255, 0, 0), 4)

        # HIGHLIGHT MASK WITH RECTANGLE
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()


# PROGRAMMING WORKS CITED

# Video capture and video display (Lines 1-12, 77-88) https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
# Hough Lines detection (Lines 28, 32, 39, 50) https://docs.opencv.org/4.x/d6/d10/tutorial_py_houghlines.html
# Masking (Lines 18-25): https://stackoverflow.com/questions/11492214/opencv-via-python-is-there-a-fast-way-to-zero-pixels-outside-a-set-of-rectangle
# OpenCV rectangle (Line 75) https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
# OpenCV line (Lines 46, 72) https://www.geeksforgeeks.org/python-opencv-cv2-line-method/
