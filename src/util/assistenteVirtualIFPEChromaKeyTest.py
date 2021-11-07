import cv2
import numpy as np
import time
import threading



def avatar():
    if __name__=='__main__':

        cap = cv2.VideoCapture('data\\videos\\mulher.mp4')  # Captura o arquivo de vídeo
        while cap:

            fundo = cv2.imread('data\\images\\ifpe-jaboatao.png') # Carrega a imagem para substituição de fundo

            ret,frame = cap.read() # carrega um frame do vídeo capturado
            if not ret:
                exit()

            fundo  = cv2.resize(fundo, (frame.shape[1],frame.shape[0]))  # Redimensiona a imagem de fundo para as mesmas dimensões do vídeo

            lower = np.array([0, 150, 0], dtype=np.uint8)  # Determina o limite inferior [daqui para cima]
            upper = np.array([100, 255, 100], dtype=np.uint8)   # Determina o limite superior [daqui para baixo]

            mask = cv2.inRange(frame, lower, upper) # Cria máscara a partir dos limites LOWER-UPPER
            # Documentação sobre InRange: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

            #cv2.imshow('mask', mask ) # Exibe a Máscara

            fundo_process = cv2.bitwise_and(fundo, fundo, mask=mask)  #  Processa o FUNDO a partir da máscara, retirando o que for comum a area escura

            #cv2.imshow('fundo_process', fundo_process )  # Exibe o resultado do fundo processado

            invert_mask = np.invert(mask) # invert as cores da máscara para inverter a seleção

            #cv2.imshow('invert_mask', invert_mask ) # Exibe a Máscara

            frame_process = cv2.bitwise_and(frame, frame, mask=invert_mask) #  Processa o FRAME a partir da máscara, retirando o que for comum a area clara.

            #cv2.imshow('frame_process', frame_process )  # Exibe o resultado do frame processado

            final = cv2.addWeighted(fundo_process,1,frame_process,1,0)  # Mistura duas imagens 
            # documentação sobre addWeighted: https://docs.opencv.org/4.0.1/d5/dc4/tutorial_adding_images.html

            cv2.imshow('final', final )    # Exibe o resultado da imagem misturada

            c = cv2.waitKey(5)    # Aguarda tecla ser pressionada por determinad tempo
            # documentação sobre WaitKey: https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=waitkey

            if c == ord('q'):
                break

        cv2.destroyAllWindows()


threading.Thread(target=avatar).start()