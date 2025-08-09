# === Makefile per GianKoLotto Quantico® ===

# Comandi supportati
.PHONY: run loop k beta media range tuning all help verifica

# Percorsi
CONFIG_FILE := etc/config.ini
LOG_RUNNER := utils/log_and_run.sh
VERIFICA_SCRIPT := ./utils/verifica.sh

# === Comandi principali ===

run:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) run

loop:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) run_loop

k:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_k

beta:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_softmax

media:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_media_mobile

range:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_range

tuning:
	@bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_k_softmax

# Nuovo comando per eseguire la verifica con due numeri
verifica:
	@bash $(VERIFICA_SCRIPT) $(num1) $(num2)

all:
	@echo "🌀 Inizio taratura completa GianKoLotto Quantico®..."
	@start=$$(date +%s); \
	bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_k && \
	bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_softmax && \
	bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_media_mobile && \
	bash $(LOG_RUNNER) $(CONFIG_FILE) taratura_range; \
	end=$$(date +%s); \
	elapsed=$$((end - start)); \
	echo "⏱️  Durata totale: $$((elapsed / 60)) min $$((elapsed % 60)) sec"

help:
	@echo "📚 Comandi disponibili:"
	@echo "  make run       → Esegue predizione singola"
	@echo "  make loop      → Esegue batch su range di estrazioni"
	@echo "  make k         → Taratura parametro decadimento k"
	@echo "  make beta      → Taratura parametro SoftMax (β)"
	@echo "  make media     → Taratura media mobile"
	@echo "  make range     → Taratura intervallo estrazioni"
	@echo "  make tuning    → Ricerca combinata k + SoftMax"
	@echo "  make all       → Esegue tutte le tarature principali"
	@echo "  make verifica  → Esegue verifica con due numeri (es: make verifica num1=46 num2=82)"
