import speech_recognition as sr


def ouvir_comando():
    reconhecedor = sr.Recognizer()

    with sr.Microphone() as fonte:
        print("Diga algo...")
        reconhecedor.adjust_for_ambient_noise(fonte)
        audio = reconhecedor.listen(fonte)

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
    except sr.RequestError:
        print("Erro ao acessar o serviço de reconhecimento de voz.")
        

# Exemplo de uso
comando = ouvir_comando()