# Answering machine

Toto byla původní verze telefonního pomocníka. Podstata tkvěla v tom volajícího vyzpovídat a jeho požadavky převést na text, který se automaticky poslal na email obchodníka. Obchodník poté měl čas se na hovor s klientem připravit, popřípadě mohl vyfiltrovat volající, se kterými vůbec mluvit nechtěl.

Jelikož zvuková nahrávka, kterou je možné poslat do googlu k převodu na text, musí mít maximálně minutu (u delších je potřeba využívat placený google cloud), zajistí skript new_file_detector.sh i rozporcování nahrávek v bodech, kde volající udělal pomlku a pošle je k transkribci jednotlivě.
