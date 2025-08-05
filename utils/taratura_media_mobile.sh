#!/bin/bash
# ================================================================
# GianKoLotto® – Taratura automatica del parametro Media Mobile
# ================================================================

# Path base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$ROOT_DIR/etc/config.ini"
MAIN_SCRIPT="$ROOT_DIR/src/main.py"

# Parametri
START=90
END=99999
STEP=1

# Colori
CYAN=$(tput setaf 6)
RESET=$(tput sgr0)

echo "${CYAN}TUNING GIANKOLOTTO | PARAMETRO media_mobile_num_predizioni"
echo "Intervallo: $START → $END con passo $STEP${RESET}"
echo ""
echo "🕒 Avvio: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Abilita modalità media mobile nel file di configurazione
sed -i.bak "s/^media_mobile_attiva=.*/media_mobile_attiva=True/" "$CONFIG_FILE"

# Inizia il ciclo di taratura
for ((n_pred = START; n_pred <= END; n_pred += STEP)); do
    # Aggiorna il valore nel config.ini
    sed -i "s/^media_mobile_num_predizioni=.*/media_mobile_num_predizioni=$n_pred/" "$CONFIG_FILE"

    # Esegui lo script Python e cattura output
    output=$(python "$MAIN_SCRIPT")

    # Estrai risultati
    score=$(echo "$output" | grep "SCORE" | awk '{print $3}')
    match=$(echo "$output" | grep "MATCH" | awk '{print $6}')
    vicini=$(echo "$output" | grep "VICINI" | awk '{print $9}')

    # Output sintetico
    printf "predizioni = %3d  →  SCORE: %s  MATCH: %s   VICINI: %s\n" "$n_pred" "${score:-N/D}" "${match:-N/D}" "${vicini:-N/D}"
done

echo ""
echo "${CYAN}✅ Taratura completata.${RESET}"
echo ""
echo "🕒 Fine:  $(date '+%Y-%m-%d %H:%M:%S')"
