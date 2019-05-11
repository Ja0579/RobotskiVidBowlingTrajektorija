import numpy as np
import cv2 as cv
import imutils
import datetime
import time
import skimage
import os
import PIL
import matplotlib
from tkinter import *



lower_hsv = (0, 110, 0)    
upper_hsv = (179, 255, 255)                  
trigger = False
startTime = 0
potovanjeKrogle = 0
met = []
tocke = []


video = cv.VideoCapture(0)

time.sleep(2.0)

while True:
    
    time.sleep(1/500)

    ret, frame = video.read()
       

    if frame is None:
        break

    cframe = frame.copy()

    poly1 = np.array([[[44,480],[146,0],[0,0],[0,480]]], dtype=np.int32)               #leva stran   
    poly = cv.fillPoly(frame, poly1, 0)
    poly2 = np.array([[[349,480],[203,0],[640,0],[640,480]]], dtype=np.int32)          #desna stran
    poly = cv.fillPoly(frame, poly2, 0)
    poly3 = np.array([[[0,0],[0,10],[640,10],[640,0]]], dtype=np.int32)                #zgori   parametr 4 in 6 
    poly = cv.fillPoly(frame, poly3, 0)
    poly4 = np.array([[[800,600],[0,600],[0,595],[800,595]]], dtype=np.int32)          #spodi    parametr 6 in 8   
    poly = cv.fillPoly(frame, poly4, 0)

       
    blurred = cv.GaussianBlur(frame, (3, 3), 0)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

    maska = cv.inRange(hsv, lower_hsv, upper_hsv)
    maska = cv.erode(maska, None, iterations=2)
    maska = cv.dilate(maska, None, iterations=2)
    

    kontura = cv.findContours(maska.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    kontura = imutils.grab_contours(kontura)
    center = None


    if len(kontura) > 0:

        if not trigger:
            trigger = True
            startTime = time.time()

        c = max(kontura, key=cv.contourArea)

        ((x, y), radius) = cv.minEnclosingCircle(c)

        M = cv.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


        if radius > 1:
            cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)
            cv.circle(frame, center, 5, (0, 0, 255), 1)
    else:
        if(trigger):
            trigger = False
            potovanjeKrogle = time.time() - startTime
            
            barva = tuple(np.random.randint(255, size=3).astype(np.uint8))  
            barva= (np.asscalar(barva[0]),np.asscalar(barva[1]),np.asscalar(barva[2]))  

            met.append([tocke, barva])  
            tocke = []


            if potovanjeKrogle > 0.5:
                print("Krogla je potovala: " + str(round(potovanjeKrogle, 2)) + " sekund" + "\n" + "Hitrost krogle je: " + str(round((18/potovanjeKrogle*3.6),2)) + " km/h" + "\n" + "\n" + "\n" + "Za izbris trajektorije pridržite tipko <d> in" + "\n" +  "pri tem pazite da na stezi ni zaznane nobene krogle!" + "\n" + "\n" + "\n" + "Za izbris terminala, pridržite tipko <t>!" + "\n" + "--------------------------------------------------------------")
                

        if cv.waitKey(1) & 0xFF == ord('d'):
            print("Trajektorija izbrisana" + "\n" + "--------------------------------------------------------------")
            met = []

        if cv.waitKey(1) & 0xFF == ord('t'):
            os.system('cls||clear')
                                
    tocke.append(center)
    
    
    for index, m in enumerate(met):
        prej = None

        barva = met[index][1]
        for i in m[0]:

            if prej is not None:
                cv.line(cframe, prej, i, barva, 4) 

            prej = i

    for i in range(1, len(tocke)):

        if tocke[i - 1] is None or tocke[i] is None:
            continue
        
        cv.line(cframe, tocke[i - 1], tocke[i], (0, 0, 255), 4)
    


    cv.imshow("Frame", cframe)
    cv.imshow("maska", maska)
    cv.imshow("Blur", blurred)
    cv.imshow("Poly", poly)
    
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break



video.release()
cv.destroyAllWindows()
