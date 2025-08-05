# === Librerie Standard ===
import configparser
from math import exp
from itertools import product
from datetime import datetime

# === Librerie Third-party ===
import numpy as np
from tqdm import tqdm

# === Moduli Progetto ===
from scraper import load_estrazioni_from_url
from modello import scomponi_cifre, score, somma_fasi_posizionali, angolo_fase

# === Parametri ===
K_VALUES = np.round(np.arange(0.40, 0.60, 0.01), 2)
SOFTMAX_VALUES = np.arange(14.0, 16.0, 0.1)
BLOCCHI = 28
LUNGHEZZA = 6
SOGLIA = 1
PESO_VICINI = 0.5

# === Funzioni ===
def softmax(vec, beta):
    vec = np.array(vec)
    e = np.exp(beta * (vec - np.max(vec)))
    return e / e.sum()

def genera_tabellone_softmax(sum_dec, sum_uni, beta):
    pred = np.zeros((11, 5), dtype=int)
    cifre = np.arange(10)
    for i in range(11):
        for j in range(5):
            probs_dec = softmax(np.cos(angolo_fase(cifre) - np.angle(sum_dec[i, j])), beta)
            probs_uni = softmax(np.cos(angolo_fase(cifre) - np.angle(sum_uni[i, j])), beta)
            dec = np.argmax(probs_dec)
            uni = np.argmax(probs_uni)
            pred[i, j] = 10 * dec + uni
    return pred

# === Entry Point ===
if __name__ == "__main__":
    print("\n=== TUNING GIANKOLOTTO QUANTICO | K & SOFTMAX ===\n")

    config = configparser.ConfigParser()
    config.read("../etc/config.ini")

    estrazioni, _ = load_estrazioni_from_url("./etc/config.ini")
    n = estrazioni.shape[0]

    risultati = []
    print(f"{'k':<6} {'softmax':<8} {'score':<6} {'match':<7} {'vicini'}")
    print("-" * 38)

    for blocco_idx in tqdm(range(BLOCCHI), desc="Blocchi testati"):
        start = n - LUNGHEZZA - blocco_idx - 1
        stop = start + LUNGHEZZA
        reale_idx = stop

        if reale_idx >= n or start < 0:
            continue

        blocco = estrazioni[start:stop]
        reale = estrazioni[reale_idx]
        decine, unita = scomponi_cifre(blocco)

        for k, beta in tqdm(product(K_VALUES, SOFTMAX_VALUES),
                            desc=f"Grid k/softmax [blocco {blocco_idx+1}]",
                            leave=False,
                            total=len(K_VALUES)*len(SOFTMAX_VALUES)):

            peso_funzione = lambda t: exp(-k * (LUNGHEZZA - 1 - t))
            somma_dec, somma_uni = somma_fasi_posizionali(blocco, peso_funzione)
            predetto = genera_tabellone_softmax(somma_dec, somma_uni, beta)
            sc, m, v = score(predetto, reale)

            risultati.append({
                "k": round(k, 2),
                "softmax": round(beta, 2),
                "score": sc,
                "match": m,
                "vicini": v
            })

    # Ordina e mostra top
    ordinati = sorted(risultati, key=lambda x: x["score"], reverse=True)

    print("\n=== MIGLIORI PARAMETRI TROVATI ===\n")
    print(f"{'rank':<5} {'k':<6} {'softmax':<8} {'score':<6} {'match':<7} {'vicini'}")
    print("-" * 44)
    for idx, r in enumerate(ordinati[:10], 1):
        print(f"{idx:<5} {r['k']:<6.2f} {r['softmax']:<8.2f} {r['score']:<6.1f} {r['match']:<7} {r['vicini']}")
