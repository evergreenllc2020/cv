import numpy as np
import cv2

def getAutoEdge(image, sigma=0.33):
	v = np.median(image)
	l = int(max(0, (1.0 - sigma) * v))
	u = int(min(255, (1.0 + sigma) * v))
	e = cv2.Canny(image, l, u)
	return e


cap = cv2.VideoCapture(0)
while True:
	_, frame =cap.read()
	gray = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.COLOR_BGR2GRAY)
	blur_img = cv2.GaussianBlur(gray, (3, 3), 0)
	laplacian = cv2.Laplacian(blur_img, cv2.CV_64F)

    # compute gradients along the X and Y axis, respectively
	gX = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0)
	gY = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1)
	#Normalize gX and gY
	gX = cv2.convertScaleAbs(gX)
	gY = cv2.convertScaleAbs(gY)
	sobel = cv2.addWeighted(gX, 0.5, gY, 0.5, 0)
	autocanny = getAutoEdge(blur_img)
	

	# compute the gradient magnitude and orientation respectively
	# compute gradients along the X and Y axis, respectively
	gX1 = cv2.Scharr(blur_img, ddepth=cv2.CV_64F, dx=1, dy=0)
	gY1 = cv2.Scharr(blur_img, ddepth=cv2.CV_64F, dx=0, dy=1)
	scharr = np.sqrt((gX1 ** 2) + (gY1 ** 2))

	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	cv2.namedWindow('Laplacian',cv2.WINDOW_NORMAL)
	cv2.namedWindow('Sobel',cv2.WINDOW_NORMAL)
	cv2.namedWindow('Scharr',cv2.WINDOW_NORMAL)
	cv2.namedWindow('Canny',cv2.WINDOW_NORMAL)

	cv2.resizeWindow('image', 800, 600)
	cv2.resizeWindow('Laplacian', 800, 600)
	cv2.resizeWindow('Sobel', 800, 600)
	cv2.resizeWindow('Scharr', 800, 600)
	cv2.resizeWindow('Canny', 800, 600)
	
	
	cv2.imshow("image", frame)
	cv2.imshow("Laplacian", laplacian)
	cv2.imshow("Sobel", sobel)
	cv2.imshow("Scharr", scharr)
	cv2.imshow("Canny", autocanny)
	
    
	k = cv2.waitKey(5) & 0xFF
	if k==27:
		break;

cv2.destroyAllWindows()
cap.release()