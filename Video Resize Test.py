import numpy as np
import math
import cv2 as cv
from PIL import Image
import time


video = cv.VideoCapture(0)

video.set(3, 5000)
video.set(4, 5000)

while True:
    ret, frame = video.read()



    cv.imshow("aa", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.DestroyAllWindows

#conclusion: OPENCV ne podpira moje Logitech C270 Web Kamere in zaradi tega ne moram dobiti max FOV-a iz nje. Default resolucija je 640x480