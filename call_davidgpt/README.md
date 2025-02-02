# Call ChatGPT

Tato složka obsahuje kód, který umožňuje uskutečnit telefonní hovor a spojit se s chatbotem. Kromě toho si můžete poslechnout vtip nebo mi nahrát vzkaz. Je potřeba zmínit, že systém využívá několik externích služeb pro zajištění funkčnosti:
- **Asterisk** - Open-source framework pro vytváření komunikačních aplikací – hraje klíčovou roli tím, že spojuje volajícího s ústřednou na základě scénáře definovaného v souboru *asterisk_extensions.conf*.
- **Google Speech-to-Text** - Převádí hlasové požadavky volajícího na text, který je následně poslán chatbotovi ke zpracování.
- **OpenAI GPT** - Zpracovává textové dotazy a generuje odpovědi.
- **OpenAI Text-to-Speech** - Převádí textové odpovědi ChatGPT zpět na řeč.

Právě kvůli procesům převádění řeči na text a textu na řeč je nutné vyčkat několik vteřin na chatbotí reakci. Tyto převody mezi textem a audiem, stejně tak jako komunikaci mezi volajícím a chatbotem, koordinuje soubor *chatgpt_agi.py*.

Po ukončení hovoru program *text_to_html.sh* ještě 30 minut umožňuje zobrazit přepis konverzace na webové stránce (https://www.davidgpt.eu/<VašeTelČíslo>). Chod webového serveru zajišťuje **Apache HTTP Server**. Komunikace je chráněna SSL/TLS certifikáty od **Let's Encrypt**, jejichž správu provádí **Certbot**. Přes Apache mám nakonfigurován i **WebDAV server**, což umožňuje snadný přístup k potřebným souborům prakticky z jakéhokoli zařízení.


### Last delirious words
V době, kdy už není problém ani v češtině hlasově interagovat s chatboty skrze aplikace, těchto pár zveřejněných souborů revoluci ve způsobu komunikace s našimi AI parťáky zřejmě neodstartuje. Přesto se v určitých situacích může hodit mít číslo na DavidGPT při ruce:
1. Jste na místě bez internetu, ale s telefonním signálem a nutně potřebujete vědět, z jaké zeleniny se dělá základ na svíčkovou.
2. Těžkěj den za vámi, máte chuť se z toho vypovídat, jenže... iPhone se vám zase vybil. Ale s tím už počítáte, takže máte po ruce záložní stroj v podobě tlačítkové nokie, jenže... přátelé to neberou, mají vyplé zvuky.
3. Vašim (pra)rodičům ty internety nic moc neříkaj, ale o tý umělý inteligenci mluvili i v televizi a oni by si to taky rádi zkusili.

