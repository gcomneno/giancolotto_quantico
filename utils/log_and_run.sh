#!/bin/bash

CONFIG_PATH="$1"
ACTION="$2"

# === Calcola il path assoluto della root del progetto ===
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTS_DIR="$PROJECT_ROOT/reports"
GEN_LOG_SCRIPT="$PROJECT_ROOT/utils/gen_report_name.sh"
ACTION_SCRIPT="$PROJECT_ROOT/utils/${ACTION}.sh"

# === Crea la cartella reports se non esiste ===
mkdir -p "$REPORTS_DIR"

# === Verifica esistenza script richiesto ===
if [ ! -f "$ACTION_SCRIPT" ]; then
    echo "❌ Errore: script '${ACTION_SCRIPT}' non trovato."
    exit 1
fi

# === Genera nome file di log ===
if [ ! -f "$GEN_LOG_SCRIPT" ]; then
    echo "❌ Errore: script '${GEN_LOG_SCRIPT}' non trovato."
    exit 1
fi

OUTPUT_PATH=$("$GEN_LOG_SCRIPT" "$CONFIG_PATH")

# === Estrai parametri attivi dal config.ini ===
estrazione=$(grep '^ultima_estrazione_da_considerare=' "$CONFIG_PATH" | cut -d= -f2)
offset=$(grep '^range_attivo_offset=' "$CONFIG_PATH" | cut -d= -f2)
lunghezza=$(grep '^range_attivo_len=' "$CONFIG_PATH" | cut -d= -f2)
k=$(grep '^decadimento_k=' "$CONFIG_PATH" | cut -d= -f2)
softmax=$(grep '^usa_softmax=' "$CONFIG_PATH" | cut -d= -f2)
beta=$(grep '^softmax_beta=' "$CONFIG_PATH" | cut -d= -f2)
media=$(grep '^media_mobile_attiva=' "$CONFIG_PATH" | cut -d= -f2)
media_n=$(grep '^media_mobile_num_predizioni=' "$CONFIG_PATH" | cut -d= -f2)
soglia=$(grep '^soglia_vicini=' "$CONFIG_PATH" | cut -d= -f2)

# === Mostra intestazione informativa ===
echo -e "📄 Config: $CONFIG_PATH"
echo -e "🚀 Azione: $ACTION"
echo -e "📝 Log:    $OUTPUT_PATH"
echo ""
echo -e "🔧 Parametri attivi:"
echo "  📅 Estrazione:      $estrazione"
echo "  ⏳ Range:           offset=$offset | len=$lunghezza"
echo "  📉 Decadimento k:   $k"
echo "  🧠 Softmax:         $softmax (β=$beta)"
echo "  🔁 Media Mobile:    $media (n=$media_n)"
echo "  🎯 Soglia vicini:   $soglia"
echo ""

# === Esecuzione con log ===
bash "$ACTION_SCRIPT" 2>&1 | tee "$OUTPUT_PATH"

if [[ "$ACTION" != "taratura_k_softmax" ]]; then
    # === Esiti Totali ===
    echo "--------------------------"
    match_esatti=$(grep -Eo 'MATCH: [0-9]+' "./$OUTPUT_PATH" | awk -F'[/ ]+' '{sum += $2} END {print sum}')
    match_vicini=$(grep -Eo 'VICINI: [0-9]+' "./$OUTPUT_PATH" | awk -F'[/ ]+' '{sum += $2} END {print sum}')

    if [[ -n "$match_esatti" ]]; then
        echo "✔️  Match esatti: $match_esatti"
    else
        echo "❌ Match esatti NON trovati nel report."
    fi

    if [[ -n "$match_vicini" ]]; then
        echo "✔️  Match vicini: $match_vicini"
    else
        echo "❌ Match vicini NON trovati nel report."
    fi

    # === Conferma finale ===
    echo -e "\n✅ Output salvato in: $OUTPUT_PATH"
fi