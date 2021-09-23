import threading
import time
import cv2
import os

diretorio1 = "assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo\\a.png"

diretorio2 = "assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo\\b.png"

def tarefa1():
    for i in range(10):
        image = cv2.imread(diretorio1)
        time.sleep(1)
        cv2.imshow("image", image)
        time.sleep(1)
        cv2.destroyAllWindows()

def tarefa2():
    for i in range(10):
        image = cv2.imread(diretorio2)
        time.sleep(1)
        cv2.imshow("image", image)
        time.sleep(1)
        cv2.destroyAllWindows()

threading.Thread(target=tarefa1).start()
tarefa2()
