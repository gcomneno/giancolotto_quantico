#!/bin/bash
set -e  # Esce se un comando fallisce

start_time=$(date +%s)

echo ""
echo "🚀 Inizio taratura completa GianKoLotto Quantico®..."
echo "🕒 Inizio: $(date +"%Y-%m-%d %H:%M:%S")"
echo ""

bash utils/taratura_k.sh
bash utils/taratura_softmax.sh
bash utils/taratura_media_mobile.sh
bash utils/taratura_range.sh

end_time=$(date +%s)
elapsed=$((end_time - start_time))

# Calcolo tempo in formato leggibile
minutes=$((elapsed / 60))
seconds=$((elapsed % 60))

echo ""
echo "✅ Tutte le tarature completate con successo."
echo "🕒 Fine: $(date +"%Y-%m-%d %H:%M:%S")"
echo "⏱️ Tempo totale: ${minutes} min ${seconds} sec"
echo ""
