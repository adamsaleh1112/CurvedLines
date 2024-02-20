# IMPORT NUMPY AND CV2
import numpy as np # importing numpy, a library that allows for complex data structures
import cv2 # importing opencv, a image processing library for python

# VIDEO = VIDEO CAPTURE
vid = cv2.VideoCapture(0) # setting vid equal to index 0 capture (default webcam)

# WHILE TRUE
while (True):

    # IMAGE PROCESSING
    ret, img = vid.read()
    kernel = np.ones((1, 1), np.uint8)
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
    lines = cv2.HoughLinesP(maskimg, rho=1, theta=np.pi / 180, threshold=10, minLineLength=5, maxLineGap=10)

    # IF LINES NOT NONE
    if lines is not None:

        midlines = []  # List to store midlines between lines

        # FOR LINE IN LINES
        for line1 in lines:
            x1_1, y1_1, x2_1, y2_1 = line1[0]

            if x2_1 - x1_1 == 0:
                slope_1 = 100
            else:
                slope_1 = (y2_1 - y1_1) / (x2_1 - x1_1)

            cv2.line(img, (x1_1, y1_1), (x2_1, y2_1), (255, 0, 0), 6)

            for line2 in lines:
                x1_2, y1_2, x2_2, y2_2 = line2[0]

                if x2_2 - x1_2 == 0:
                    slope_2 = 100
                else:
                    slope_2 = (y2_2 - y1_2) / (x2_2 - x1_2)

                slopedifference = abs(slope_2 - slope_1)

                if slopedifference > 0.2:
                    pass
                else:
                    mid_x1 = int((x1_1 + x1_2) / 2)
                    mid_y1 = int((y1_1 + y1_2) / 2)
                    mid_x2 = int((x2_1 + x2_2) / 2)
                    mid_y2 = int((y2_1 + y2_2) / 2)

                    midlines.append(((mid_x1, mid_y1), (mid_x2, mid_y2)))

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

