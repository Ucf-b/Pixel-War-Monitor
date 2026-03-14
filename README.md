# 🖼️ Pixel Watcher

A Python toolkit for a pixel-war like canvas.
It lets you **pixelize an image** to match the canvas palette and **monitor a zone** for unauthorized edits — with Discord alerts and a beep sound when a change is detected.

> Inspired by [haykam821/Pxls-Snapshot-Stream](https://github.com/haykam821/Pxls-Snapshot-Stream) — the original snapshot-streaming logic was adapted from JavaScript to Python and extended with zone monitoring and Discord notifications.

---

## Features

| Script | Description |
|---|---|
| `pixelizer.py` | Converts any image to a low-resolution, palette-quantized version that matches Picsel's color palette |
| `watcher.py` | Polls the live canvas and sends a Discord `@everyone` ping (+ a beep) when your zone is modified |

---

## Requirements

- Python 3.10+
- Windows (for the `winsound` beep in `watcher.py`; easily removable on Linux/macOS)

Install dependencies:

```bash
pip install pillow numpy requests
```

---

## Quick Start

### 1 · Pixelize an image

```bash
python pixelizer.py
```

Edit the constants at the top of the file to set your input image path, output path, and desired pixel grid size:

```python
INPUT_PATH  = "images/example_image.png"
OUTPUT_PATH = "pixelized_example.png"
PIXEL_SIZE  = (64, 64)
```

### 2 · Monitor a canvas zone

1. Open `watcher.py` and configure the two constants:

```python
# Top-left corner and dimensions of the zone to protect (in canvas pixels)
MONITOR_ZONE = (350, 134, 49, 31)   # (x, y, width, height)

# Your Discord channel webhook URL
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"
```

2. Run the watcher:

```bash
python watcher.py
```

Every 10 seconds the script fetches a fresh snapshot and compares the monitored zone to the previous one. If anything changed you will hear a beep and your Discord channel will receive an `@everyone` alert.

---

## Configuration Reference

### `pixelizer.py`

| Constant | Default | Description |
|---|---|---|
| `INPUT_PATH` | `"images/…"` | Source image to pixelize |
| `OUTPUT_PATH` | `"pixelized_example.png"` | Where to save the result |
| `PIXEL_SIZE` | `(64, 64)` | Downscale resolution before quantization |
| `PALETTE` | *(35 colors)* | Color palette matching the Picsel canvas |

### `watcher.py`

| Constant | Default | Description |
|---|---|---|
| `BASE_URL` | `"https://your-pixel-server.com/"` | Canvas API base URL |
| `MONITOR_ZONE` | `(350, 134, 49, 31)` | Zone to watch `(x, y, w, h)` |
| `POLL_INTERVAL` | `10` | Seconds between snapshots |
| `DISCORD_WEBHOOK` | *(placeholder)* | Discord incoming webhook URL |

---

## Project Structure

```
picsel-watcher/
├── images/
│   └── example_image.png   # Example source image
├── pixelizer.py                       # Image → palette-quantized pixel art
├── watcher.py                         # Canvas zone monitor + Discord alerts
└── README.md
```

---

## Notes

- `winsound` is a Windows-only standard-library module. To run `watcher.py` on Linux or macOS, simply remove the `play_beep()` call and the `import winsound` line.
- The Discord webhook URL in the repository must be kept secret — consider storing it in an environment variable or a `.env` file (and adding `.env` to `.gitignore`).

---

## Credits

- Canvas snapshot approach adapted from [haykam821/Pxls-Snapshot-Stream](https://github.com/haykam821/Pxls-Snapshot-Stream)
- Built for the Picsel pixel war at [cs-campus.fr](https://picsel.cs-campus.fr/)
