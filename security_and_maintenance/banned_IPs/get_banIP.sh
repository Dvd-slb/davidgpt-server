#!/bin/bash

# Zjištění IP adres, které jsou díky fail2ban zablokované
sudo iptables -S | grep -Po '(?<=-s ).*?(?=-j)' >> "</.../banned_IPs/banned_IP_list.txt>"

# Zajistí, že v seznamu budou všechny adresy unikátní
python3 "</.../banned_IPs/unique_banned_IP.py>"
cat "</.../banned_IPs/uniq_banned_IP_list.txt>" > "</.../banned_IPs/banned_IP_list.txt>"
rm "</.../banned_IPs/uniq_banned_IP_list.txt>"

