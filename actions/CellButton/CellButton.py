from src.backend.PluginManager.ActionBase import ActionBase
from loguru import logger as log

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw

import os


class CellButton(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        self.plugin_base.register_cell_action(self)
        self.update_display()

    def get_cell_index(self) -> int:
        """Get the cell index from settings (0-8)."""
        settings = self.get_settings()
        return settings.get("cell_index", 0)

    def update_display(self) -> None:
        """Update the cell display based on game state."""
        cell_index = self.get_cell_index()
        board = self.plugin_base.board
        cell_value = board[cell_index] if cell_index < len(board) else ""

        assets_path = os.path.join(self.plugin_base.PATH, "assets")

        if cell_value == "X":
            icon_path = os.path.join(assets_path, "x.png")
        elif cell_value == "O":
            icon_path = os.path.join(assets_path, "o.png")
        else:
            icon_path = os.path.join(assets_path, "empty.png")

        self.set_background_color([50, 50, 50, 255])  # Fond gris pour toutes les cases

        self.set_media(media_path=icon_path, size=0.9)

        # Show winner highlight
        if self.plugin_base.game_over and self.plugin_base.winner:
            if cell_value == self.plugin_base.winner:
                self.set_background_color([100, 200, 100, 255])  # Vert clair pour gagnant

    def on_key_down(self) -> None:
        cell_index = self.get_cell_index()
        self.plugin_base.play_cell(cell_index)

    def get_config_rows(self) -> list:
        self.cell_index_row = Adw.SpinRow.new_with_range(0, 8, 1)
        self.cell_index_row.set_title("Index de la case")
        self.cell_index_row.set_subtitle("0-8, de gauche à droite, de haut en bas")
        self.cell_index_row.set_value(self.get_cell_index())
        self.cell_index_row.connect("changed", self.on_cell_index_changed)

        return [self.cell_index_row]

    def on_cell_index_changed(self, spin_row):
        settings = self.get_settings()
        settings["cell_index"] = int(spin_row.get_value())
        self.set_settings(settings)
        self.update_display()
