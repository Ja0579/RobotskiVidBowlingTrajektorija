import numpy as np
import math
import cv2 as cv
from PIL import Image


video = cv.VideoCapture(0)

def nothing(x):
    pass

cv.namedWindow("Win")

cv.createTrackbar("Lower_H", "Win", 0, 179, nothing)
cv.createTrackbar("Lower_S", "Win", 0, 255, nothing)
cv.createTrackbar("Lower_V", "Win", 0, 255, nothing)
cv.createTrackbar("Upper_H", "Win", 0, 179, nothing)
cv.createTrackbar("Upper_S", "Win", 0, 255, nothing)
cv.createTrackbar("Upper_V", "Win", 0, 255, nothing)

while True:

    ret, frame = video.read()

    poly1 = np.array([[[44,480],[146,0],[0,0],[0,480]]], dtype=np.int32)               #leva stran   
    poly = cv.fillPoly(frame, poly1, 0)
    poly2 = np.array([[[349,480],[203,0],[640,0],[640,480]]], dtype=np.int32)          #desna stran
    poly = cv.fillPoly(frame, poly2, 0)
    poly3 = np.array([[[0,0],[0,10],[640,10],[640,0]]], dtype=np.int32)                #zgori   parametr 4 in 6 
    poly = cv.fillPoly(frame, poly3, 0)
    poly4 = np.array([[[800,600],[0,600],[0,595],[800,595]]], dtype=np.int32)          #spodi    parametr 6 in 8   
    poly = cv.fillPoly(frame, poly4, 0)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    lower_h = cv.getTrackbarPos("Lower_H", "Win")
    lower_s = cv.getTrackbarPos("Lower_S", "Win")
    lower_v = cv.getTrackbarPos("Lower_V", "Win")
    upper_h = cv.getTrackbarPos("Upper_H", "Win")
    upper_s = cv.getTrackbarPos("Upper_S", "Win")
    upper_v = cv.getTrackbarPos("Upper_V", "Win")

    low_hsv = np.array([lower_h, lower_s, lower_v])
    up_hsv = np.array([upper_h, upper_s, upper_v])

    mask = cv.inRange(hsv, low_hsv, up_hsv)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    cv.imshow("poli",poly)
    cv.imshow("Maska",mask)
    cv.imshow("Orig", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.waitKey(0)
cv.destroyAllWindows()


