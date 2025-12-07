from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.InputIdentifier import Input
from loguru import logger as log

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw


class ScoreDisplay(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event_callback(self, event, data=None):
        super().event_callback(event, data)
        if event == Input.Key.Events.HOLD_START:
            self.on_key_hold_start()

    def on_ready(self) -> None:
        self.plugin_base.register_score_action(self)
        self.update_display()

    def get_display_mode(self) -> str:
        """Get display mode: 'both', 'x', or 'o'."""
        settings = self.get_settings()
        return settings.get("display_mode", "both")

    def update_display(self) -> None:
        """Update the score display."""
        mode = self.get_display_mode()
        score_x = self.plugin_base.score_x
        score_o = self.plugin_base.score_o
        current_player = self.plugin_base.current_player
        game_over = self.plugin_base.game_over
        winner = self.plugin_base.winner

        if game_over:
            if winner:
                label = f"{winner} gagne!"
                if winner == "X":
                    self.set_background_color([150, 50, 50, 255])  # Red
                else:
                    self.set_background_color([50, 50, 150, 255])  # Blue
            else:
                label = "Match nul!"
                self.set_background_color([100, 100, 50, 255])  # Yellow
        else:
            if mode == "both":
                label = f"X:{score_x} O:{score_o}"
                self.set_background_color([50, 50, 50, 255])
            elif mode == "x":
                label = f"X: {score_x}"
                self.set_background_color([100, 40, 40, 255])
            else:
                label = f"O: {score_o}"
                self.set_background_color([40, 40, 100, 255])

        self.set_center_label(label, font_size=18)

        # Show current player indicator
        if not game_over:
            turn_label = f"Tour: {current_player}"
            self.set_label(turn_label, position="bottom")

    def on_key_down(self) -> None:
        self.update_display()

    def on_key_hold_start(self) -> None:
        self.plugin_base.reset_scores()
        self.plugin_base.reset_game()

    def get_config_rows(self) -> list:
        self.mode_row = Adw.ComboRow()
        self.mode_row.set_title("Mode d'affichage")

        model = Adw.EnumListModel.new(type(None))
        string_list = ["Les deux scores", "Score X seulement", "Score O seulement"]

        # Create a StringList for the combo
        self.mode_row.set_model(
            type(self.mode_row).get_model.__get__(self.mode_row, type(self.mode_row))
        ) if False else None

        # Simple approach: use factory
        from gi.repository import Gtk
        string_model = Gtk.StringList.new(string_list)
        self.mode_row.set_model(string_model)

        mode = self.get_display_mode()
        mode_map = {"both": 0, "x": 1, "o": 2}
        self.mode_row.set_selected(mode_map.get(mode, 0))
        self.mode_row.connect("notify::selected", self.on_mode_changed)

        return [self.mode_row]

    def on_mode_changed(self, combo_row, *args):
        settings = self.get_settings()
        mode_map = {0: "both", 1: "x", 2: "o"}
        settings["display_mode"] = mode_map.get(combo_row.get_selected(), "both")
        self.set_settings(settings)
        self.update_display()
