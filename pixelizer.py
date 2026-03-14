from PIL import Image
import numpy as np

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
INPUT_PATH  = "images/example_image.png"  # Path to the input image
OUTPUT_PATH = "pixelized_example.png"
PIXEL_SIZE  = (64, 64)   # Resolution for the pixelized version

# Color palette used on the Picsel canvas
PALETTE = [
    (0, 0, 0),       (1, 191, 165),   (3, 52, 191),    (5, 69, 35),
    (20, 156, 255),  (22, 119, 126),  (24, 134, 47),   (31, 30, 38),
    (36, 35, 103),   (56, 34, 21),    (66, 70, 81),    (83, 29, 140),
    (85, 0, 34),     (97, 224, 33),   (119, 127, 140), (124, 63, 32),
    (141, 245, 255), (153, 1, 26),    (166, 48, 210),  (177, 255, 55),
    (185, 195, 207), (192, 111, 55),  (233, 115, 255), (241, 79, 180),
    (243, 15, 12),   (243, 243, 243), (246, 110, 8),   (253, 225, 17),
    (254, 173, 108), (255, 120, 114), (255, 159, 23),  (255, 164, 208),
    (255, 210, 177), (255, 255, 165), (255, 255, 255),
]


# ──────────────────────────────────────────────
# Core helpers
# ──────────────────────────────────────────────
def closest_palette_color(color: tuple, palette: list) -> tuple:
    """Return the palette color closest to *color* (Euclidean distance in RGB space)."""
    diffs = np.sum((np.array(palette) - np.array(color)) ** 2, axis=1)
    return palette[np.argmin(diffs)]


def pixelize(image: Image.Image, pixel_size: tuple, palette: list) -> Image.Image:
    """
    Resize *image* to *pixel_size*, map every pixel to the nearest palette color,
    then scale back to the original dimensions so individual pixels are visible.
    """
    # Downscale
    small = image.resize(pixel_size, Image.NEAREST)
    pixels = np.array(small)

    # Quantize to palette
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            pixels[i, j] = closest_palette_color(tuple(pixels[i, j]), palette)

    # Upscale back to original size for display
    quantized = Image.fromarray(pixels.astype("uint8"), "RGB")
    return quantized.resize(image.size, Image.NEAREST)


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    image = Image.open(INPUT_PATH).convert("RGB")
    result = pixelize(image, PIXEL_SIZE, PALETTE)
    result.save(OUTPUT_PATH)
    result.show()
    print(f"Saved pixelized image to {OUTPUT_PATH}")
