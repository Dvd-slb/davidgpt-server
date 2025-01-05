#!/bin/bash

# Soubor s logy Asterisk (nebo jiného systému)
ASTERISK_LOG="</.../asterisk/security.log>"
# Soubor pro ukládání podezřelých IP adres
SUSPICIOUS_IPS_FILE="</.../suspicious_ips.list>"

# Vyčištění předchozího souboru s IP adresami
> "$SUSPICIOUS_IPS_FILE"

# Extrakce IP adres z logu, které odpovídají neúspěšným pokusům o přihlášení
grep "InvalidAccountID" "$ASTERISK_LOG" | grep -oP 'RemoteAddress="IPV4/UDP/\K[0-9.]+(?=/)' >> "$SUSPICIOUS_IPS_FILE"
grep "InvalidPassword" "$ASTERISK_LOG" | grep -oP 'RemoteAddress="IPV4/UDP/\K[0-9.]+(?=/)' >> "$SUSPICIOUS_IPS_FILE"

# Spuštění skriptu, který přidá IP adresy do ipset seznamu
. "</.../add_to_blacklist.sh>"

