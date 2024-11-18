#!/bin/bash

# Bude hlídat, jestli v zadané složce nepřibyl nový soubor (tzn. nový hovor), pokud ano, tak soubor pošle k převodu na text a odešle email uživateli.

# Cesty ke složkám a souborům, které budeme potřebovat
audio_dir="<path/to/target/folder/or/file>"
audio_done="<path/to/target/folder/or/file>"
ended_calls="<path/to/target/folder/or/file>"
py_stt="<path/to/target/folder/or/file>"
myenv="<path/to/target/folder/or/file>"
stats="<path/to/target/folder/or/file>"

# Nastaví pythonovské virtuální prostředí pro budoucí script
source $myenv

# Monitorování složky, jestli nepřibyl nový zvukový soubor
inotifywait -m -e create --timefmt "%d.%m.%Y %H:%M:%S" --format "%T %e %w%f %f" $audio_dir |
while read -r datum cas udalost cesta soubor; do
    unq_id=${soubor#*_}  # Odstraní část před prvním znakem "_"
    unq_id=${unq_id%_*}  # Odstraní část za posledním znakem "_"
    phone_num=$(echo $soubor | cut -d "_" -f 1)

# Kontrola souboru Master.csv, jestli už byl hovor dokončen
    until [[ $(cat $ended_calls | grep $unq_id | wc -l) > 0 ]]; do
        sleep 10
    done
    
# Určení délky nahrávky
    lenght=$(ffmpeg -i $cesta 2>&1 | grep "Duration" | cut -d " " -f 4)
    lenght=${lenght::-1}
    hrs=${lenght:0:2}
    mins=${lenght:3:2}
    secs=${lenght:6:2}
    
# Pokud je délka nahrávky méně než 1 minuta, posíláme jí do python scriptu na přepsání řeči na text    
    if [ $hrs == "00" ] && [ $mins == "00" ]; then
        python3 $py_stt $phone_num $unq_id $cesta $cesta
        mv $cesta $audio_done$phone_num"_"$unq_id".wav"
	
# Pokud je delší než 1 minuta, musíme nahrávku rozdělit do úseků kratších než 60s (požadavek google stt)
    else
        
    # Nejdříve určíme cílová tichá místa v nahrávce, abychom soubor nerozdělili v půlce slova.
    # Tyto časy uložíme do seznamu find_silence
        find_silence=$(ffmpeg -i $cesta -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | awk '/silence_start/{print $NF}')
        
    # Určíme konkrétní časy z find_silence, které jsou od sebe vzdáleny co nejdál, ale méně než 60s.
    # Tyto časy uložíme do seznamu cut_times
        x=60
        cut_times=(0)
        for r in $find_silence; do
            t=$r
            r=$(echo $r | cut -d "." -f 1)
            if [ $r -lt $x ]; then
                y=$t
            else
                cut_times+=($y)
                x=$((60 + $(echo $y | cut -d. -f1)))
            fi
        done
       
    # Rozdělíme soubor v časech uložených v seznamu cut_times
        index=0
        for time in ${cut_times[@]}; do
            if [ $time != 0 ]; then
                ffmpeg -i $cesta -c:a copy -ss $start -to $time $audio_done"/parted/"$phone_num"_"$unq_id"_"$index".wav"
            fi
            start=$time
            ((index++))
        done
        
    # Poslední část bude rozdělena od poslední hodnoty z cut_times až do konce souboru
        ffmpeg -i $cesta -c:a copy -ss $time $audio_done"/parted/"$phone_num"_"$unq_id"_"$index".wav"
        
    # Vytvoření seznamu s jednotlivými soubory pod 60s        
        parted_files=()
        for p in $(ls $audio_done"parted/" | grep $unq_id); do
            parted_files+=($audio_done"parted/"$p)
        done
        
    # Odešleme potřebné argumenty do pythonovského scriptu
        python3 $py_stt $phone_num $unq_id $cesta ${parted_files[@]}
        mv $cesta $audio_done$phone_num"_"$unq_id".wav"
        
    fi
    
# Zaznamenání hovoru do statistik    
    echo "$datum $cas / $phone_num / $lenght / $unq_id" >> $stats
done
