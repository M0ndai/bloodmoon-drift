#!/usr/bin/env python3
import yaml
import os

MODULES_DIR = "./modules"
MANIFEST_PATH = "drift_deployment_manifest.yaml"

def load_base_manifest():
    return {
        "version": "vexor-bloodmoon-1.0",
        "description": "Automatisch generiertes Manifest für BlutMond Drift-Ökosystem.",
        "modules": {},
        "optional": {
            "plugin_loader": {
                "enabled": True,
                "description": "Lädt zur Laufzeit externe Drift-Plugins.",
                "source": "./modules/plugin_loader.py"
            },
            "symbolic_registry": {
                "enabled": True,
                "description": "Zentrales Verzeichnis aller Symbol-Metadaten.",
                "source": "./modules/symbolic_registry.py"
            },
            "ritual_logbook": {
                "enabled": True,
                "description": "Archiviert alle Drift-Mutationen als YAML-Log.",
                "source": "./modules/ritual_logbook.py"
            }
        },
        "entrypoint": {
            "main": "main.py",
            "description": "Startet das Drift- und Ritualnetz."
        },
        "env": {
            "BLOODMOON_MODE": "chaotic",
            "DRIFT_LEVEL": "auto",
            "XAI_LOGGING": "on",
            "DEBUG_UI": True
        },
        "ci_cd": {
            "pipeline": ".github/workflows/drift_deploy.yml"
        }
    }

def discover_modules(manifest):
    for fname in os.listdir(MODULES_DIR):
        if fname.endswith(".py") and fname not in ["plugin_loader.py", "symbolic_registry.py", "ritual_logbook.py"]:
            name = fname[:-3]
            manifest["modules"][name] = {
                "enabled": True,
                "description": f"Auto-loaded: {name}",
                "source": f"{MODULES_DIR}/{fname}"
            }

def write_manifest(manifest):
    with open(MANIFEST_PATH, "w") as f:
        yaml.dump(manifest, f, sort_keys=False)
    print(f"✔ Generated {MANIFEST_PATH}")

if __name__ == "__main__":
    manifest = load_base_manifest()
    discover_modules(manifest)
    write_manifest(manifest)
