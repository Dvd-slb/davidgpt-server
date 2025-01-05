#!/"<path/to/your/virtual/env>"

import json
import smtplib
import sys

service = sys.argv[1].upper()
environment = "<path/to/file/with/variables>"
with open(environment, "r") as file:
    file = json.load(file)
    my_email = file["my_email"]
    password = file["my_email_pass"]
    to_email = file["target_email"]

msg = f"""\
Subject: Pozor nebezi {service}

Zkoukni si server, nebezi ti tam sluzba {service}!"""

with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(my_email, to_email, msg)

