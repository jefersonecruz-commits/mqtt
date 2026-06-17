import speech_recognition as sr 
import paho.mqtt.client as mqtt
import json 
import time 

#mqtt
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "forja/desenvolvimento/tarde"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

#voz
recognizer = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    print("calibrando...")
    recognizer.adjust_for_ambient_noise(source, duration = 2)

print("pronto mande o comando:\n")
while True:
    try:
        with mic as source:
            print("ouvindo...")
            audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5        
    )
            
            texto = recognizer.recognize_google(
    audio,
    language = "pt-BR"
)
            tetxo = texto.strip()
            print("você disse: " +texto)

        partes = texto.split(maxplit=1)
        comando =partes[0]
        valor = partes[1] if len(partes) > 1 else ""

        playload = {
         comand: comando,
                        "value": valor.capitalize()
                    }
        mensagem = json.dumps(
                        playload,
                        ensure_ascii=False
                    )
        client.publish(TOPIC, mensagem)
        print("enviado!")

    except sr.UnknownValueError:
        print("enviado!")
                        
    except Exception as e:
        print("erro:", e)
                        
    time.sleep(1)