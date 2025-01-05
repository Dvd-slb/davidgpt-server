#!/bin/bash

# Název ipset seznamu
IPSET_NAME="blacklist"

# Vytvoření nového ipset seznamu (pokud neexistuje)
sudo ipset list $IPSET_NAME &> /dev/null
if [ $? -ne 0 ]; then
    echo "Vytvářím ipset seznam '$IPSET_NAME'"
    sudo ipset create $IPSET_NAME hash:ip timeout 2147000
else
    echo "ipset seznam '$IPSET_NAME' již existuje"
fi


# Přidání pravidel do iptables pro blokování IP adres ze seznamu ipset
sudo iptables -C INPUT -m set --match-set $IPSET_NAME src -j DROP &> /dev/null
if [ $? -ne 0 ]; then
    sudo iptables -I INPUT -m set --match-set $IPSET_NAME src -j DROP
    echo "Pravidlo přidáno do iptables pro blokování IP adres ze seznamu '$IPSET_NAME'."
else
    echo "Pravidlo pro iptables již existuje."
fi

# Přidání IP adres ze souboru do ipset seznamu
while IFS= read -r ip; do
    sudo ipset test $IPSET_NAME $ip &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Přidávám IP adresu $ip do seznamu '$IPSET_NAME'"
        sudo ipset add $IPSET_NAME $ip timeout 2147000
    else
        echo "IP adresa $ip již je v seznamu '$IPSET_NAME'"
    fi
done < "</.../known_hackers_ips.list>"

echo "Inicializace dokončena."
