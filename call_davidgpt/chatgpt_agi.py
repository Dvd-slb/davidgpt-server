#!/"<path/to/your/virtual/env>"

import os
import random
import time
import json
from openai import OpenAI
from pydub import AudioSegment
from asterisk.agi import AGI
from google.oauth2 import service_account
from google.cloud import speech

# Definování proměnných
environment = "<path/to/file/with/variables>"
sounds_path = "<path/to/sounds/dir>"
date = time.strftime("%Y-%m-%d")
time_number = str(time.time()).replace(".", "")
rep_dir = "<path/to/text/records/dir>"
os.makedirs(rep_dir, exist_ok=True)

# Ověření u Googlu a OPENAI
with open(environment, "r") as file:
    file = json.load(file)
    openai = file["OPEN_AI_KEY"]
    stt_var = file["STT_KEY"]

client = OpenAI(api_key=openai)
credentials = service_account.Credentials.from_service_account_file(stt_var)
clientg = speech.SpeechClient(credentials=credentials)

# Instrukce pro chatbota
messages = [
    {"role": "system", "content": "Jsi užitečný telefonní asistent. Na zákazníky jsi milý. Když ti někdo řekne, že se nudí, navrhni mu, že si můžete zahrát slovní fotbal. Odpovídej maximálně 30 slovy."},
]


# Funkce pro převedení zvukové nahrávky na text
def my_stt(audio_file):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="cs-CZ",
        enable_automatic_punctuation=True,
    )
    text = ""
    with open(audio_file, "rb") as f:
        content = f.read()
        audio = speech.RecognitionAudio(content=content)
    response = clientg.recognize(config=config, audio=audio)
    for result in response.results:
        text += result.alternatives[0].transcript
        text += " "
    return text


# Funkce pro získání odpovědi od GPT
def send_request(text):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    response = response.choices[0].message.content
    return response


# Spuštění procesu
agi = AGI()
callerId = agi.env['agi_callerid']
agi.verbose(f"call from {callerId}")

# Nastavení maximálního denního počtu hovorů z jednoho čísla na 5 
number_of_calls = len(os.listdir(rep_dir))
if number_of_calls >= 5 and callerId != "<my number>":
    agi.stream_file("max-pocet-hovoru")
    agi.hangup()

else:
    agi.stream_file("zvolen-gpt", "1234567890*#")

# Zaznamenání hovoru v textové podobě pro pozdější zobrazení na webu
    with open(f"{rep_dir}/{time_number}", "w") as report:
        while True:
            n = random.randint(1, 9999999999)
            filename = str(n).zfill(10)

# Nahrání dotazu volajícího 
            agi.verbose("Recording started...")
            agi.record_file(f"{sounds_path}/{filename}", "wav", "#", 10000, 0, True, 2.5)
            agi.verbose("Recording stopped. Processing now...")
            agi.set_variable("VOLUME(TX)", "-5")
            agi.stream_file("success")
            agi.set_variable("VOLUME(TX)", "0")

# Převedení zvukové žádosti volajícího na text
            text = my_stt(f"{sounds_path}/{filename}.wav")
            report.write(f"You: {text}\n")
            agi.verbose("I heard: " + text)
            messages.append({"role": "user", "content": text}),

# Získání a zpřehlednění odpovědi od OpenAI
            original_response = send_request(text)
            response = original_response.replace('\n', ' ')
            response = original_response.replace('"', '\'')

# Odeslání odpovědi do Asterisku
            agi.verbose("I got back: " + response)
            agi.set_variable("Result", response)
            messages.append({"role": "assistant", "content": response}),
            report.write(f"Me: {response}\n")

# Převedení textové odpovědi na hlasovou zprávu.
            tts = client.audio.speech.create(
                model="tts-1",
                voice="echo",
                input=response,
            )
            tts.stream_to_file(f"{sounds_path}/{filename}_response.mp3")

# Nastavení parametrů zvukového souboru
            sound = AudioSegment.from_file(f"{sounds_path}/{filename}_response.mp3", format="mp3")
            sound = sound.set_frame_rate(8000)
            sound = sound.set_channels(1)
            sound.export(f"{sounds_path}/{filename}_response.wav", format="wav")

# Přehrání odpovědi voljícímu
            agi.stream_file(f"{sounds_path}/{filename}_response")

# Odstranění vzniklých audio souborů
            os.remove(f"{sounds_path}/{filename}.wav")
            os.remove(f"{sounds_path}/{filename}_response.mp3")
            os.remove(f"{sounds_path}/{filename}_response.wav")

