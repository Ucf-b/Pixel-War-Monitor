import re
import time

import numpy as np
import requests
import winsound  # Windows only – remove/replace on Linux/macOS

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
BASE_URL = "https://your-pixel-server.com/"

# Rectangular zone to monitor on the canvas (pixels)
# (x_start, y_start, width, height) – top-left origin
MONITOR_ZONE = (350, 134, 49, 31)

POLL_INTERVAL = 10  # seconds between each snapshot

DISCORD_WEBHOOK = (
    "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
)


# ──────────────────────────────────────────────
# Palette / color utilities
# ──────────────────────────────────────────────
def parse_palette(raw_palette: list) -> list[tuple]:
    """
    Convert a list of hex color strings (or dicts with a 'value' key) into
    RGBA tuples in the same byte order used by the board data.
    """
    result = []
    for entry in raw_palette:
        if isinstance(entry, dict) and "value" in entry:
            entry = entry["value"]

        match = re.fullmatch(r"#?([\da-fA-F]{2})([\da-fA-F]{2})([\da-fA-F]{2})", entry)
        if not match:
            raise ValueError(f"Invalid color format: {entry!r}")

        r, g, b = (int(match.group(i), 16) for i in (1, 2, 3))
        # Board stores colors as ARGB; convert to RGBA for NumPy
        argb = 0xFF000000 | (b << 16) | (g << 8) | r
        rgba = (
            (argb >> 24) & 0xFF,
            (argb >> 16) & 0xFF,
            (argb >> 8) & 0xFF,
            argb & 0xFF,
        )
        result.append(rgba)

    return result


# ──────────────────────────────────────────────
# Snapshot helpers  (inspired by haykam821/Pxls-Snapshot-Stream)
# ──────────────────────────────────────────────
def capture_snapshot(base_url: str = BASE_URL) -> np.ndarray:
    """
    Fetch the full canvas from *base_url* and return it as an RGBA NumPy array
    of shape (height, width, 4).
    """
    info = requests.get(f"{base_url}info").json()
    width, height = info["width"], info["height"]
    palette = parse_palette(info["palette"])

    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    raw = np.frombuffer(requests.get(f"{base_url}boarddata").content, dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            color_index = raw[y * width + x]
            if color_index != 0xFF:          # 0xFF = transparent / unset pixel
                canvas[y, x] = palette[color_index]

    return canvas


def extract_zone(canvas: np.ndarray, zone: tuple) -> np.ndarray:
    """Slice *canvas* to the rectangle defined by *zone* (x, y, w, h)."""
    x, y, w, h = zone
    return canvas[y:y + h, x:x + w]


def zone_has_changed(old: np.ndarray, new: np.ndarray, zone: tuple) -> bool:
    """Return True if the monitored *zone* differs between *old* and *new* canvases."""
    return not np.array_equal(extract_zone(old, zone), extract_zone(new, zone))


# ──────────────────────────────────────────────
# Alert helpers
# ──────────────────────────────────────────────
def play_beep(frequency: int = 1000, duration_ms: int = 1000) -> None:
    """Emit a system beep (Windows only)."""
    winsound.Beep(frequency, duration_ms)


def notify_discord(message: str, webhook_url: str = DISCORD_WEBHOOK) -> None:
    """Send *message* to a Discord channel via webhook."""
    requests.post(webhook_url, json={"content": message})


# ──────────────────────────────────────────────
# Main monitoring loop
# ──────────────────────────────────────────────
def monitor(zone: tuple = MONITOR_ZONE, interval: int = POLL_INTERVAL) -> None:
    """
    Poll the canvas every *interval* seconds and trigger alerts whenever a
    change is detected inside *zone*.
    """
    print(f"Monitoring zone {zone} on {BASE_URL} — polling every {interval}s")
    previous = None

    while True:
        current = capture_snapshot()

        if previous is not None:
            if zone_has_changed(previous, current, zone):
                print("[ALERT] Change detected in the monitored zone!")
                play_beep()
                notify_discord(
                    "@everyone A change has been detected in the Picsel Moroccan flag — defend your nation! 🇲🇦"
                )
            else:
                print("[OK] No change detected.")

        previous = current
        time.sleep(interval)


if __name__ == "__main__":
    monitor()
