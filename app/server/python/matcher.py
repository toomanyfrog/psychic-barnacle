import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv
from colourmatch import ColourMatch
import sys

# look at the photo
# identify coloured circles
# find pattern (red blue green magenta)
# use contours to find a centroid
# use the centroids to compute a homography

# ==========================================

# find cyan circles - these are the ends of the projection


def calibrate(cm, original_image, original_centers, filepath, filename):
    print "filepath: " + filepath
    img = cv2.imread(filepath)
    height, width = img.shape[:2]
    corners = [[0,0], [width, 0], [height,width], [0, height]]

    #cv2.imshow('a', img)
    #cv2.waitKey(0)
    contours = []
    centroids = []
    for colour_index in range(0,4):
        mask = cm.threshold_colour(img, colour_index)
        blurred = cv2.GaussianBlur(mask,(49,49),0)
        #cv2.imshow('b', blurred)
        #cv2.waitKey(0)
        #cm.getCircles(a)
        contours.append(cm.get_contours(blurred))

    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centroids.append([cX, cY])

        # draw the contour and center of the shape on the image
        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(img, "center", (cX - 20, cY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # show the image
        #cv2.imshow("Image", img)
        #cv2.waitKey(0)

    new_points = []
    transform = sourceToDest(centroids, original_centers)
    out_2 = cv.fromarray(np.zeros((1000,1000,3),np.uint8))
    cv.WarpPerspective(cv.fromarray(original_image), out_2, cv.fromarray(transform))
    #cv.ShowImage("test", out_2)
    cv.SaveImage(filename, out_2)
    cv2.waitKey()
    # cv2.warpPerspective(original_image, transform, dsize[, dst[, flags[, borderMode[, borderValue]]]])
    # for x in range(4):
    #     new_p getDest(original_centers[x], transform)


    #TODO: find homography from four points
        # take photo of (new) calibration img projected on wall
        # find homography from camera image to original
        # apply transform


def scaleByCoeff(point1, point2, point3, point4):
    a = np.array([[point1[0], point2[0], point3[0]], [point1[1], point2[1], point3[1]], [1,1,1]])
    b = np.array([point4[0],point4[1], 1])
    x = np.linalg.solve(a,b) #coefficients
    A = np.array([[x[0]*point1[0], x[1]*point2[0], x[2]*point3[0]],
                 [x[0]*point1[1], x[1]*point2[1], x[2]*point3[1]],
                 x.transpose()])
    return A

def adjoint(A):
    return np.array([[A[1,1]*A[2,2]-A[1,2]*A[2,1], A[0,2]*A[2,1]-A[0,1]*A[2,2], A[0,1]*A[1,2]-A[0,2]*A[1,1]],
                     [A[1,2]*A[2,0]-A[1,0]*A[2,2], A[0,0]*A[2,2]-A[0,2]*A[2,0], A[0,2]*A[1,0]-A[0,0]*A[1,2]],
                     [A[1,0]*A[2,1]-A[1,1]*A[2,0], A[0,1]*A[2,0]-A[0,0]*A[2,1], A[0,0]*A[1,1]-A[0,1]*A[1,0]]])

def sourceToDest(source,dest):
    basisToSource = scaleByCoeff(source[0], source[1], source[2], source[3])
    sourceToBasis = adjoint(basisToSource)
    basisToDest = scaleByCoeff(dest[0],dest[1],dest[2],dest[3])
    a = np.dot(basisToDest, sourceToBasis)
    print "a", a
    return a

def getDest(source, transform):
    s = np.array([source[0], source[1], 1]) #homogeneous
    t = np.dot(transform, s)
    print transform, s
    return np.array([[t[0]/t[2], t[1]/t[2]], t[2]])




def main():
    filepath = sys.argv[1] #read_in()
    filename = sys.argv[2]
    cm = ColourMatch()
    original_image = cv2.imread("test2.jpg")
    original_centers = [[436, 101], [110, 251], [429, 247], [266, 98]]
    calibrate(cm, original_image, original_centers, filepath, filename)


if __name__ == '__main__':
    main()
