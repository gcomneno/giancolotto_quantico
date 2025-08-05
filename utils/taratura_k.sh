#!/bin/bash
# ==========================================================
# GianKoLotto® – Taratura automatica del parametro k
# ==========================================================

# Path base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$ROOT_DIR/etc/config.ini"
MAIN_SCRIPT="$ROOT_DIR/src/main.py"

# Intervallo di tuning per k
START=0.33
END=0.42
STEP=0.01

# Colori terminale
CYAN=$(tput setaf 6)
RESET=$(tput sgr0)

echo "${CYAN}TUNING GIANKOLOTTO | PARAMETRO decadimento_k"
echo "Intervallo: $START → $END con passo $STEP${RESET}"
echo ""
echo "🕒 Avvio: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

k=$START
while awk "BEGIN {exit !($k <= $END)}"; do
    # Aggiorna valore nel file di configurazione
    sed -i.bak "s/^decadimento_k=.*/decadimento_k=$k/" "$CONFIG_FILE"

    # Esegui il main e cattura l'output
    output=$(python "$MAIN_SCRIPT")

    # Estrai risultati
    match=$(echo "$output" | grep "Totale match esatti" | awk '{print $4}')
    vicini=$(echo "$output" | grep "Totale match vicini" | awk '{print $4}')

    # Visualizza sintesi
    printf "k = %.2f  →  MATCH: %s   VICINI: %s\n" "$k" "${match:-N/D}" "${vicini:-N/D}"

    # Prossimo valore
    k=$(awk "BEGIN {printf \"%.2f\", $k + $STEP}")
done

echo ""
echo "${CYAN}✅ Taratura completata.${RESET}"
echo ""
echo "🕒 Fine:  $(date '+%Y-%m-%d %H:%M:%S')"
