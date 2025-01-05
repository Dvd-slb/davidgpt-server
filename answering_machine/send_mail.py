import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
import json
import os

# Potřebné informace k odeslání emailu
environment = "<path/to/file/with/variables>"
with open(environment, "r") as file:
    file = json.load(file)
    my_email = file["my_email"]
    password = file["my_email_pass"]
    to_email = file["target_email"]

# Funkce, která odesílá email na požadovanou adresu. Email obsahuje: jméno a číslo volajícího, přepsaný text z hovoru, zvukový záznam hovoru.
def send_mail(number, text, record):
    index = text.find("  ")
    if index > -1:
        name = text[:index]
        text = text[index+2:]
    else:
        name = "Jméno nezadáno"
        
    message = MIMEMultipart()
    message['From'] = my_email
    message['To'] = to_email
    message['Subject'] = f"Nový vzkaz od {name} - {number}"

    text = f"Dobrý den, přináším vám nový vzkaz od:\nJméno: {name}\nTelefonní číslo: {number}\n\nText vzkazu:\n{text}\n\nV případě potřeby naleznete zvukový záznam hovoru v příloze tohoto emailu."
    message.attach(MIMEText(text, 'plain'))

    with open(record, 'rb') as attachment:
        part = MIMEAudio(attachment.read(), _subtype='wav')
        part.add_header('Content-Disposition', 'attachment', filename="Záznam hovoru.wav")
        message.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(my_email, to_email, message.as_string())
        

