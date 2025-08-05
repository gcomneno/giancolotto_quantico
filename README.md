# 🎰 GianKoLotto Quantico®  

**Sistema Interferenziale Posizionale per la Predizione Quantistica del Lotto**  
Ultimo aggiornamento: 05 August 2025

---

## 👴 A chi è rivolto
Questo progetto è pensato per:
- curiosi e appassionati di **statistica applicata** e **fisica quantistica leggera**;
- chi desidera **giocare con i numeri del Lotto** in modo intelligente e scientifico;
- e sì, anche tu, pensionato curioso che hai tempo, pazienza e voglia di capire come funziona questo marchingegno!

---

## 🧠 Cos’è GianKoLotto Quantico®
Un sistema di predizione numerica che si basa su:
- **modelli di interferenza quantistica** (ispirati agli orologi di Feynman),
- **scomposizione delle cifre** delle estrazioni,
- **somma vettoriale di fasi complesse** per ogni ruota e posizione,
- **pesatura armonica con decadimento temporale**,
- **softmax ispirato da Boltzmann** per estrarre la probabilità che un numero esca!

Il tutto condito con una buona dose di Python, Bash e tarature rigorose.

---

## 📦 Struttura del progetto

```
giankolotto_quantico/
├── etc/                   # Configurazione (config.ini)
├── src/                   # Tutti i sorgenti Python
│   ├── main.py            # Punto di ingresso principale
│   ├── scraper.py         # Parser HTML delle estrazioni
│   ├── modello.py         # Algoritmi di predizione
│   └── tuning.py          # Tuning avanzato K + Softmax
├── utils/                 # Script Bash per automazione e tuning
│   ├── run.sh
│   ├── run_loop.sh
│   ├── taratura_k.sh
│   ├── taratura_softmax.sh
│   ├── taratura_range.sh
│   ├── taratura_media_mobile.sh
│   ├── taratura_k_softmax.sh
│   └── all.sh
├── Makefile               # Interfaccia comandi facilitata
└── README.md              # Questo file
```

---

## ⚙️ Requisiti

- Python ≥ 3.8
- librerie Python:
  - `numpy`
  - `requests`
  - `beautifulsoup4`
  - `tqdm`
- Ambiente Bash (consigliato: Git Bash o WSL su Windows)

Puoi installa i pacchetti richiesti manualmente oppure con:

```bash
pip install -r requirements.txt
```

---

## 🧾 Come iniziare

1. Clona il progetto:
   ```bash
   git clone https://github.com/gcomneno/giankolotto_quantico.git
   cd giankolotto_quantico
   ```

2. Modifica le impostazioni nel file `etc/config.ini` secondo le tue esigenze (vedi sezione dedicata).

3. Lancia il sistema predittivo con:
   ```bash
   make run
   ```

   Otterrai la predizione dei 55 numeri (11 ruote x 5 posizioni), con confronto con l’estrazione reale.

---

## 🛠️ Comandi disponibili

| Comando        | Azione                                                             |
|----------------|--------------------------------------------------------------------|
| `make run`     | Esegue la predizione una tantum                                    |
| `make loop`    | Lancia una serie di predizioni su range di estrazioni              |
| `make k`       | Esegue la taratura del parametro `k` (decadimento)                 |
| `make beta`    | Esegue la taratura del parametro `softmax_beta`                    |
| `make media`   | Testa il miglior numero di predizioni per la media mobile          |
| `make range`   | Ottimizza il range attivo delle estrazioni                         |
| `make all`     | Esegue **tutte le tarature** in sequenza (occhio: lunga durata!)   |
| `make tuning`  | Tuning avanzato `k + softmax` su griglia incrociata                |

---

## 🧪 Filosofia del sistema

Il cuore del sistema è la **trasformata quantistica** delle estrazioni precedenti:

1. Ogni numero è **scomposto** in cifra delle decine e unità.
2. Ogni cifra è convertita in **fase angolare** (tra 0 e 2π).
3. Si calcola la somma vettoriale complessa delle fasi, pesata nel tempo.
4. Dalla direzione della somma si stimano le **probabilità di uscita**.
5. Le previsioni possono essere:
   - "secche" (fase più vicina),
   - "probabilistiche" (softmax su 10 cifre),
   - "medie mobili" (previsione aggregata su n run).

---

### 📐 Dettaglio fasi angolari

Gli "orologi di Feynman" che ho usato sono strutturati per ruotare lungo un **cerchio di 2π radianti**, suddiviso equamente in **10 fasi**, una per ciascuna cifra da 0 a 9. Ogni cifra è mappata su una fase angolare specifica, con incremento costante:

| Cifra | Fase (rad) | Fase (gradi) |
| ----- | ---------- | ------------ |
| 0     | 0.000      | 0°           |
| 1     | 0.628      | 36°          |
| 2     | 1.257      | 72°          |
| 3     | 1.885      | 108°         |
| 4     | 2.513      | 144°         |
| 5     | 3.142      | 180°         |
| 6     | 3.770      | 216°         |
| 7     | 4.398      | 252°         |
| 8     | 5.027      | 288°         |
| 9     | 5.655      | 324°         |

---

## 🧾 Esempio di output
```text
GianKoLotto® | Sistema Interferenziale Posizionale
--------------------------------------------------

Range attivo usato: 95:100

Milano     83   27*  52   46   18*
Roma       90   45   77*  12   26@
...

Totale match esatti: 8/55
Totale match vicini: 1|14/55
```

Legenda:
- `@` → numero esatto
- `*` → numero vicino (entro soglia, es. ±4)

---

## 🧩 Il file `config.ini`
Contiene tutte le opzioni di personalizzazione:

```ini
[Scraping]
url = https://...

[Modello]
decadimento_k = 0.45
range_attivo_offset = 0
range_attivo_len = 6
media_mobile_attiva = False
media_mobile_num_predizioni = 3
usa_softmax = True
softmax_beta = 14.0

[Output]
soglia_vicini = 5
ultima_estrazione_da_considerare = 135
```

---

## 🧘 Filosofia Zen del Progetto

Questo sistema **non garantisce vincite**, ma offre:
- una struttura chiara e modulare per fare analisi numeriche;
- un ambiente per imparare Python, statistica e automazione;
- una visione "quantistica" e "poetica" dei numeri del Lotto.

---

## 📌 Conclusioni

Il sistema GianKoLotto Quantico® ha mostrato **segnali incoraggianti di predizione non casuale**, ma **non è ancora predittivo in senso pieno**. 
È un oscillatore informativo in risonanza con il passato, **non un indovino**. 
Le basi sono solide, e il **comportamento è coerente** ma si tratta ancora di capire dove "premere" per **amplificare le probabilità reali**.

---

## 🧙‍♂️ Ringraziamenti

Un grazie speciale a:
- Feynman, per l’idea degli orologi quantistici,
- NumPy, per il cuore matematico,
- Il pensionato curioso, che ha ancora voglia di sognare ✨

---

## 🛡️ Licenza

Questo progetto è rilasciato con **licenza MIT**.  
Usalo, modificane il codice, ma gioca responsabilmente!