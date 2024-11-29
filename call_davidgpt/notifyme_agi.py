#!/"<path/to/your/virtual/env>"

import os
import json
from asterisk.agi import AGI
import smtplib
from email.mime.text import MIMEText

environment = "<path/to/file/with/variables>"
with open(environment, "r") as file:
    file = json.load(file)
    my_email = file["my_email"]
    password = file["my_email_pass"]
    to_email = file["target_email"]


def send_mail(tel_num):
    subject = f'Hledá tě {tel_num}'
    text = f'Shání se po tobě {tel_num}, tak se mu ozvi!'

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = my_email
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(my_email, to_email, msg.as_string())


agi = AGI()
callerId = agi.env['agi_callerid']
callerId = callerId[-9:]

send_mail(callerId)
agi.stream_file("notification-done")
agi.hangup()
