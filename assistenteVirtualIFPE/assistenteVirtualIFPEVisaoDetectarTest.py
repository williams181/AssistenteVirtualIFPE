import cv2 # pip install OpenCV
import numpy as np # pip install NumPy
from matplotlib import pyplot as plt
print("Versão do OpenCV:", cv2.__version__)

classificador = cv2.CascadeClassifier('assistenteVirtualIFPE\\cascades\\haarcascade_frontalface_default.xml')

webCam = cv2.VideoCapture(0)

while(True):
    conectou, imagem = webCam.read()
    converteuCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    encontrarFaces = classificador.detectMultiScale(converteuCinza, 1.3, 5)

    for (x,y,w,h) in encontrarFaces:
        cv2.rectangle(imagem,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = converteuCinza[y:y+h, x:x+w]
        roi_color = imagem[y:y+h, x:x+w]
        eyes = classificador.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        cv2.imshow("Rosto", imagem)
        teclou = cv2.waitKey(1) & 0xFF
        if teclou == ord('q') or teclou == 27: # se apertar q ou ESC
            break
    
    webCam.release()
    cv2.destroyAllWindows()
