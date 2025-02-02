# Answering machine

Toto byla původní verze telefonního pomocníka, která měla za cíl vyzpovídat volajícího a převést jeho požadavky na text. Tento text byl automaticky zaslán na email obchodníka, který tak měl možnost se na hovor s klientem připravit, popřípadě mohl vyfiltrovat volající, se kterými vůbec mluvit nechtěl.

Vzhledem k tomu, že zvuková nahrávka, kterou lze poslat Googlu k převodu na text, musí mít maximální délku jednu minutu (pro delší nahrávky je nutné využít placený Google Cloud), zajistí skript *new_file_detector.sh* také rozporcování nahrávky v místech, kde volající udělal pauzu a pošle části rozhovoru k transkribci jednotlivě.
