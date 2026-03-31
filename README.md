# Invisible Cloak: Real-Time Background Compositing with OpenCV

> *"Make any coloured cloth disappear — like a Harry Potter invisibility cloak."*

---

## What This Project Does

This project uses your **webcam** and **pure OpenCV** to create a real-time "invisibility cloak" effect. When you hold up a solid-coloured piece of cloth (a towel, dupatta, blanket, or any fabric with a distinct colour) in front of the camera, the cloth becomes **transparent** — revealing the static background behind you, as if it never existed.

There are **no deep learning models**, no cloud APIs, and no special hardware needed. It runs entirely on your CPU using fundamental computer vision techniques:

- **HSV Colour Space Conversion** — for accurate, lighting-robust colour isolation
- **Binary Masking** — to locate exactly where the cloth is in the frame
- **Morphological Operations** — to clean up noisy mask edges
- **Bitwise Compositing** — to seamlessly blend background and foreground

An interactive **6-slider control panel** lets you tune the exact colour range of your cloth in real time, and a live **Mask Debug Window** shows you precisely what the algorithm is detecting.

---

## Demo Preview

```
[ Background Captured ]  +  [ Your Cloth Detected ]  =  [ Cloth Disappears! ]
    (stored frame)            (white mask region)         (final composite)
```

Three windows appear when running:
| Window | Description |
|---|---|
| `Invisible Cloak Magic` | The final composited output — your cloth is gone |
| `Mask (White = Disappearing Area)` | Debug view showing what the algorithm detects as "cloak" |
| `Colour Adjustments` | 6 sliders to tune Hue, Saturation, and Value ranges |

---

## Requirements

- Python **3.7 or higher**
- A working **webcam**
- A **solid-coloured cloth** (towels, scarves, blankets all work great)

### Python Dependencies

```
opencv-python
numpy
```

Both are lightweight and install in seconds.

---

## Setup & Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<MANAST11>/invisible-cloak.git
cd invisible-cloak
```

### Step 2 — Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
```

Activate it:

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

### Step 3 — Install Dependencies

```bash
pip install opencv-python numpy
```

---

## How to Run

```bash
python main.py
```

---

## Step-by-Step Usage Guide

### Step 1 — Background Capture
When the script starts, you will see a **3-second countdown** in the terminal.

>  **You must step completely out of the camera frame during this time.**

The program captures a clean image of the background (your room, wall, desk, etc.). This stored frame is what will be "revealed" through the cloak later.

---

### Step 2 — Step Back In With Your Cloth
After the countdown, walk back into the frame holding your coloured cloth.

---

### Step 3 — Tune the Colour Sliders
Open the **"Colour Adjustments"** window. You will see 6 sliders:

| Slider | What It Controls |
|---|---|
| `Hue Min` / `Hue Max` | The colour range (e.g., blue = 90–130, green = 40–80, red = 0–10 or 160–179) |
| `Sat Min` / `Sat Max` | How vivid/saturated the colour must be |
| `Val Min` / `Val Max` | How bright or dark the colour can be |

**Watch the `Mask` window** while adjusting. Your goal:
-  Cloth area → **solid white**
-  Everything else → **solid black**

Once the mask looks clean, the `Invisible Cloak Magic` window will show the cloak effect in real time.

---

### Step 4 — Exit

Press **`q`** on your keyboard while any video window is active to stop the program.

---

## Quick Colour Reference (Hue Values in HSV)

| Colour | Hue Min | Hue Max |
|---|---|---|
| Red (lower) | 0 | 10 |
| Red (upper) | 160 | 179 |
| Orange | 10 | 25 |
| Yellow | 25 | 35 |
| Green | 40 | 80 |
| Cyan | 80 | 95 |
| Blue | 90 | 130 |
| Purple/Violet | 130 | 160 |

>  **Tip:** Start by adjusting only the Hue sliders, then fine-tune Saturation to eliminate false detections from similarly-coloured objects in the room.

---

## Project Structure

```
invisible-cloak/
│
├── main.py                              # Core application
├── README.md                            # This file
└── invisible-cloak-report.docx          # Project Report file
```

---

## How It Works — Technical Deep Dive

```
                  ┌─────────────────────────────────────────────────┐
  Startup         │  Camera warms up → Background frame captured    │
                  └───────────────────────┬─────────────────────────┘
                                          │
                  ┌───────────────────────▼─────────────────────────┐
  Each Frame      │  Live frame → Convert BGR → HSV                 │
                  └───────────────────────┬─────────────────────────┘
                                          │
                  ┌───────────────────────▼─────────────────────────┐
  Masking         │  inRange(HSV, lower_bound, upper_bound)         │
                  │  → Binary mask: WHITE=cloak, BLACK=everything   │
                  └───────────────────────┬─────────────────────────┘
                                          │
                  ┌───────────────────────▼─────────────────────────┐
  Cleanup         │  morphologyEx OPEN  → removes noise specks      │
                  │  morphologyEx DILATE → fills mask gaps          │
                  └───────────────────────┬─────────────────────────┘
                                          │
                  ┌───────────────────────▼─────────────────────────┐
  Compositing     │  res1 = background AND mask   (cloak region)   │
                  │  res2 = live_frame AND ~mask  (rest of scene)  │
                  │  output = res1 + res2                           │
                  └─────────────────────────────────────────────────┘
```

**Why HSV instead of BGR/RGB?** BGR mixes colour and brightness in all three channels, making colour isolation sensitive to lighting changes. HSV separates **Hue** (the actual colour), **Saturation** (vividness), and **Value** (brightness) — letting us match a colour reliably even when the lighting in the room shifts.

---

## Known Limitations

- Works best in **stable, consistent lighting**. Avoid backlighting or rapidly changing light.
- The cloth colour should **not closely match anything else** in the room (e.g., don't use a blue cloth in front of a blue wall).
- The **background must remain completely static** after capture — any movement (fan-blown curtains, shifting sunlight) will cause artifacts.
- Performance depends on your CPU; most modern laptops run this at 20–30 FPS smoothly.

---

## Possible Extensions

- [ ] Add support for **two simultaneous colour ranges** (e.g., two-sided red cloth)
- [ ] Save HSV presets to a JSON config file for fast reloading
- [ ] Record the output to a video file with `cv2.VideoWriter`
- [ ] Add an **edge-smoothing / feathering** pass for softer cloak boundaries
- [ ] Port to a **mobile camera** using IP Webcam + network stream

---

## License

This project is released under the **MIT License** — free to use, modify, and share.

---

