#!/bin/bash

# Funzione per leggere il valore START dal file run_loop.sh
get_start_offset() {
    # Leggi il valore della variabile START dal file
    grep -oP '^START=\K\d+' ./utils/run_loop.sh
}

# Funzione per gestire l'estrazione e la ruota
find_matching_extraction() {
    local numbers=("$@")  # Ottieni tutti i numeri da cercare
    local reports_dir="./reports"
    
    # Ottieni l'offset dal file run_loop.sh
    local start_offset
    start_offset=$(get_start_offset)-1
    
    # Contiamo le estrazioni
    local extraction_count=0
    local found_header=false  # Flag per segnare quando troviamo l'header "CONFRONTO CON L'ESTRAZIONE REALE"
    
    # Definiamo le ruote valide
    local valid_ruote=("Bari" "Cagliari" "Firenze" "Genova" "Milano" "Napoli" "Palermo" "Roma" "Torino" "Venezia" "Nazionale")
    
    # Per ogni file all'interno della cartella reports
    for report_file in "$reports_dir"/*; do
        # Salta se è una directory
        if [ -d "$report_file" ]; then
            continue
        fi
        
        # Scandisci il file riga per riga
        while IFS= read -r line; do
            # Controlla se è l'header "CONFRONTO CON L'ESTRAZIONE REALE"
            if [[ "$line" =~ "CONFRONTO CON L'ESTRAZIONE REALE" ]]; then
                found_header=true
                continue  # Salta la riga dell'header
            fi

            # Se l'header è stato trovato, considera solo le prossime 12 righe, e continua per altri blocchi
            if [ "$found_header" = true ]; then
                # Estrai la ruota dalla riga
                ruota=$(echo "$line" | cut -d ' ' -f 1)
                
                # Se la ruota non è valida, salta la riga
                if [[ ! " ${valid_ruote[@]} " =~ " ${ruota} " ]]; then
                    continue
                fi
                
                # Incrementa il contatore per ogni riga valida
                extraction_count=$((extraction_count + 1))
                
                # Estrarre i numeri dalla riga
                numeri=$(echo "$line" | cut -d ' ' -f 2-)

                # Ignora le righe che contengono "+o-1::"
                if [[ "$line" =~ "+o-1::" ]]; then
                    continue
                fi

                # Verifica che tutti i numeri siano presenti nell'estrazione
                match=true
                for num in "${numbers[@]}"; do
                    if [[ ! "$numeri" =~ "$num" ]]; then
                        match=false
                        break
                    fi
                done
                
                # Se tutti i numeri sono presenti, stampa l'estrazione
                if [ "$match" = true ]; then
                    # Calcola il numero corretto con l'offset
                    adjusted_count=$((start_offset + extraction_count))
                    # Stampa l'estrazione con il numero corretto
                    printf "%03d:%s:%s\n" "$adjusted_count" "$ruota" "$numeri"
                fi
                
                # Se abbiamo processato 12 righe, resettiamo il contatore e riprendiamo con il prossimo blocco
                if [ "$extraction_count" -ge 12 ]; then
                    extraction_count=0
                fi
            fi
        done < "$report_file"
    done
}

# Chiamata alla funzione con i numeri da cercare (tutti gli argomenti passati)
find_matching_extraction "$@"
