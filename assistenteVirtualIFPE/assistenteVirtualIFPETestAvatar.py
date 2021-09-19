import threading
import time
import cv2

diretorioA = "assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo\\olho\\avatar_personalizado1.png"

imgA = cv2.imread(diretorioA)

diretorioB = "assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo\\boca\\avatar_personalizado1.png"

imgB = cv2.imread(diretorioB)

while True:
    def threadx():
        cv2.imshow("img",imgA)
        time.sleep(1)
        cv2.imshow("img",imgB)
        time.sleep(1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    t1 = threading.Thread(target=threadx)
# t2 = threading.Thread(target=threadx)
# t3 = threading.Thread(target=threadx)
# t4 = threading.Thread(target=threadx)

# t1.start()
# t2.start()
# t3.start()
    t1.start()
    print(threading.active_count())
