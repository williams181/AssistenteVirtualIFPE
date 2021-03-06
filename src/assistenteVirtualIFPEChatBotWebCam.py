# -*- coding: utf-8 -*-
import serial # pip install pyserial
import threading
import time
import PIL # pip install pillow
import PIL as Image # pip install pillow 
import numpy as np # pip install NumPy
import speech_recognition as sr # pip install SpeechRecognition
import pyttsx3 # pip install pyttsx3
import cv2 # pip install opencv-python
import chatterbot # pip install chatterbot
import spacy
# from assistenteVirtualIFPE.assistenteVirtualIFPEChromaKeyTest import avatar # pip install -U spacy
# python -m spacy link en_core_web_sm en
# python -m spacy link en_core_web_md en
# python -m spacy download en_core_web_sm
# en-core-web-sm-3.1.0

#chatbot
from chatterbot.trainers import ListTrainer # pip install chatterbot
# caso de erro: No module named 'chatterbot_corpus'
# python -m pip install chatterbot-corpus

from chatterbot import ChatBot

AMGbot = ChatBot("assistenteVirtualIFPE")

# texto inicial, com as conversas o bot vai ficando mais inteligente

conversa = ['Oi?', 
    'Olá, tudo certo?',
    'Qual o seu nome?', 
    'Assistente IFPE, seu amigo bot',
    'Por que seu nome é Assistente IFPE?', 
    'Assistente IFPE é meu nome, sou um chatbot criado para fins educacionais',
    'Prazer em te conhecer', 
    'Igualmente jovem.',
    'Quantos anos você tem?', 
    'Eu nasci em 2021, sou bebê, faz as contas, rs.',
    'Você gosta de videogame?', 
    'Eu sou um bot, eu só apelo.',
    'Qual a capital de Pernambuco?', 
    'Recife, aqui é muito bonito.',
    'Qual o seu personagem favorito?', 
    'Gandalf, o mago.',
    'Qual a sua bebida favorita?', 
    'Eu bebo café, o motor de todos os programas de computador.',
    'Qual o seu gênero?', 
    'Sou um chatbot e gosto de algoritmos',
    'Conte uma história', 
    'Tudo começou com a forja dos Grandes Aneis. Três foram dados aos Elfos, imortais... os mais sabios e belos de todos os seres. Sete, aos Senhores-Anões...',
    'Conhece a Siri?', 
    'Conheço, a gente saiu por um tempo.',
    'Conhece a Alexa?', 
    'Ela nunca deu bola pra mim.',
    'Você gosta de Game of Thrones?', 
    'Dracarys',
    'O que você faz?', 
    'Eu bebo e sei das coisas',
    'Errado', 
    'Você não sabe de nada, John Snow.']

treinar = ListTrainer(AMGbot)
treinar.train(conversa)

r = sr.Recognizer()

mic = sr.Microphone(0) # 0 = microfone embutido

conectado = False
porta = 'COM11' # linux ou mac em geral -> '/dev/ttyS0'
velocidadeBaud = 115200

mensagensRecebidas = 1;
desligarArduinoThread = False
desligarCameraThread = False
desligarVozThread = False

falarTexto = False;
textoRecebido = ""
textoFalado = ""

arduinoFuncionando = True
nuncaTeVi = True;
jaTeVi = False;

def avatar():
    if __name__=='__main__':

        cap = cv2.VideoCapture('data\\videos\homem.mp4')  # Captura o arquivo de vídeo
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

            c = cv2.waitKey(10)    # Aguarda tecla ser pressionada por determinad tempo
            # documentação sobre WaitKey: https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=waitkey

            if c == ord('q'):
                break

        cv2.destroyAllWindows()


threading.Thread(target=avatar).start()




try:
    SerialArduino = serial.Serial(porta,velocidadeBaud, timeout = 0.2)
except:
    print("Verificar porta serial ou religar arduino")
    arduinoFuncionando = False

def handle_data(data):
    global mensagensRecebidas, falarTexto, textoRecebido
    print("Recebi " + str(mensagensRecebidas) + ": " + data)
    
    mensagensRecebidas += 1
    textoRecebido = data
    
    falarTexto = True

def read_from_port(ser):
    global conectado, desligarArduinoThread
    
    while not conectado:
        conectado = True

        while True:
           try:
               reading = ser.readline().decode()
           except:
               print("Serial desligada")
           if reading != "":
               handle_data(reading)
           if desligarArduinoThread:
               print("Desligando Arduino")
               break


def conectaCamera():
    global desligarCameraThread, arduinoFuncionando, SerialArduino,\
        nuncaTeVi, jaTeVi
    classificador = cv2.CascadeClassifier('data\\cascades\\haarcascade_frontalface_default.xml')
    webCam = cv2.VideoCapture(0)
    while(True):
        conectou, imagem = webCam.read()
        
        imagem = cv2.flip(imagem, 1) # inverte imagem (opcional)
        alturaImagem, larguraImagem = imagem.shape[:2]
        
        converteuCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        
        encontrarFaces = classificador.detectMultiScale(converteuCinza,
                                                        scaleFactor=1.5,
                                                        minSize=(150,150),
                                                        maxSize=(200,200))
        cor = (0,0,255)
        for(origemX, origemY, largura, altura) in encontrarFaces:
            cv2.rectangle(imagem,(origemX,origemY),
                          (origemX + largura, origemY + altura),
                          cor,2)
            
            if nuncaTeVi: # quando a camera te ver pela primeira vez
                time.sleep(0.5)
                nuncaTeVi = False
                jaTeVi = True
            
            raio = 4
            centroRosto = (origemX + int(largura/2),origemY + int(altura/2))
            cv2.circle(imagem, centroRosto, raio, cor)
            
            # Normalizar = deixa valores entre zero até um
            normalizarZeroAteUm = int(larguraImagem/2)
            # Correção = transforma valores para 1 até 10
            fatorDeCorrecao = 10
            
            erroCentro = (((centroRosto[0] - (larguraImagem/2))
            /normalizarZeroAteUm) * fatorDeCorrecao)
            
            try:
                if arduinoFuncionando:
                    pass
                # arduino desativado porque o som do motor interfere na voz
                    #SerialArduino.write(('servo' + str(erroCentro) + '\n').encode())
            except:
                print("não enviou")
    
        cv2.imshow("Rosto", imagem)
        
        teclou = cv2.waitKey(1) & 0xFF
        if desligarCameraThread:
            webCam.release()
            cv2.destroyAllWindows()
            print("Desligando camera")
            break
    


def falar():
    global jaTeVi, falarTexto, textoRecebido, textoFalado
    
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 180) # velocidade 120 = lento
    contar = 0;
    for vozes in voices: # listar vozes
        print(contar, vozes.name)
        contar+=1
    
    voz = 0 #1
    engine.setProperty('voice', voices[voz].id)
    
    #IVONA VOICE: RICARDO
    #https://harposoftware.com/en/portuguese-brasil/166-ricardo-portuguese-brasilian-voice.html
    #https://kripytonianojarvis.com/site/pre-instalacao/

    while True:
        if desligarVozThread:
            engine.stop()
            break
        if jaTeVi:
            engine.say("Olá, bem vindo! em que posso ajuda-lo?")
            # from PIL import Image
            # im = Image.open(r"assistenteVirtualIFPE\\assistenteVirtualIFPEAvatarModelo\\b.png")
            # im.show()
            engine.runAndWait()
            jaTeVi = False
        if falarTexto:
            if textoRecebido != "":
                engine.say(textoRecebido)
                engine.runAndWait()
                textoRecebido = ""
            elif textoFalado != "":
                resposta = AMGbot.get_response(textoFalado)
                print("Assistente: " + str(resposta))
                engine.say(resposta)
                engine.runAndWait()
                textoFalado = ""
            
            falarTexto = False

def desligando():
    global desligarArduinoThread, arduinoFuncionando, \
        SerialArduino, lerSerialThread,  \
        desligarCameraThread, desligarVozThread
    
    desligarArduinoThread = True
    desligarCameraThread = True
    desligarVozThread = True
    if arduinoFuncionando:
        SerialArduino.close()
        lerSerialThread.join()
    falarVozThread.join()
    
    print("Tudo desligado")

if arduinoFuncionando:
    try:
        lerSerialThread = threading.Thread(target=read_from_port, args=(SerialArduino,))
        lerSerialThread.start()
    except:
        print("Verificar porta serial ou religar arduino")
        arduinoFuncionando = False
    print("Preparando Arduino")
    time.sleep(2)
    print("Arduino Pronto")
else:
    time.sleep(2)
    print("Arduino não conectou")

ligaCamera = True
if ligaCamera:
    try:
        cameraLigadaThread = threading.Thread(target=conectaCamera)
        cameraLigadaThread.start()
    except:
        print("sem câmera")
        
falarVozes = True
if falarVozes:
    try:
        falarVozThread = threading.Thread(target=falar)
        falarVozThread.start()
    except:
        print("sem mic")

while(nuncaTeVi): # só conversa depois de ver a pessoa
        pass

while (True):
    
    try:
        with mic as fonte:
            r.adjust_for_ambient_noise(fonte)
            print("Fale alguma coisa")
            audio = r.listen(fonte)
            print("Enviando para reconhecimento")
        try:
            text = r.recognize_google(audio, language= "pt-BR").lower()
            print("Você disse: {}".format(text))

            if arduinoFuncionando:
                SerialArduino.write((text + '\n').encode())

            print("Dado enviado")
            if(text.startswith("desativar")):
                print("Saindo")
                
                desativando = "assistenteVirtualIFPE desativando."
                textoRecebido = desativando
                textoFalado = desativando

                desligando()
                break
            
            # retirar os textos que são comandos especiais
            if text != "" and not text.startswith("ligar") and \
            not text.startswith("desligar") \
            and not text.startswith("desativar"):
                textoFalado = text
                falarTexto = True
        except:
            print("Não entendi o que você disse\n")

    except (KeyboardInterrupt, SystemExit):
        print("Apertou Ctrl+C")
        desligando()
        break

