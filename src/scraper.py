# =============================================================
# GianKoLotto® – Modulo di scraping delle estrazioni dal web
# =============================================================

# Librerie Standard
import configparser
import re
from typing import List, Tuple

# Librerie Third-party
import numpy as np
import requests
from bs4 import BeautifulSoup

def load_estrazioni_from_url(config_path: str) -> Tuple[np.ndarray, List[int]]:
    """
    Estrae le estrazioni del Lotto da una pagina HTML.

    Args:
        config_path: Percorso al file .ini contenente l'URL della sorgente.

    Returns:
        Una tupla composta da:
            - np.ndarray delle estrazioni con shape (n, 11, 5)
            - Lista di etichette numeriche delle estrazioni
    """
    # Carica configurazione
    config = configparser.ConfigParser()
    config.read(config_path)
    url = config['Scraping']['url']

    # Richiesta HTTP
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    estrazioni = []
    etichette = []

    # Cerca tutte le tabelle nel documento HTML
    for tabella in soup.find_all('table'):
        blocco = []
        label = None

        for riga in tabella.find_all('tr'):
            celle = riga.find_all(['td', 'th'])

            # Etichetta numerica (es. "Estrazione n. ???")
            if label is None:
                testo = riga.get_text()
                match = re.search(r'Estrazione\s+n\.\s*(\d+)', testo)
                if match:
                    label = int(match.group(1))

            # Righe con 5 numeri + nome ruota (totale 6 celle)
            if len(celle) == 6:
                try:
                    numeri = [int(c.get_text()) for c in celle[1:]]
                    blocco.append(numeri)
                except ValueError:
                    continue  # Salta righe non numeriche

        if len(blocco) == 11:
            estrazioni.append(blocco)
            etichette.append(label if label is not None else -1)

    if not estrazioni:
        raise ValueError("Nessuna estrazione valida trovata nella pagina HTML.")

    arr = np.array(estrazioni)[::-1]  # Ordine crescente
    etichette = etichette[::-1]

    if arr.shape[1:] != (11, 5):
        raise ValueError(f"Formato estrazioni inconsistente: trovato {arr.shape}")

    return arr, etichette
