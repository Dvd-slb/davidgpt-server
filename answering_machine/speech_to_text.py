from google.oauth2 import service_account
from google.cloud import speech
import os
import sys
from send_mail import send_mail

# Vytvoření spojení s google speech to text
client_file = os.environ.get("STT_KEY")
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

# Přijaté argumenty ze scriptu new_file_detector.sh
phone_num = sys.argv[1]
unq_id = sys.argv[2]
full_file = sys.argv[3]
audio_files = sys.argv[4:]

# Konfigurace konkrétních požadavků pro přepis STT
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code="cs-CZ",
    enable_automatic_punctuation=True,
)

# Přepis zvukových souborů na text
text = ""
for file in audio_files:
    with open(file, "rb") as f:
        content = f.read()
        audio = speech.RecognitionAudio(content=content)

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        text += result.alternatives[0].transcript
        text += " "

# Odeslání emailu s přepisem, zvukovou nahrávkou a tel. číslem na požadovanou adresu
send_mail(number=phone_num, text=text, record=full_file)


