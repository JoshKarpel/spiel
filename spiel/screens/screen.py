from typing import TYPE_CHECKING

from textual.screen import Screen

if TYPE_CHECKING:
    from spiel.app import SpielApp


class SpielScreen(Screen):
    app: "SpielApp"
