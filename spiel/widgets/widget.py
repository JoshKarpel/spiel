from __future__ import annotations

from typing import TYPE_CHECKING

from textual.widget import Widget

if TYPE_CHECKING:
    from spiel.app import SpielApp


class SpielWidget(Widget):
    app: "SpielApp"
