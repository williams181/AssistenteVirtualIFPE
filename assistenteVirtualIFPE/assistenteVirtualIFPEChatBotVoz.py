# -*- coding: utf-8 -*-
import serial # pip install pyserial
import threading
import time
import speech_recognition as sr # pip install SpeechRecognition
import pyttsx3 # pip install pyttsx3
from chatterbot import ChatBot # pip install chatterbot
from chatterbot.trainers import ListTrainer 
    
AMGbot = ChatBot("assistenteVirtualIFPE")

# texto inicial, com as conversas o bot vai ficando mais inteligente
conversa1 = ['olá bom dia!','bom dia, tudo bem?','voce poderia me ajudar?','sim, claro, o que o senhor precisa?'
            ,'onde fica a sala da coordenação?','subindo o corregor a esquerda!'
            ,'como faço para levar um livro para casa?','voce precisar preencher um pequeno formulario'
            ,'quanto tempo posso ficar com o livro?','voce pode ficar com o livro por no maximo 15 dias!']
            
conversa2 = ['olá bom dia!','bom dia, tudo bem?','voce poderia me ajudar?','sim, claro, o que o senhor precisa?'
            ,'onde fica a sala da coordenação?','subindo o corregor a esquerda!'
            ,'como faço para levar um livro para casa?','voce precisar preencher um pequeno formulario'
            ,'quanto tempo posso ficar com o livro?','voce pode ficar com o livro por no maximo 15 dias!']

treinar = ListTrainer(AMGbot)
treinar.train(conversa1)
treinar.train(conversa2)

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('rate', 150) # velocidade 120 = lento
contar = 0;
for vozes in voices: # listar vozes
    print(contar, vozes.name)
    contar+=1

voz = 0
engine.setProperty('voice', voices[voz].id)

r = sr.Recognizer()

mic = sr.Microphone(1) # 0 = microfone embutido

conectado = False
porta = 'COM7' # linux ou mac em geral -> '/dev/ttyS0'
velocidadeBaud = 115200

mensagensRecebidas = 1;
desligarArduinoThread = False

falarTexto = False;
textoRecebido = ""
textoFalado = ""

arduinoFuncionando = True

try:
    SerialArduino = serial.Serial(porta,velocidadeBaud, timeout = 0.2)
except:
    print("Verificar porta serial ou religar arduino")
    arduinoFuncionando = False

def handle_data(data):
    global mensagensRecebidas, engine, falarTexto, textoRecebido
    print("Recebi " + str(mensagensRecebidas) + ": " + data)
    
    mensagensRecebidas += 1
    textoRecebido = data
    falarTexto = True

def read_from_port(ser):
    global conectado, desligarArduinoThread
    
    while not conectado:
        conectado = True

        while True:
           reading = ser.readline().decode()
           if reading != "":
               handle_data(reading)
           if desligarArduinoThread:
               print("Desligando Arduino")
               break   

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

while (True):
    if falarTexto:
        if textoRecebido != "":
            engine.say(textoRecebido)
            engine.runAndWait()
            textoRecebido = ""
        elif textoFalado != "":
            resposta = AMGbot.get_response(textoFalado)
            engine.say(resposta)
            engine.runAndWait()
            textoFalado = ""
        
        #voz jarvis
        #wsh.AppActivate("MiniSpeech") # select another application
        #wsh.SendKeys("^a")
        #wsh.SendKeys(textoRecebido)
        #wsh.SendKeys("%{ENTER}")
        
        falarTexto = False
        #time.sleep(3)
    try:
        with mic as fonte:
            r.adjust_for_ambient_noise(fonte)
            print("Fale alguma coisa")
            audio = r.listen(fonte)
            print("Enviando para reconhecimento")
        try:
            text = r.recognize_google(audio, language= "pt-BR").lower()
            print("Você disse: {}".format(text))
            if text == "ligar" or text == "desligar":
                try:
                    pass
                    #message = b"/gpio/1"
                    
                    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #server_address = ('192.168.0.102', 80)
                    #sock.connect(server_address)
                    #sock.sendall(message)
                    #sock.close()
                except:
                    print("sem socket")
            if arduinoFuncionando:
                SerialArduino.write((text + '\n').encode())
            
            if text != "":
                textoFalado = text
                falarTexto = True
            
            print("Dado enviado")
            if(text == "desativar"):
                print("Saindo")
                
                desativando = "assistenteVirtualIFPE desativando."
                
                engine.say(desativando)
                engine.runAndWait()
                
                #voz jarvis
                #wsh.AppActivate("MiniSpeech") # select another application
                #wsh.SendKeys("^a")
                #wsh.SendKeys(desativando)
                #wsh.SendKeys("%{ENTER}")
                
                engine.stop()
                desligarArduinoThread = True
                if arduinoFuncionando:
                    SerialArduino.close()
                    lerSerialThread.join()
                break
        except:
            print("Não entendi o que você disse\n")
            engine.say("que que voce disse?")
            engine.runAndWait()
        
        time.sleep(0.5) # aguarda resposta do arduino
    except (KeyboardInterrupt, SystemExit):
        print("Apertou Ctrl+C")
        engine.stop()
        desligarArduinoThread = True
        if arduinoFuncionando:
            SerialArduino.close()
            lerSerialThread.join()
        break

