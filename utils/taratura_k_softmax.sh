#!/bin/bash

# Percorsi principali
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$ROOT_DIR/src"

# Esporta PYTHONPATH per permettere import da src.*
export PYTHONPATH="$SRC_DIR${PYTHONPATH:+:$PYTHONPATH}"

echo ""
echo "=== TUNING GIANKOLOTTO QUANTICO | K + SOFTMAX ==="
echo "📍 Script: tuning.py"
echo "📦 PythonPath: $PYTHONPATH"
echo ""
echo "🕒 Avvio: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Esegui tuning.py dentro src/
python "$SRC_DIR/tuning.py"

echo ""
echo "✅ Tuning completato con successo."
echo ""
echo "🕒 Fine:  $(date '+%Y-%m-%d %H:%M:%S')"
