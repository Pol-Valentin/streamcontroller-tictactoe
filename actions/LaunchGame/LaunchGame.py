from src.backend.PluginManager.ActionBase import ActionBase
from loguru import logger as log

import globals as gl
import os


class LaunchGame(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "tictactoe.png")
        if os.path.exists(icon_path):
            self.set_media(media_path=icon_path, size=0.75)
        else:
            self.set_center_label("TicTacToe", font_size=12)
        self.set_background_color([80, 60, 100, 255])

    def on_key_down(self) -> None:
        self.launch_game()

    def launch_game(self) -> None:
        """Crée et charge la page de jeu."""
        deck_controller = self.deck_controller
        if deck_controller is None:
            log.error("No deck controller")
            return

        # Sauvegarde la page actuelle pour le retour
        self.plugin_base.back_page = deck_controller.active_page

        # Reset le jeu
        self.plugin_base.reset_game()

        # Crée la page de jeu
        page_dict = self._create_game_page()

        # Enregistre et charge la page (comme k9s_manager)
        page_name = "TicTacToe_Game"
        gl.page_manager.add_page(page_name, page_dict)
        page_path = os.path.join(gl.DATA_PATH, "pages", f"{page_name}.json")
        page = gl.page_manager.create_page(page_path, deck_controller)
        deck_controller.load_page(page)

        log.info("Tic-Tac-Toe game launched")

    def _create_game_page(self) -> dict:
        """Crée la structure de la page de jeu pour un deck 5x3."""
        page_dict = {"keys": {}}

        # Layout pour un Stream Deck 5x3 (15 touches):
        # [Back] [Cell0] [Cell1] [Cell2] [Score]
        # [New ] [Cell3] [Cell4] [Cell5] [     ]
        # [    ] [Cell6] [Cell7] [Cell8] [     ]

        # Bouton Retour (0,0)
        page_dict["keys"]["0x0"] = self._create_action_key(
            "com_pol_tictactoe::BackButton", {}
        )

        # Bouton Nouvelle Partie (0,1)
        page_dict["keys"]["0x1"] = self._create_action_key(
            "com_pol_tictactoe::NewGame", {}
        )

        # Score (4,0)
        page_dict["keys"]["4x0"] = self._create_action_key(
            "com_pol_tictactoe::ScoreDisplay", {"display_mode": "both"}
        )

        # Grille 3x3 (positions 1-3 sur colonnes, 0-2 sur lignes)
        cell_positions = [
            (1, 0), (2, 0), (3, 0),  # Ligne 0: cells 0, 1, 2
            (1, 1), (2, 1), (3, 1),  # Ligne 1: cells 3, 4, 5
            (1, 2), (2, 2), (3, 2),  # Ligne 2: cells 6, 7, 8
        ]

        for cell_index, (col, row) in enumerate(cell_positions):
            page_dict["keys"][f"{col}x{row}"] = self._create_action_key(
                "com_pol_tictactoe::CellButton", {"cell_index": cell_index}
            )

        return page_dict

    def _create_action_key(self, action_id: str, settings: dict) -> dict:
        """Crée une structure de touche avec une action."""
        return {
            "states": {
                "0": {
                    "actions": [{
                        "id": action_id,
                        "settings": settings
                    }],
                    "image-control-action": 0,
                    "label-control-actions": [0, 0, 0],
                    "background-control-action": 0,
                }
            }
        }
