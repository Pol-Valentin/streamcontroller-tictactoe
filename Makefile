PLUGIN_ID = com_pol_tictactoe
FLATPAK_PATH = $(HOME)/.var/app/com.core447.StreamController/data/plugins/$(PLUGIN_ID)
NATIVE_PATH = $(HOME)/.config/streamcontroller/plugins/$(PLUGIN_ID)

.PHONY: link install uninstall clean status

# Symlink pour développement (recommandé)
link:
	@if [ -e "$(FLATPAK_PATH)" ]; then \
		rm -rf "$(FLATPAK_PATH)"; \
	fi
	ln -sf "$(CURDIR)" "$(FLATPAK_PATH)"
	@echo "Lié à $(FLATPAK_PATH)"

# Copie pour installation définitive
install:
	@if [ -e "$(FLATPAK_PATH)" ]; then \
		rm -rf "$(FLATPAK_PATH)"; \
	fi
	cp -r "$(CURDIR)" "$(FLATPAK_PATH)"
	@echo "Installé dans $(FLATPAK_PATH)"

# Supprime le plugin
uninstall:
	rm -rf "$(FLATPAK_PATH)"
	rm -rf "$(NATIVE_PATH)"
	@echo "Plugin supprimé"

# Nettoie les fichiers temporaires
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Affiche le statut d'installation
status:
	@if [ -L "$(FLATPAK_PATH)" ]; then \
		echo "Lié (dev): $(FLATPAK_PATH) -> $$(readlink $(FLATPAK_PATH))"; \
	elif [ -d "$(FLATPAK_PATH)" ]; then \
		echo "Installé (copie): $(FLATPAK_PATH)"; \
	else \
		echo "Non installé"; \
	fi
