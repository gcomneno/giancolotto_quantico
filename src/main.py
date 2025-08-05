# Librerie Standard
import sys
import configparser
from collections import Counter

# Librerie Third-party
import numpy as np

# Moduli Progetto
from scraper import load_estrazioni_from_url
from modello import vicino_digitale  
from modello import (
    RUOTE, funzione_peso, somma_fasi_posizionali,
    genera_tabellone, genera_tabellone_softmax,
    score, calcola_shift_medio_vicini,
    genera_tabellone_softmax_decoerente
)

def main():
    # Parametri dalla riga di comando
    verbose = "-v" in sys.argv or "--verbose" in sys.argv

    # Parametri dal file di configurazione
    config = configparser.ConfigParser()
    config.read('./etc/config.ini')

    k = float(config['Modello'].get('decadimento_k', '0'))
    range_start = int(config['Modello']['range_attivo_offset'])
    range_stop = int(config['Modello']['range_attivo_len'])
    soglia = int(config['Output']['soglia_vicini'])
    peso_vicini = float(config['Output']['peso_vicini'])
    ultima = int(config['Scraping']['ultima_estrazione_da_considerare'])
    media_mobile = config['Modello'].getboolean('media_mobile_attiva', fallback=False)
    n_pred = int(config['Modello'].get('media_mobile_num_predizioni', fallback=1))
    usa_softmax = config['Modello'].getboolean('usa_softmax', fallback=False)
    beta = float(config['Modello'].get('softmax_beta', fallback=1.0))
    rumore_fase = float(config['Modello'].get('rumore_fase', '0.0'))
    variazione_beta = float(config['Modello'].get('variazione_beta', '0.0'))

    # Acquisizione Estrazioni
    estrazioni, _ = load_estrazioni_from_url('./etc/config.ini')

    # Applica Filtri
    n = estrazioni.shape[0]
    range_len = abs(range_start - range_stop)

    if n < range_len:
        print(f"Solo {n} estrazioni disponibili. Adattamento dinamico del range attivo.")
        range_start, range_stop = -n, 0

    idx_start = ultima - abs(range_start) - abs(range_stop)
    idx_stop = idx_start + abs(range_stop) - 1
    if verbose:
        print(f"Range attivo usato: {idx_start + 1}:{idx_stop + 1}\n")

    range_attivo = estrazioni[idx_start:idx_stop + 1]
    reale_idx = ultima
    reale = estrazioni[reale_idx] if 0 <= reale_idx < n else None

    if verbose:
        print(range_attivo, '\n')

    T = len(range_attivo) - 1
    peso_fn = funzione_peso(k, T)
    somma_dec, somma_uni = somma_fasi_posizionali(range_attivo, peso_fn, verbose=verbose)

    if verbose:
        print(f"\nEstrazioni caricate: shape {estrazioni.shape}")

    shift_medio = 0.0
    if usa_softmax and media_mobile:
        if verbose:
            print(f"SoftMAX: {beta} | Media Mobile: {n_pred} | Decoerenza: {rumore_fase} rad\n")

        pred_temp = genera_tabellone_softmax(somma_dec, somma_uni, beta)
        if reale is not None:
            shift_medio = calcola_shift_medio_vicini(pred_temp, reale, soglia)
        tabelloni = [
            genera_tabellone_softmax_decoerente(
                somma_dec, somma_uni, beta, shift_medio, rumore_fase, variazione_beta
            ) for _ in range(n_pred)
        ]
        predetto = np.zeros((11, 5), dtype=int)
        for i in range(11):
            for j in range(5):
                numeri = [tab[i, j] for tab in tabelloni]
                predetto[i, j] = Counter(numeri).most_common(1)[0][0]

    elif usa_softmax:
        if verbose:
            print(f"SoftMAX: {beta} | Decoerenza: {rumore_fase} rad\n")

        predetto = genera_tabellone_softmax_decoerente(
            somma_dec, somma_uni, beta, shift_medio, rumore_fase, variazione_beta
        )

    else:
        predetto = genera_tabellone(somma_dec, somma_uni, shift_medio)

    # Stampa tabellone predetto
    for i in range(11):
        riga = []
        for j in range(5):
            numero = predetto[i, j]
            simbolo = " "
            if reale is not None:
                r = reale[i, j]
                if numero == r:
                    simbolo = "@"
                elif vicino_digitale(numero, r, soglia):
                    simbolo = "*"
            riga.append(f"{numero:02d}{simbolo}")
        print(f"{RUOTE[i]:<10} " + "  ".join(riga))

    # Stampa tabellone reale
    if reale is not None:
        print(f"\nCONFRONTO CON L'ESTRAZIONE REALE (n. {reale_idx + 1})")
        print("---------- ---------------------")
        for i in range(11):
            riga = "  ".join(f"{reale[i, j]:02d}" for j in range(5))
            print(f"{RUOTE[i]:<10} {riga}")

        score_tot, match, vicini = score(predetto, reale, peso_vicini, soglia)

        fase_shift = shift_medio * (2 * np.pi / 10)
        if verbose:
            print(f"\nshift_medio: {shift_medio:.3f} fase_corr +- {fase_shift:.3f} rad")

        print(f"\n### SCORE: {score_tot:.1f} | MATCH: {match} | VICINI: {vicini}")

if __name__ == "__main__":
    main()
