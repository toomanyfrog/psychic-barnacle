import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv
from matplotlib import pyplot as plt


class TemplateMatch:
    #match_method = cv.CV_TM_SQDIFF
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


    def match(self, img, template, meth=methods[1]):
        method = eval(meth)
        w, h = template.shape[::-1]

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()



# v = Vision()
# logo = cv2.imread('imgs/testlogo2.jpg',0)
# shoe1 = cv2.imread('imgs/shoe.jpg',0)
# shoe2 = cv2.imread('imgs/shoe2.png',0)
# v.match(shoe1, logo)
