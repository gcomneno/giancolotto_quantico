#!/bin/bash
# ==========================================================
# GianKoLotto® – Esecuzione in loop di run.sh su più estrazioni
# ==========================================================

# Path e setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$ROOT_DIR/etc/config.ini"
RUN_SCRIPT="$SCRIPT_DIR/run.sh"

# Range estrazioni
START=10
STOP=100
TOTAL=$((STOP - START + 1))
CURRENT=0

# Colori terminale portabili
GREEN=$(tput setaf 2)
BLUE=$(tput setaf 4)
RESET=$(tput sgr0)

echo "${BLUE}Avvio taratura su range estrazioni da $START a $STOP... ($TOTAL iterazioni)${RESET}"
echo ""

for ((i=START; i<=STOP; i++)); do
  CURRENT=$((CURRENT + 1))

  echo "${GREEN}[INFO] ($CURRENT/$TOTAL) Set: ultima_estrazione_da_considerare = $i${RESET}"
  sed -i "s/^ultima_estrazione_da_considerare=.*/ultima_estrazione_da_considerare=$i/" "$CONFIG_FILE"

  echo "${GREEN}[INFO] Avvio run.sh per estrazione n. $i...${RESET}"
  bash "$RUN_SCRIPT"
done

echo ""
echo "${BLUE}✅ Taratura completata."
