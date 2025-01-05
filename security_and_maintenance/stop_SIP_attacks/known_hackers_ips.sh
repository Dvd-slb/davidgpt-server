#!/bin/bash

# Skript stačí spustit přes cron jednou denně. Zajistí, že budeme mít seznam všech IP adres, které jsme kdy zabanovali.

cat "</.../suspicious_ips.list>" >> "</.../known_hackers_ips.list>"
sudo ipset list | grep -Po '^[1-9].*?(?=tim)' >> "</.../known_hackers_ips.list>"

# Aby se ve finálním seznamu žádné adresy nedublovali
python3 "</.../unique_IPs.py>"

cat "</.../unique_ips.list>" > "</.../known_hackers_ips.list>"
rm "</.../unique_ips.list>"
