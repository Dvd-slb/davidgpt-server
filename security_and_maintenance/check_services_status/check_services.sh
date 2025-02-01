#!/bin/bash

# Služby, na jejichž nečekané zastavení chci být upozorněn
services=("firewalld" "asterisk" "new_file_detector" "fail2ban")

for service in ${services[@]}; do
	systemctl status $service > /dev/null 2>&1
	# Pokud služba není aktivní, upozorni mě
	if [ $? -ne 0 ]; then
		python3 "</.../send_alarming_email.py>" $service
	fi	
done
