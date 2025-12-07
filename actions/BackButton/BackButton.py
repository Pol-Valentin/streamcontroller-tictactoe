from src.backend.PluginManager.ActionBase import ActionBase
from loguru import logger as log

import os


class BackButton(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "back.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.set_label("Retour", position="bottom")
        self.set_background_color([60, 60, 80, 255])

    def on_key_down(self) -> None:
        deck_controller = self.deck_controller
        if deck_controller is None:
            log.warning("No deck controller available")
            return

        back_page = self.plugin_base.back_page
        log.info(f"Back button pressed, back_page: {back_page}")

        if back_page is not None:
            deck_controller.load_page(back_page)
            log.info("Navigated back to previous page")
        else:
            log.warning("No back page stored")
