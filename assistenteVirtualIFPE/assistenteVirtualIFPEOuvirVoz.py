import speech_recognition as sr

r = sr.Recognizer()

mic = sr.Microphone()

with mic as fonte:
    r.adjust_for_ambient_noise(fonte)
    print("Diga algo: ")
    audio = r.listen(fonte)
    print("Enviando para reconhecimento")
    try:
        text = r.recognize_google(audio, language= "pt-BR")
        print("Voce Disse: {}" . format(text))
    except:
        print("Não entendi o que voce disse!")