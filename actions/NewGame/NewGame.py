from src.backend.PluginManager.ActionBase import ActionBase
from loguru import logger as log

import os
import time


class NewGame(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_press_time = 0

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "newgame.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.set_label("Rejouer", position="bottom")
        self.set_background_color([40, 80, 40, 255])

    def on_key_down(self) -> None:
        self.last_press_time = time.time()

    def on_key_up(self) -> None:
        press_duration = time.time() - self.last_press_time

        if press_duration >= 1.5:
            # Long press: reset scores too
            self.plugin_base.reset_scores()
            self.plugin_base.reset_game()
            log.info("Game and scores reset (long press)")
        else:
            # Short press: just reset game
            self.plugin_base.reset_game()
            log.info("Game reset (short press)")
