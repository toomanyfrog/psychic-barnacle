import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv

# 1) project patterns
# 2) compare with photo
# 3) template matching
# 4) obtain local homography
# 5) apply homography to specified image

patterns, display = [], []

def readImgs():
    global patterns, display
    #calibration images
    patterns.append(cv2.imread('patterns/pat1.jpg',  0))
    patterns.append(cv2.imread('patterns/pat2.jpg',  0))
    patterns.append(cv2.imread('patterns/pat3.jpg',  0))
    patterns.append(cv2.imread('patterns/pat4.jpg',  0))
    patterns.append(cv2.imread('patterns/patall.jpg',0))

    #display images
    # TODO: add support for video
    display = cv2.imread('display/display.jpg', 0)


def projectPatterns(patterns):
    cv2.imshow(patterns[-1])
    cv2.waitKey(0)
