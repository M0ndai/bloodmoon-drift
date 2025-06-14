# Ritual Guide: Sigil Drift

Dieses Dokument beschreibt das Ritualfeld für die **Sigil Drift**-Funktionalität, ihre Anwendung und Integration in deine Projektarbeit.

---

## 1. Überblick

**Sigil Drift** ist das semantische Agentensystem, das dein Verhalten beobachtet, reflektiert und performativ mit symbolischen Karten antwortet. Es verbindet:

* **Symbolmatrix** (coordinate-based glyph map)
* **Heatmap & Zonen** (Emergenz, Nachhall, Neutralität)
* **Chronos-Ritus** (Fokus-Timer, Delegation)

## 2. Anwendungsfälle

1. **Tägliche Reflexion**: Rufe `bloodmoon map` auf und lege 25 Minuten Fokuszeit fest. Beobachte Schwellenübergänge in deiner Matrix.
2. **Ritualentwicklung**: Erstelle mit `bloodmoon synth` ein neues Sigil für deinen aktuellen Gedankengang.
3. **Team-Review**: Visualisiert Heat-Layer und Schwellen in Meetings für gemeinsame Interpretation.

## 3. Schritt-für-Schritt Ritual

1. **Initialisierung**

   ```bash
   poetry run bloodmoon map
   ```
2. **Fokus-Timer setzen**
   ⏳ Automatisch gestartet
3. **Heat & Zonen studieren**
   Beobachte, welche Zellen in den Zonen „rift\_core“, „echo\_static“, „neutral\_zone“ aktiviert sind.
4. **Sigil-Erzeugung**

   ```bash
   poetry run bloodmoon synth --name "mood_shift"
   ```
5. **Dokumentation**
   Speichere Heatmap-Screenshot und Sigil in `docs/rituals/sigil_drift.md` oder in dein Echo-Journal.

## 4. Release Workflow

Um das Framework automatisch zu veröffentlichen, nutze folgenden GitHub Actions-Workflow:

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install --no-dev
      - name: Run Tests
        run: pytest --maxfail=1 --disable-warnings -q
      - name: Build Package
        run: poetry build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
      - name: Create GitHub Release
        uses: ncipollo/release-action@v1
        with:
          tag: ${{ github.ref }}
          name: Release ${{ github.ref }}
          body: |
            ## Changelog
            - Integration Manifest-Dashboard
            - Zone-Threshold-Pipeline
            - CI & Tests
```

---

Nutze diesen Guide, um deine Sigil-Drift-Rituale zu standardisieren und Releases automatisiert auszuliefern. Viel Erfolg!
