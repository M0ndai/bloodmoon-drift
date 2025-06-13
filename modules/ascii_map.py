# === scripts/ascii_map.py ===
from vitalum.core import get_state

ZONES = ["mirror", "support", "seer", "observer"]

def render_map():
    state = get_state()
    zones = state.get("zones", {})
    lines = ["Zonenstatus:"]
    for z in ZONES:
        status = zones.get(z, "locked")
        marker = "🟢" if status == "active" else ("🔒" if status == "locked" else "⚪")
        lines.append(f" {marker} {z.upper()}")
    return "\n".join(lines)

if __name__ == "__main__":
    print(render_map())
