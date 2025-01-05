#!/bin/bash

# Název ipset seznamu
IPSET_NAME="blacklist"

# Soubor s podezřelými IP adresami
SUSPICIOUS_IPS_FILE="</.../suspicious_ips.list>"

# Ověř, zda existuje soubor s IP adresami
if [ ! -f "$SUSPICIOUS_IPS_FILE" ]; then
    echo "Soubor s podezřelými IP adresami ($SUSPICIOUS_IPS_FILE) neexistuje."
    exit 1
fi

# Přidání IP adres ze souboru do ipset seznamu
while IFS= read -r ip; do
    # Ověř, zda IP adresa již není v seznamu
    sudo ipset test $IPSET_NAME $ip &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Přidávám IP adresu $ip do seznamu '$IPSET_NAME'"
        sudo ipset add $IPSET_NAME $ip timeout 2147000
    else
        echo "IP adresa $ip již je v seznamu '$IPSET_NAME'"
    fi
done < "$SUSPICIOUS_IPS_FILE"

echo "Přidávání IP adres dokončeno."

