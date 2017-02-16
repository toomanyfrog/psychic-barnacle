import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv
from colourmatch import ColourMatch

# look at the photo
# identify coloured circles
# find pattern (red blue green magenta)
# use contours to find a centroid
# use the centroids to compute a homography



cm = ColourMatch()

def calibrate():
    img = cv2.imread("imgs/dark.jpg")
    contours = []
    centroids = []
    for colour_index in range(0,4):
        mask = cm.threshold_colour(cm.img, colour_index)
        blurred = cv2.GaussianBlur(mask,(49,49),0)
        cv2.imshow('b', blurred)
        cv2.waitKey(0)
        #cm.getCircles(a)
        contours.append(cm.get_contours(blurred))

    for c in contours:
        # compute the center of the contour
    	M = cv2.moments(c)
    	cX = int(M["m10"] / M["m00"])
    	cY = int(M["m01"] / M["m00"])
        centroids.append((cX, cY))

        # draw the contour and center of the shape on the image
        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(img, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # show the image
        cv2.imshow("Image", img)
        cv2.waitKey(0)

    #TODO: find homography from four points
        # take photo of (new) calibration img projected on wall
        # find homography from camera image to original
        # apply transform




calibrate()
