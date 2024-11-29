#!/bin/bash

# Vyhledání posledního souboru pro dané tel. číslo
last_file=`find <path/to/folder/with/last/file/$1> -type f -cmin -30 -exec stat --format '%Y %n' {} + | sort -nr | cut -d" " -f2 | head -1`

# Založení složky, ve které bude přepis posledního hovoru k dispozici
phone_num=${1: -9}
phone_num_dir="<path/to/html/folder/$phone_num>"
mkdir $phone_num_dir

# Načtěte obsah souboru last_file
mapfile -t texts < $last_file

# Počet řádků v souboru last_file
lines=`wc -l $last_file | cut -d" " -f1`

# Vytvoř HTML soubor ve složce s požadovaným tel. číslem
cat > $phone_num_dir/index.html << EOF
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DavidGPT</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <div class="terminal">
        <div class="terminal-header">
            <span class="terminal-title">Last Call Transcription</span>
        </div>
        <div class="terminal-body">
            <div class="terminal-content">
                <span class="prompt">$</span>
                <span class="command">echo \$LASTCALL</span>
`		for i in $(seq 0 $(($lines-1))); do
                        echo "<br>"
                        echo "<span class="output">${texts[$i]}</span>"
                        echo "<br>"
                done`
                <br>
            </div>
        </div>
    </div>
</body>
</html>
EOF

# Po určité době složku odeber
sleep 1800
rm -r $phone_num_dir
