#!/bin/bash
# ================================================================
# GianKoLotto® – Taratura automatica del RANGE ATTIVO delle estrazioni
# ================================================================

# Path base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$ROOT_DIR/etc/config.ini"
MAIN_SCRIPT="$ROOT_DIR/src/main.py"

# Parametri di riferimento
K_OPT=0.57
RANGE_OFFSET=5
RANGE_LEN=3
ULTIMA_ESTRAZIONE=100

# Colori
YELLOW=$(tput setaf 3)
RESET=$(tput sgr0)

totale_esatti=0

echo "${YELLOW}TUNING GIANKOLOTTO | RANGE ESTRAZIONI ATTIVE"
echo "decadimento_k fisso a $K_OPT${RESET}"
echo ""
echo "🕒 Avvio: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Loop combinatorio su range offset e lunghezza
for ((start=RANGE_OFFSET; start<=ULTIMA_ESTRAZIONE - RANGE_LEN; start++)); do
    # Aggiorna valori nel config
    sed -i "s/^range_attivo_offset=.*/range_attivo_offset=$start/" "$CONFIG_FILE"
    echo ""
    for ((stop=1; stop<=RANGE_LEN; stop++)); do
        # Aggiorna valori nel config
        sed -i "s/^range_attivo_len=.*/range_attivo_len=$stop/" "$CONFIG_FILE"

        # Esegui e cattura output
        output=$(python "$MAIN_SCRIPT")

        # Estrai risultati
        match=$(echo "$output" | grep "###" | awk '{print $6}')
        vicini=$(echo "$output" | grep "###" | awk '{print $9}')

        # Output formattato
        printf "Range (%d → %d)  →  MATCH: %s   VICINI: %s\n" "$start" "$stop" "${match:-N/D}" "${vicini:-N/D}"

        (( totale_esatti += match ))
        (( totale_estrazioni += 1 ))
    done
done

rate=$(( 100 * totale_esatti / totale_estrazioni ))
echo ""
echo "RATE $rate %"

echo ""
echo "${YELLOW}✅ Taratura range completata.${RESET}"
echo ""

echo "🕒 Fine:  $(date '+%Y-%m-%d %H:%M:%S')"
