#!/bin/bash

CONFIG_PATH="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Estrai solo i parametri numerici e booleani
archivio=$(grep '^url=' "$CONFIG_PATH" | cut -d= -f2 | awk -F- '{print $NF}')
estrazione=$(grep '^ultima_estrazione_da_considerare=' "$CONFIG_PATH" | cut -d= -f2)
offset=$(grep '^range_attivo_offset=' "$CONFIG_PATH" | cut -d= -f2)
len=$(grep '^range_attivo_len=' "$CONFIG_PATH" | cut -d= -f2)
k=$(grep '^decadimento_k=' "$CONFIG_PATH" | cut -d= -f2)
softmax=$(grep '^usa_softmax=' "$CONFIG_PATH" | cut -d= -f2)
beta=$(grep '^softmax_beta=' "$CONFIG_PATH" | cut -d= -f2)
media=$(grep '^media_mobile_attiva=' "$CONFIG_PATH" | cut -d= -f2)
media_n=$(grep '^media_mobile_num_predizioni=' "$CONFIG_PATH" | cut -d= -f2)
soglia=$(grep '^soglia_vicini=' "$CONFIG_PATH" | cut -d= -f2)

# Costruisci nome log pulito
filename="${TIMESTAMP}_${archivio}_${estrazione}_${offset}_${len}_${k}_${softmax}_${beta}_${media}_${media_n}_${soglia}.dat"

echo "reports/${filename}"
