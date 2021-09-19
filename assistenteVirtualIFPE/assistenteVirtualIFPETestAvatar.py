import threading
import time
import cv2
import os

DirPath = "assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo\\"

Files = os.listdir(DirPath)

for File in Files:
    imgPath = os.path.join(DirPath, File)
    print(imgPath)
    image = cv2.imread(imgPath)
    cv2.imshow("image", image)
    # time.sleep(1)
    # cv2.destroyAllWindows()
    cv2.waitKey(0)
cv2.destroyAllWindows()