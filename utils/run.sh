#!/bin/bash
# ==========================================================
# GianKoLotto® – Avvio predizione quantistica Lotto
# Questo script lancia il "main predictor" in src/main.py,
# gestendo il PYTHONPATH e controllando le dipendenze.
# ==========================================================

# Calcola i path assoluti necessari
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$ROOT_DIR/src"

# Salva PYTHONPATH corrente e lo estende con src/
OLD_PYTHONPATH="$PYTHONPATH"
export PYTHONPATH="$SRC_DIR${PYTHONPATH:+:$PYTHONPATH}"

echo ""
echo "GianKoLotto® | Sistema Interferenziale Posizionale"
echo "--------------------------------------------------"
echo ""
echo "🕒 Avvio: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Verifica che src/main.py esista
if [[ ! -f "$SRC_DIR/main.py" ]]; then
    echo "❌ Errore: il file main.py non esiste in $SRC_DIR"
    exit 1
fi

# Verifica la presenza delle dipendenze Python richieste
REQUIRED_PKG=("requests" "bs4" "numpy")
for pkg in "${REQUIRED_PKG[@]}"; do
    if ! python -m pip show "$pkg" >/dev/null 2>&1; then
        echo "❌ Pacchetto mancante: '$pkg'"
        echo "   ➤ Installalo con: pip install $pkg"
        export PYTHONPATH="$OLD_PYTHONPATH"
        exit 1
    fi
done

# Esegue il programma principale
python "$SRC_DIR/main.py"
STATUS=$?

# Controlla esito dell'esecuzione
if [[ $STATUS -ne 0 ]]; then
    echo "❌ Errore durante l'esecuzione di main.py (codice $STATUS)"
    export PYTHONPATH="$OLD_PYTHONPATH"
    exit $STATUS
fi

# Ripristina il PYTHONPATH originale
export PYTHONPATH="$OLD_PYTHONPATH"

echo ""
echo "✅ Predizione completata con successo."
echo ""
echo "🕒 Fine:  $(date '+%Y-%m-%d %H:%M:%S')"
