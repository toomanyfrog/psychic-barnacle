import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv

class ColourMatch:
    img = cv2.imread("imgs/huetest.jpg")

    def thresholdColour(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # lower mask (0-10)
        lower_red = np.array([0,100,100])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

        # join my masks
        mask = mask0+mask1

        # set my output img to zero everywhere except my mask
        output_img = img.copy()
        output_img[np.where(mask==0)] = 0
        output_img[np.where(mask==1)] = 1

        # cv2.imshow('img',mask)
        # cv2.waitKey(0)

        return mask

        # or your HSV image, which I *believe* is what you want
        # output_hsv = img_hsv.copy()
        # output_hsv[np.where(mask==0)] = 0

    def getCircles(self, image):
        output = image.copy()
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect circles in the image
    #    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 2, 5)
        circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1, 1, 200, 100)

        print 'hi'
        # ensure at least some circles were found
        if circles is not None:
            print 'hi2'
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
            	# draw the circle in the output image, then draw a rectangle
            	# corresponding to the center of the circle
            	cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            	cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # show the output image
            cv2.imshow("output", np.hstack([image, output]))
            cv2.waitKey(0)

cm = ColourMatch()
m = cm.thresholdColour(cm.img)
a = cv2.GaussianBlur(cv2.imread("imgs/huetest.jpg",0),(5,5),0)
cm.getCircles(a)
