# modules/manifest_dashboard.py

# Wenn du die textual-Bibliothek nutzt, stelle sicher, dass sie installiert ist:
# pip install textual
# Auskommentiert, um Pylance-Fehler zu vermeiden:
# from textual.app import App, ComposeResult
# from textual.widgets import Tree, Header, Footer, Button, Static
# from textual.containers import Horizontal, Vertical
# from textual.message import Message

from typing import Any, Dict, List
import yaml
import os

CONFIG_DIR = "configs"


class ManifestDashboard:
    """
    Minimaler Dashboard-Loader, der YAML-Konfigs aus configs/ lädt
    und per simple CLI anzeigt.
    """

    def __init__(self, config_dir: str = CONFIG_DIR) -> None:
        self.config_dir = config_dir
        self.manifests: Dict[str, Any] = {}

    def load_manifests(self) -> None:
        """Lädt alle .yaml-Dateien aus dem Config-Ordner."""
        for fname in os.listdir(self.config_dir):
            if not fname.endswith((".yaml", ".yml")):
                continue
            path = os.path.join(self.config_dir, fname)
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            self.manifests[fname] = data

    def list_manifests(self) -> List[str]:
        """Gibt die Liste aller geladenen Manifeste zurück."""
        return list(self.manifests.keys())

    def show_manifest(self, name: str) -> None:
        """Druckt den Inhalt eines einzelnen Manifests in die Konsole."""
        manifest = self.manifests.get(name)
        if manifest is None:
            print(f"[!] Manifest '{name}' nicht gefunden.")
            return
        print(f"\n=== {name} ===")
        print(yaml.dump(manifest, sort_keys=False))

    def run(self) -> None:
        """Einfache CLI-Schleife, um Manifeste zu inspizieren."""
        self.load_manifests()
        print("⚙️  Manifest Dashboard geladen.")
        while True:
            print("\nVerfügbare Manifeste:")
            for idx, name in enumerate(self.list_manifests(), start=1):
                print(f"  [{idx}] {name}")
            print("  [q] Beenden")
            choice = input("Auswahl: ").strip().lower()
            if choice in ("q", "quit", "exit"):
                break
            try:
                idx = int(choice) - 1
                name = self.list_manifests()[idx]
                self.show_manifest(name)
            except (ValueError, IndexError):
                print("[!] Ungültige Auswahl.")
        print("👋 Dashboard beendet.")


if __name__ == "__main__":
    dashboard = ManifestDashboard()
    dashboard.run()
