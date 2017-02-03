
import numpy as np
import numpy.linalg as la
import cv2
import cv2.cv as cv

class SiftMatch:
    texCoords = [1,1,1,1]
    imgPoints = []


    def correctFromCamImg(self):
        imageA=cv2.imread("imgs/dragging.jpg")
        imageB=cv2.imread("imgs/dia.jpg")

        h= self.getHomo([imageB, imageA], showMatches=True)
        for i in range(len(self.imgPoints)):
        	point = [self.imgPoints[i][0], self.imgPoints[i][1], 1]
        	#dest = np.dot(A, point)
        	dest = self.getDest(point, h)
        	self.imgPoints[i] = [dest[0][0], dest[0][1]]
        	self.texCoords[i] = dest[1]

    def getDest(self, source, transform):
    	s = np.array([source[0], source[1], 1]) #homogeneous
    	t = np.dot(transform, s)
    	return np.array([[t[0]/t[2], t[1]/t[2]], t[2]])


    def getHomo(self, images, ratio=0.75, reprojThresh=4.0,showMatches=False):
        # unpack the images, then detect keypoints and extract
        # local invariant descriptors from them
        (imageB, imageA) = images

        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)

        # match features between the two images
        M = self.matchKeypoints(kpsA, kpsB,
            featuresA, featuresB, ratio, reprojThresh)
        (matches, H, status) = M
        return H

    def detectAndDescribe(self, image):
		# convert the image to grayscale
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # detect keypoints in the image
                detector = cv2.FeatureDetector_create("SIFT")
                kps = detector.detect(gray)

                # extract features from the image
                extractor = cv2.DescriptorExtractor_create("SIFT")
                (kps, features) = extractor.compute(gray, kps)

		# convert the keypoints from KeyPoint objects to NumPy
		# arrays
		kps = np.float32([kp.pt for kp in kps])

		# return a tuple of keypoints and features
		return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,ratio, reprojThresh):
		# compute the raw matches and initialize the list of actual
		# matches
		matcher = cv2.DescriptorMatcher_create("BruteForce")
		rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
		matches = []

		# loop over the raw matches
		for m in rawMatches:
			# ensure the distance is within a certain ratio of each
			# other (i.e. Lowe's ratio test)
			if len(m) == 2 and m[0].distance < m[1].distance * ratio:
				matches.append((m[0].trainIdx, m[0].queryIdx))

		# computing a homography requires at least 4 matches
		if len(matches) > 4:
			# construct the two sets of points
			ptsA = np.float32([kpsA[i] for (_, i) in matches])
			ptsB = np.float32([kpsB[i] for (i, _) in matches])

			# compute the homography between the two sets of points
			(H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
				reprojThresh)

			# return the matches along with the homograpy matrix
			# and status of each matched point
			return (matches, H, status)

		# otherwise, no homograpy could be computed
		return None
