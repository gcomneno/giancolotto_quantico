# === Librerie Standard ===
import os
import configparser
from math import exp
from itertools import product
from datetime import datetime

# === Librerie Third-party ===
import numpy as np
from tqdm import tqdm
from scipy.stats import entropy

# === Moduli Progetto ===
from scraper import load_estrazioni_from_url
from modello import scomponi_cifre, score, somma_fasi_posizionali, angolo_fase

# === Parametri ===
K_VALUES=np.round(np.arange(0.40, 0.43, 0.01), 2)
SOFTMAX_VALUES=np.arange(14.2, 14.6, 0.1)
BLOCCHI=89
LUNGHEZZA=28
SOGLIA=1
PESO_VICINI=0.25
SOGLIA_SCORE_FINESTRA=1.0       # Soglia minima di score per considerare una finestra predittiva significativa
ALPHA=0.8                       # Peso score vs risonanza (funzione obiettivo F)
#| `ALPHA` | Interpretazione                                              |
#| ------: | ------------------------------------------------------------ |
#| **1.0** | Solo `score`, ignora la coerenza fisica                      |
#| **0.8** | Priorità alta allo `score`, ma considera ancora la risonanza |
#| **0.6** | Bilanciamento 60% score / 40% risonanza                      |
#| **0.5** | Equilibrio perfetto: score = risonanza                       |
#| **0.2** | Dai priorità alla risonanza quantistica                      |
#| **0.0** | Solo coerenza fisica, ignora performance numeriche           |


# === Funzioni ===
def trova_finestre_predittive(risultati, soglia_score=2.0):
    """
    Restituisce una lista di parametri che:
    - hanno score ≥ soglia
    - sono massimi locali di risonanza
    """
    finestre = []
    for i in range(1, len(risultati) - 1):
        prec = risultati[i - 1]
        curr = risultati[i]
        succ = risultati[i + 1]
        if curr["score"] >= soglia_score:
            if curr["risonanza"] > prec["risonanza"] and curr["risonanza"] > succ["risonanza"]:
                finestre.append(curr)
    return finestre

def analizza_stato_quantico(sum_dec, sum_uni):
    """
    Analizza coerenza del vettore quantistico.
    Non richiede conoscenza del risultato reale.
    """
    report = {
        'media_modulo_dec': float(np.mean(np.abs(sum_dec))),
        'media_modulo_uni': float(np.mean(np.abs(sum_uni))),
        'std_angolo_dec': float(np.std(np.angle(sum_dec))),
        'std_angolo_uni': float(np.std(np.angle(sum_uni))),
    }
    return report

def calcola_risonanza(mod_dec, mod_uni, entropia_media, epsilon=1e-6):
    media_modulo = (mod_dec + mod_uni) / 2
    return media_modulo / (entropia_media + epsilon)

def analizza_stato_quantico(sum_dec, sum_uni, probs_tab=None):
    report = {
        'media_modulo_dec': float(np.mean(np.abs(sum_dec))),
        'media_modulo_uni': float(np.mean(np.abs(sum_uni))),
        'std_angolo_dec': float(np.std(np.angle(sum_dec))),
        'std_angolo_uni': float(np.std(np.angle(sum_uni))),
    }

    if probs_tab:
        entropie = []
        for i in range(11):
            for j in range(5):
                p_d, p_u = probs_tab[i][j]
                entropie.append(entropy(p_d))
                entropie.append(entropy(p_u))
        report['entropia_media'] = float(np.mean(entropie))
        report['entropia_std'] = float(np.std(entropie))

    return report

def softmax(vec, beta):
    vec = np.array(vec)
    e = np.exp(beta * (vec - np.max(vec)))
    return e / e.sum()

def genera_tabellone_softmax(sum_dec, sum_uni, beta):
    pred = np.zeros((11, 5), dtype=int)
    probs_tab = {}
    cifre = np.arange(10)

    for i in range(11):
        probs_tab[i] = {}
        for j in range(5):
            ang_d = np.angle(sum_dec[i, j])
            ang_u = np.angle(sum_uni[i, j])

            cos_d = np.cos(angolo_fase(cifre) - ang_d)
            cos_u = np.cos(angolo_fase(cifre) - ang_u)

            probs_dec = softmax(cos_d ** 2, beta)
            probs_uni = softmax(cos_u ** 2, beta)

            dec = np.argmax(probs_dec)
            uni = np.argmax(probs_uni)

            pred[i, j] = 10 * dec + uni
            probs_tab[i][j] = (probs_dec, probs_uni)

    return pred, probs_tab

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

            predetto, probs_tab = genera_tabellone_softmax(somma_dec, somma_uni, beta)
            sc, m, v = score(predetto, reale, PESO_VICINI, SOGLIA)
            feedback = analizza_stato_quantico(somma_dec, somma_uni, probs_tab)

            risonanza = calcola_risonanza(
                feedback['media_modulo_dec'],
                feedback['media_modulo_uni'],
                feedback['entropia_media']
            )

            F = ALPHA * sc + (1 - ALPHA) * risonanza

            risultati.append({
                "k": round(k, 2),
                "softmax": round(beta, 2),
                "score": sc,
                "match": m,
                "vicini": v,
                "mod_dec": round(feedback['media_modulo_dec'], 4),
                "mod_uni": round(feedback['media_modulo_uni'], 4),
                "std_ang_dec": round(feedback['std_angolo_dec'], 4),
                "std_ang_uni": round(feedback['std_angolo_uni'], 4),
                "entropia_media": round(feedback['entropia_media'], 4),
                "entropia_std": round(feedback['entropia_std'], 4),
                "risonanza": round(risonanza, 4),
                "F": round(F, 4)
            })

    ordinati_risonanti = sorted(risultati, key=lambda x: x["risonanza"], reverse=True)
    finestre = trova_finestre_predittive(ordinati_risonanti, soglia_score=SOGLIA_SCORE_FINESTRA)

    if finestre:
        print("\n=== FINESTRE PREDITTIVE OTTIMALI ===\n")
        print(f"{'k':<6} {'β':<7} {'score':<6} {'rison.':<8} {'match':<6} {'entro':<7}")
        print("-" * 60)
        for f in finestre:
            print(f"{f['k']:<6} {f['softmax']:<7} {f['score']:<6.1f} {f['risonanza']:<8.4f} {f['match']:<6} {f['entropia_media']:<7.4f}")
    else:
        print("\nNessuna finestra predittiva stabile individuata con score >= 2.0 e massimo locale di risonanza!")

    print("\n=== MIGLIORI PARAMETRI TROVATI ===\n")
    ordinati_F = sorted(risultati, key=lambda x: x["F"], reverse=True)
    best = ordinati_F[0]

    print("\n=== PARAMETRI OTTIMI (funzione obiettivo F = score/risonanza) ===\n")
    print(f"{'rank':<5} {'k':<6} {'Beta':<7} {'F':<8} {'score':<6} {'match':<6} {'rison.':<8}")
    print("-" * 60)
    for idx, r in enumerate(ordinati_F[:10], 1):
        print(f"{idx:<5} {r['k']:<6} {r['softmax']:<7} {r['F']:<8.4f} {r['score']:<6.1f} {r['match']:<6} {r['risonanza']:<8.4f}")

    # Parametri dal file di configurazione
    config_path = "./etc/config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)

    config['Modello']['decadimento_k'] = str(best['k'])
    config['Modello']['softmax_beta'] = str(best['softmax'])

    with open(config_path, 'w') as configfile:
        config.write(configfile)

    print(f"\nMigliori parametri salvati in config.ini:")
    print(f"-> decadimento_k = {best['k']}")
    print(f"-> softmax_beta  = {best['softmax']}")
