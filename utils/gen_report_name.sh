#!/bin/bash

CONFIG_PATH="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Helper: Estrai valore da sezione usando awk (ignora [DEFAULT])
extract() {
    grep -A 10 "^\[$2\]" "$CONFIG_PATH" | grep "^$1=" | cut -d= -f2
}

# Estrai parametri
archivio=$(grep '^url=' "$CONFIG_PATH" | cut -d= -f2 | awk -F- '{print $NF}')
estrazione=$(extract "ultima_estrazione_da_considerare" "Scraping")
offset=$(extract "range_attivo_offset" "Modello")
len=$(extract "range_attivo_len" "Modello")
k=$(extract "decadimento_k" "Modello")
softmax=$(extract "usa_softmax" "Modello")
beta=$(extract "softmax_beta" "Modello")
shift=$(extract "shift_medio" "Modello")
adattamento=$(extract "auto_adattamento" "Modello")
media=$(extract "media_mobile_attiva" "Modello")
media_n=$(extract "media_mobile_num_predizioni" "Modello")
soglia=$(extract "soglia_vicini" "Output")

# Aggiuntivi (opzionali)
rumore=$(extract "rumore_fase" "Modello")
var_beta=$(extract "variazione_beta" "Modello")

# Costruzione nome log coerente e leggibile
filename="${TIMESTAMP}_${archivio}_${estrazione}_${offset}_${len}_k${k}_b${beta}_s${shift}_soft${softmax}_med${media}_${media_n}_a${adattamento}_r${rumore}_vb${var_beta}_sog${soglia}.dat"

echo "reports/${filename}"
