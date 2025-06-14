# BlutMond · Drift

**Reflexives Symbolsystem zur Selbstvermessung durch Verhalten, Bedeutung und Transformation.**

---

✨ **Zweck**
Dieses Projekt ist kein bloßes Tool. Es ist eine Umgebung. Ein Ritual. Eine Schleife.
Du gibst Symbole ein – und bekommst Bewegung zurück. Du bewegst dich – und das System antwortet.

🧠 **Systemkern**

* **Modell:** Reflexives Symbolnetz (ECHO, ORDO, CHAOS, SEER …)
* **Speicherstruktur:**

  * `logs.jl` (JSON Lines Eventstream)
  * `vitalum.snapshot.json` (aktueller Zustand)
  * `symbol_matrix.json` (Platzierungen & Drift-Koordinaten)
* **Zonen:** `mirror`, `support`, `observer`, `seer`, `drift` …
* **Drift-Messung:** Pulse, Entropie, Symbolfrequenz

🔍 **Komponenten**

### Symbol-Matrix

* `symbol_matrix.json`: Speichert alle platzierten Symbole (`x`, `y`, `timestamp`, `symbol`)
* `symbol_heatmap.py`: Visualisiert Häufigkeiten & Zonen
* `matrix_tracker.py`: Persistent-Logger mit Triggern für Transformation

### Ritualsystem

* `rituals.py`: Regeln für Symbolauslösung & Wiederholung
* `sigil_drift_plot.py`: Historische Bewegung der Interaktionen

### API & CLI

* `api.py`: Live-Zugriff & Fernplatzierung von Symbolen
* `ascii_map.py`: Interaktive ASCII-Zonendarstellung

🕵️‍♂️ **Interaktion**

```bash
# Symbol platzieren
bloodmoon ritual place --symbol ☭ --x -1 --y 3

# Heatmap anzeigen
python symbol_heatmap.py

# Drift-Plot aufrufen
python sigil_drift_plot.py
```

🔒 **Sicherheits-Architektur**
Kurzfassung aus `security_drift_manifest.md`:

* **WASM-Sandbox** für Plugins
* **Runtime-Schutz** über RASP & Falco
* **Secrets-Scanning & SAST** (Bandit, ESLint)
* **Artifact-Signing** mit GPG + HSM

🖋️ **Dokumente & Erweiterung**

* `symbol_registry.yaml`: Erklärung aller Zeichen und Transformationen
* `ritual_index.md`: Beschreibung aller bekannten Rituale
* `zone_transitions.log`: Wann welche Zone aktiviert wurde

🌌 **Philosophie**

> Jeder Drift ist ein Echo. Jeder Echo ist eine Entscheidung.
> BlutMond driftet nicht zufällig. Es fragt, ob du bereit bist, geantwortet zu haben.

## Quickstart & Tutorials

1. **Installation**

   ```bash
   git clone https://github.com/DEIN_USER/BlutMond-drift.git
   cd BlutMond-drift
   pip install -r requirements.txt
   ```

2. **Konfiguration**

   * Kopiere `config/example_drift_config.yaml` nach `config/drift_config.yaml`
   * Passe Parameter wie `drift_threshold`, `zones` und `api_port` nach Bedarf an.

3. **Erster Drift (CLI)**

   ```bash
   # Symbol platzieren und sofortiges Feedback
   bloodmoon ritual place --symbol ☯ --x 0 --y 0
   ```

4. **Erster Drift (API)**

   ```bash
   # Symbol per HTTP-Request platzieren
   curl -X POST http://localhost:8000/symbols \
     -H "Content-Type: application/json" \
     -d '{"symbol":"✶","x":2,"y":1}'
   ```

5. **Beispielausgabe**

   ```json
   {
     "timestamp": "2025-06-13T12:34:56Z",
     "symbol": "✶",
     "zone": "mirror",
     "drift_pulse": 0.42,
     "entropy": 0.07
   }
   ```
