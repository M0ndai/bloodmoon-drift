# modules/sigil_overlay.py

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from textual.widgets import Static
    from rich.panel import Panel
else:
    class Static:  # type: ignore
        """Stub-Klasse für textual.widgets.Static"""
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass
        def update(self, renderable: Any) -> None:
            pass

    class Panel:  # type: ignore
        """Stub-Klasse für rich.panel.Panel"""
        def __init__(self, content: Any, title: str = "", border_style: str = "") -> None:
            self.content = content
            self.title = title
            self.border_style = border_style

class SigilOverlay(Static):
    """
    Visualisiert aktuelle aktive Zone(n) als Sigil-Symbol(e).
    """

    def __init__(self, id: str = "") -> None:
        super().__init__()
        self.id = id

    def update_sigils(self, active_zones: List[str]) -> None:
        SIGIL_STATE: dict[str, str] = {
            "rift_core": "⛧",
            "echo_static": "☍",
            "neutral_zone": "ὰf",
        }
        symbols: List[str] = [SIGIL_STATE.get(zone, "?") for zone in active_zones]
        sigil_line: str = " ".join(symbols)

        panel = Panel(sigil_line, title="Aktive Zonen", border_style="bold magenta")
        self.update(panel)
