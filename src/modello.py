# Librerie Standard
from math import exp, pi, sin
import configparser
import random

# Librerie Third-party
import numpy as np

# === Costanti ===
RUOTE = [
    'Bari', 'Cagliari', 'Firenze', 'Genova', 'Milano', 'Napoli',
    'Palermo', 'Roma', 'Torino', 'Venezia', 'Nazionale'
]

POSIZIONI = ['1^', '2^', '3^', '4^', '5^']

# === Configurazione ===
_config = configparser.ConfigParser()
_config.read("etc/config.ini")

SOGLIA = int(_config["Output"].get("soglia_vicini", 1))
PESO_VICINI = float(_config["Output"].get("peso_vicini", 0.5))

# === Parametri Quantistici per la Decoerenza ===
RUMORE_FASE = float(_config["Modello"].get("rumore_fase", 0.0))
VARIAZIONE_BETA = float(_config["Modello"].get("variazione_beta", 0.0))

# === Utility ===
def distanza_circolare(a, b):
    """Restituisce la distanza più breve (positiva) tra due cifre modulo 10."""
    a = np.asarray(a)
    b = np.asarray(b)
    return np.minimum((a - b) % 10, (b - a) % 10)

def vicino_digitale(a, b, soglia=1):
    """
    Determina se due numeri a due cifre (00–99) sono "vicini" in senso posizionale-cifrico
    con confronto circolare (modulo 10) tra le cifre decine e unità.
    """
    a = np.asarray(a)
    b = np.asarray(b)
    dec_a, unit_a = divmod(a, 10)
    dec_b, unit_b = divmod(b, 10)

    distanza_unit = distanza_circolare(unit_a, unit_b)
    distanza_dec = distanza_circolare(dec_a, dec_b)

    return (dec_a == dec_b) & (distanza_unit <= soglia) | (unit_a == unit_b) & (distanza_dec <= soglia)

def softmax(x, beta=1.0):
    x = np.array(x)
    e_x = np.exp(beta * (x - np.max(x)))
    return e_x / e_x.sum()

def angolo_fase(cifra):
    return 2 * pi * cifra / 10

def choose_digit(theta):
    if theta < 0:
        theta += 2 * pi
    return int(round((10 * theta) / (2 * pi))) % 10

def scomponi_cifre(matrice):
    return matrice // 10, matrice % 10

def peso_risonante(t, T):
    armoniche = [
        (1.0, pi / 10, 0),
        (0.5, pi / 5, pi / 4)
    ]
    return sum(
        amp * (sin(freq * (T - t) + phase)) ** 2
        for amp, freq, phase in armoniche
    )

def funzione_peso(k, T):
    return lambda t: exp(-k * (T - t)) * peso_risonante(t, T)

def somma_fasi_posizionali(estrazioni, peso_funzione, verbose=False):
    sum_dec = np.zeros((11, 5), dtype=complex)
    sum_uni = np.zeros((11, 5), dtype=complex)

    for i in range(11):
        for j in range(5):
            for t, numero in enumerate(estrazioni[:, i, j]):
                peso = peso_funzione(t)
                d, u = numero // 10, numero % 10

                fase_d = angolo_fase(d) + random.gauss(0, RUMORE_FASE)
                fase_u = angolo_fase(u) + random.gauss(0, RUMORE_FASE)

                sum_dec[i, j] += peso * np.exp(1j * fase_d)
                sum_uni[i, j] += peso * np.exp(1j * fase_u)

                if verbose and i == 0 and j == 0:
                    print(f"t={t} peso={peso:.3f} numero={numero} D={d} fase={fase_d:.2f}")

    return sum_dec, sum_uni

def genera_tabellone(sum_dec, sum_uni, shift_medio=0.0):
    fase_shift = shift_medio * (2 * np.pi / 10)
    ang_dec = np.angle(sum_dec) + fase_shift
    ang_uni = np.angle(sum_uni) + fase_shift
    pred_dec = np.vectorize(choose_digit)(ang_dec)
    pred_uni = np.vectorize(choose_digit)(ang_uni)
    return 10 * pred_dec + pred_uni

def genera_tabellone_softmax(sum_dec, sum_uni, beta_base, shift_medio=0.0):
    tabellone = np.zeros((11, 5), dtype=int)
    fase_shift = shift_medio * (2 * np.pi / 10)
    for i in range(11):
        for j in range(5):
            beta_effettivo = beta_base + random.uniform(-VARIAZIONE_BETA, VARIAZIONE_BETA)

            ang_d = np.angle(sum_dec[i, j]) + fase_shift
            ang_u = np.angle(sum_uni[i, j]) + fase_shift

            prob_d = [np.cos(ang_d - angolo_fase(c)) ** 2 for c in range(10)]
            prob_u = [np.cos(ang_u - angolo_fase(c)) ** 2 for c in range(10)]

            p_dec = softmax(prob_d, beta_effettivo)
            p_uni = softmax(prob_u, beta_effettivo)

            d = np.random.choice(10, p=p_dec)
            u = np.random.choice(10, p=p_uni)

            tabellone[i, j] = 10 * d + u
    return tabellone

def score(predetto, reale, peso_vicini=0.5, soglia=1):
    match = (predetto == reale)
    vicini = vicino_digitale(predetto, reale, soglia) & (~match)
    n_match = np.sum(match)
    n_vicini = np.sum(vicini)
    return n_match + n_vicini * peso_vicini, n_match, n_vicini

def calcola_shift_medio_vicini(predetti, reali, soglia):
    delta_list = []
    for i in range(11):
        for j in range(5):
            p = predetti[i, j]
            r = reali[i, j]
            delta = p - r
            if p != r and abs(delta) <= soglia:
                delta_list.append(delta)
    return sum(delta_list) / len(delta_list) if delta_list else 0.0

def genera_tabellone_softmax_decoerente(sum_dec, sum_uni, beta, shift_medio=0.0, rumore_fase=0.0, variazione_beta=0.0):
    tabellone = np.zeros((11, 5), dtype=int)
    for i in range(11):
        for j in range(5):
            fase_random = np.random.normal(loc=0.0, scale=rumore_fase)
            fase_shift = (shift_medio + fase_random) * (2 * np.pi / 10)

            ang_d = np.angle(sum_dec[i, j]) + fase_shift
            ang_u = np.angle(sum_uni[i, j]) + fase_shift

            beta_noise = np.random.uniform(-variazione_beta, variazione_beta)
            beta_effettivo = max(0.01, beta + beta_noise)

            prob_d = [np.cos(ang_d - angolo_fase(c)) ** 2 for c in range(10)]
            prob_u = [np.cos(ang_u - angolo_fase(c)) ** 2 for c in range(10)]
            p_dec = softmax(prob_d, beta_effettivo)
            p_uni = softmax(prob_u, beta_effettivo)

            d = np.random.choice(10, p=p_dec)
            u = np.random.choice(10, p=p_uni)
            tabellone[i, j] = 10 * d + u
    return tabellone
