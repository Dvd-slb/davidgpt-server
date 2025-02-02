# Security & maintenance
K zabezpečení a údržbě serveru používám několik běžných hotových služeb (např. firewalld, fail2ban, cron, logrotate, ...).


###### check_services_status
Tato složka má na starosti mě upozornit emailem, pokud se neočekávaně zastaví nějaká důležitá služba (např. firewall). U většiny poskytovatelů emailových adres lze nastavit službu "email to sms", takže je možné takto důležitá oznámení dostávat i formou SMS zprávy.


###### banned_IPs
Shromažďuje všechny IP adresy, které byly zablokovány přes fail2ban.


###### stop_SIP_attacks
Jelikož se mi nedařilo nastavit fail2ban tak, aby fungoval podle mých představ i pro SIP, vytvořil jsem vlastní řešení. Nevýhodou bylo, že se paměť takto zabanovaných adres po restartu serveru vymazala. Proto je potřeba mít aktualizovaný seznam již zabanovaných adres (k tomu slouží *known_hackers_ips.sh*) a spouštět službu po každém nastartování serveru (*init_sip_blocker.service*).
