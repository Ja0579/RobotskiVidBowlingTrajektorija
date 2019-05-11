import numpy as np
import math
import cv2 as cv
from PIL import Image


def nothing(x):
    pass

cv.namedWindow("Win", cv.WINDOW_NORMAL)

cv.createTrackbar("1", "Win", 0, 640, nothing)
cv.createTrackbar("2", "Win", 0, 480, nothing)
cv.createTrackbar("3", "Win", 0, 640, nothing)
cv.createTrackbar("4", "Win", 0, 480, nothing)
cv.createTrackbar("5", "Win", 0, 640, nothing)
cv.createTrackbar("6", "Win", 0, 480, nothing)
cv.createTrackbar("7", "Win", 0, 640, nothing)
cv.createTrackbar("8", "Win", 0, 480, nothing)

vid = cv.VideoCapture(0)

while True:
    #img = cv.imread("slika1.jpg")
    ret, frame = vid.read()

    x1 = cv.getTrackbarPos("1", "Win")
    x2 = cv.getTrackbarPos("2", "Win")
    x3 = cv.getTrackbarPos("3", "Win")
    x4 = cv.getTrackbarPos("4", "Win")
    x5 = cv.getTrackbarPos("5", "Win")
    x6 = cv.getTrackbarPos("6", "Win")
    x7 = cv.getTrackbarPos("7", "Win")
    x8 = cv.getTrackbarPos("8", "Win")
      
    poly = np.array([[[x1,x2],[x3,x4],[x5,x6],[x7,x8]]], dtype=np.int32)  
    poly = cv.fillPoly(frame, poly, 255)

    cv.imshow("Maska", poly)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows

cv.waitKey(0)
cv.destroyAllWindows()


