#!/bin/bash
# ==========================================================
# GianKoLotto® – Taratura automatica del parametro SoftMax β
# ==========================================================

# Path base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$ROOT_DIR/etc/config.ini"
MAIN_SCRIPT="$ROOT_DIR/src/main.py"

# Intervallo di tuning per softmax_beta
START=6.00
END=28.00
STEP=0.50

# Colori terminale
YELLOW=$(tput setaf 3)
RESET=$(tput sgr0)

echo "${YELLOW}TUNING GIANKOLOTTO | PARAMETRO SoftMax β"
echo " Intervallo: $START → $END con passo $STEP${RESET}"
echo ""
echo "🕒 Avvio: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

smax=$START
while awk "BEGIN {exit !($smax <= $END)}"; do
    # Abilita SoftMax e aggiorna valore beta nel file di configurazione
    sed -i.bak -e "s/^usa_softmax=.*/usa_softmax=True/" \
               -e "s/^softmax_beta=.*/softmax_beta=$smax/" "$CONFIG_FILE"

    # Esegui il main e cattura l'output
    output=$(python "$MAIN_SCRIPT")

    # Estrai risultati
    match=$(echo "$output" | grep "Totale match esatti" | awk '{print $4}')
    vicini=$(echo "$output" | grep "Totale match vicini" | awk '{print $4}')

    # Visualizza sintesi
    printf "β = %.2f  →  MATCH: %s   VICINI: %s\n" "$smax" "${match:-N/D}" "${vicini:-N/D}"

    # Prossimo valore
    smax=$(awk "BEGIN {printf \"%.2f\", $smax + $STEP}")
done

echo ""
echo "${YELLOW}✅ Taratura completata.${RESET}"
echo ""
echo "🕒 Fine:  $(date '+%Y-%m-%d %H:%M:%S')"
