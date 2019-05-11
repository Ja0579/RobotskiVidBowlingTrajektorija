import numpy as np
import cv2 as cv
import imutils
import time
import os

lower_hsv = (0, 110, 0)    
upper_hsv = (179, 255, 255)                    
trigger = False
startTime = 0
potovanjeKrogle = 0
met = []
tocke = []

video = cv.VideoCapture("video2.mp4")   #za testiranje "video1.mp4" in "video2.mp4"

time.sleep(2.0)

while True:
    
    time.sleep(1/100)

    ret, frame = video.read()  #zajamemo video iz kamere
        
    if frame is None:  #če ni zaznanih frame-ov, se program ustavi
        break

    cframe = frame.copy()

    poly1 = np.array([[[44,480],[146,0],[0,0],[0,480]]], dtype=np.int32)    #zapolnitev leve strani steze (ombočje določeno preko podprograma Fillpoly test)   
    poly = cv.fillPoly(frame, poly1, 0)
    poly2 = np.array([[[349,480],[203,0],[640,0],[640,480]]], dtype=np.int32)    #zapolnitev desne strani steze 
    poly = cv.fillPoly(frame, poly2, 0)
    poly3 = np.array([[[0,0],[0,6],[640,6],[640,0]]], dtype=np.int32)                #zapolnitev zgornjega dela steze (po potrebi zaradi premikanja pobiralnika kegljev) 
    poly = cv.fillPoly(frame, poly3, 0)
    poly4 = np.array([[[800,600],[0,600],[0,595],[800,595]]], dtype=np.int32)          #zapolnitev spodnjega dela steze (po potrebi)  
    poly = cv.fillPoly(frame, poly4, 0)
           
    blurred = cv.GaussianBlur(frame, (3, 3), 0)    #meglitev videa/slike
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)   #pretvorba v HSV prostor

    maska = cv.inRange(hsv, lower_hsv, upper_hsv)   #z dobljenimi lower_hsv in upper_hvs parametri, ki jih dobimo iz podprograma HSV Test, omejimo zaznavanje barv na sliki
    maska = cv.erode(maska, None, iterations=2)     #erozija: majhne zaznane konture odstranimo s slike/videa, s tem tudi zmanjšamo zaznane konture iskanih objektov
    maska = cv.dilate(maska, None, iterations=2)    #dilatacija: sedaj pa vse zaznane konture z odstranjenimi šumi, povečamo za lažje zaznavanje
    
    kontura = cv.findContours(maska.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  #na sliki/videu poiščemo konture
    kontura = imutils.grab_contours(kontura)
    center = None
    
    if len(kontura) > 0:  #če je zaznava vsaj ena kontura se zanka izvede

        if not trigger:  #zanka za čas potovanja krogle
            trigger = True
            startTime = time.time()

        konmax = max(kontura, key=cv.contourArea)  #poisce konturo z najvecjo povrsino in shrani v spremeljivko c
        ((x, y), radius) = cv.minEnclosingCircle(konmax)  #naredi krog znotraj konture
        moment = cv.moments(konmax)   #izracun momentov konture da lahko kasneje dolocimo center
        center = (int(moment["m10"] / moment["m00"]), int(moment["m01"] / moment["m00"]))

        if radius > 1:  #če na sliki/videu zaznamo vsak eno konturo in ima ta radij večji od 1, to konturo obdamo s krogom in narišemo center
            cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1)
            cv.circle(frame, center, 5, (0, 0, 255), 1)
    else:   #če kontura ni zaznana se izvede naslednji del kode
        if(trigger):    
            trigger = False
            potovanjeKrogle = time.time() - startTime   #po prvem zaznavanju krogle tu izracunamo čas potovanja krogle
            
            barva = tuple(np.random.randint(255, size=3).astype(np.uint8))         #to je random tuple v velikosti x1, x2, x3, ki ga uporabimo za spreminjanje barv trajektorije
            barva= (np.asscalar(barva[0]),np.asscalar(barva[1]),np.asscalar(barva[2]))                 #iz zgornjega array-a poberemo vrednosti in jih spremenimo v skalar

            met.append([tocke, barva])                                                                 #v met appendamo tocke in pa vrednosti barve - to je list v listu
            tocke = []
            if potovanjeKrogle > 0.5:   #če je čas zaznavanja večji od 0,5 sekund izpišemo statistiko v terminal (več od 0,5 zato da se ne izrisujejo milisekundna zaznavanja okolice)
                print("Krogla je potovala: " + str(round(potovanjeKrogle, 2)) + " sekund" + "\n" + "Hitrost krogle je: " + str(round((18/potovanjeKrogle*3.6),2)) + " km/h" + "\n" + "\n" + "\n" + "Za izbris trajektorije pridržite tipko <d> in" + "\n" +  "pri tem pazite da na stezi ni zaznane nobene krogle!" + "\n" + "\n" + "\n" + "Za izbris terminala, pridržite tipko <t>!" + "\n" + "--------------------------------------------------------------")
                
        if cv.waitKey(1) & 0xFF == ord('d'):  #ob pritisku tipke D izbrisemo trajektorijo pod pogojem, da se krogla ne zaznava
            print("Trajektorija izbrisana" + "\n" + "--------------------------------------------------------------")
            met = []

        if cv.waitKey(1) & 0xFF == ord('t'):  #ob pritisku tipke T se terminal izbriše
            os.system('cls||clear')
                                
    tocke.append(center)   #tocke pripenjamo v center
        
    for index, m in enumerate(met):     #enumerate naredi array v obliki --> [1, met1, 2, met2, 3, met3] in s to for zanko menjamo barve metov
        prej = None
        barva = met[index][1]
        for i in m[0]:
            if prej is not None:
                cv.line(cframe, prej, i, barva, 4) 
            prej = i

    for i in range(1, len(tocke)):      #v tej for zanki pa se trenutni met izrisuje z rdeco crto
        if tocke[i - 1] is None or tocke[i] is None:
            continue
        
        cv.line(cframe, tocke[i - 1], tocke[i], (0, 0, 255), 4)
    
    cv.imshow("Frame", cframe)
    cv.imshow("maska", maska)
    cv.imshow("Poly", poly)
    
    if cv.waitKey(1) & 0xFF == ord('q'):    #force shutdown s tipko Q
        break

video.release()
cv.destroyAllWindows()
