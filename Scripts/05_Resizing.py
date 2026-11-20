# This script resizes all selected images to 224 × 224 pixels and checks their dimensions to ensure consistent image sizes.

# Import required libraries
from PIL import Image
from pathlib import Path
import pandas as pd

# Define data and image directories
OUT_IMAGES = Data / "BFree_Images_600"

# Resize every image (skips ones already 224x224)
for path in OUT_IMAGES.glob("*.jpg"):
    with Image.open(path) as img:
        if img.size == (224, 224):
            continue
        img = img.convert("RGB").resize((224, 224), Image.LANCZOS)
    img.save(path, "JPEG", quality=90)

# Print every image in the folder with its size
files = sorted(OUT_IMAGES.glob("*.jpg"))
bad = 0

# Check image dimensions and count incorrectly sized images
for p in files:
    with Image.open(p) as img:
        w, h = img.size
    print(f"{p.name}: {w} x {h}")
    if (w, h) != (224, 224):
        bad += 1

# Load final dataset metadata
df = pd.read_csv(DATA_PATH / "BFree_viral_images_600.csv")
