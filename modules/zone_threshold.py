# modules/zone_threshold.py

from typing import TYPE_CHECKING, Any, Dict, Tuple
import matplotlib.pyplot as plt

if TYPE_CHECKING:
    # Damit Pylance weiß, was Circle und colormaps sind:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    import matplotlib.cm as cm
else:
    # Laufzeit-Stubs
    class cm:  # type: ignore
        """Stub-Modul für colormaps"""
        @staticmethod
        def get_cmap(name: str) -> Any:
            return plt.cm.get_cmap(name)

def evaluate_heat_zones(
    heatmap: Dict[Tuple[int, int], float],
    thresholds: Dict[str, float],
) -> Dict[str, int]:
    """
    Zählt für jede Zone (key in thresholds) die Zellen im heatmap-Grid,
    deren Wert >= threshold.
    """
    zone_hits: Dict[str, int] = {zone: 0 for zone in thresholds}
    for coord, val in heatmap.items():
        for zone, thresh in thresholds.items():
            if val >= thresh:
                zone_hits[zone] += 1
                break
    return zone_hits

def plot_zone_thresholds(
    heatmap: Dict[Tuple[int, int], float],
    thresholds: Dict[str, float],
) -> None:
    """
    Visualisiert das heatmap-Grid und markiert Zone-Schwellen
    als Kreise um koordinaten, die bestimmte Intensitäten überschreiten.
    """
    from matplotlib.patches import Circle
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()

    # Plot Heatmap-Punkte
    xs, ys, intensities = zip(*[(x, y, v) for (x, y), v in heatmap.items()])
    scatter = ax.scatter(xs, ys, c=intensities, cmap=cm.get_cmap("viridis"), s=50)
    plt.colorbar(scatter, ax=ax)

    # Threshold-Circles
    for (x, y), intensity in heatmap.items():
        if intensity >= min(thresholds.values()):
            circle = Circle((x, y), radius=0.4, fill=False, linewidth=1.5)
            ax.add_patch(circle)

    ax.set_xlabel("X-Koordinate")
    ax.set_ylabel("Y-Koordinate")
    ax.set_title("Zone Threshold Visualisierung")
    ax.grid(True)
    plt.show()