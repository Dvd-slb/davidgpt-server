# Security & maintenance
K zabezpečení a údržbu serveru používám několik běžných hotových služeb (např. firewalld, fail2ban, cron, logrotate, ...).


###### check_services_status
Tato složka má na starosti mě upozornit emailem, pokud se neočekávaně zastaví nějaká důležitá služba (např. firewall). A u většiny emailových poskytovatelů lze nastavit službu "email to sms", takže si takto důležité oznámení nechávám zaslat sms zprávou.


###### banned_IPs
Sbírá všechny IP adresy, které byly zablokovány přes fail2ban


###### stop_SIP_attacks
Jelikož se mi nedařilo nastavit fail2ban tak, aby fungoval podle mých představ i na SIP, udělal jsem to takto. Nevýhodou bylo, že se paměť takto zabanovaných adres po restartu serveru vymazala. Proto je potřeba mít aktualizovaný seznam již zabanovaných adres (k tomu slouží known_hackers_ips.sh) a spouštět službu po každém nastartování serveru (init_sip_blocker.service).
