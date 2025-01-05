#!/"<path/to/your/virtual/env>"

import os
import time
import json
from asterisk.agi import AGI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio

new_audio_dir = "<path/to/recorded/audio/folder>"
environment = "<path/to/file/with/variables>"
with open(environment, "r") as file:
    file = json.load(file)
    my_email = file["my_email"]
    password = file["my_email_pass"]
    to_email = file["target_email"]


def send_mail(tel_num, record):
    subject = f'Nový vzkaz od {tel_num}'
    text = f'Sháněl se po tobě {tel_num} a zanechal ti vzkaz, tak si ho co nejdřív pusť!'::

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = my_email
    msg['To'] = to_email
    msg.attach(MIMEText(text, 'plain'))

    with open(record, 'rb') as attachment:
        part = MIMEAudio(attachment.read(), _subtype='wav')
        part.add_header('Content-Disposition', 'attachment', filename="Záznam hovoru.wav")
        msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(my_email, to_email, msg.as_string())


agi = AGI()
callerId = agi.env['agi_callerid']
callerId = callerId[-9:]
now_time = time.time()
time_number = str(now_time).replace(".", "")
record = f"{new_audio_dir}{callerId}_{time_number}"

agi.record_file(record, "wav", "#", 10000, 0, True, 2)
agi.verbose("VZKAZ NAHRÁN")

send_mail(callerId, record + ".wav")
agi.verbose("EMAIL ODESLÁN")

agi.stream_file("record-done")
agi.hangup()

