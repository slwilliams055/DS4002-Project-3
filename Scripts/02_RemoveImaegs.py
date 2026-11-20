# This script removes identified unwanted images from the dataset and deletes their corresponding rows from the metadata CSV.
# Import required libraries
import pandas as pd
from pathlib import Path

# Define data and image directories

IMAGES = Data / "BFree_Images"

# List images to remove
BAD_FILES = ["image_00229.jpg", "image_00297.jpg", "image_00369.jpg",
    "image_00516.jpg", "image_00541.jpg", "image_00601.jpg",
    "image_00606.jpg", "image_00691.jpg", "image_00710.jpg",
    "image_00896.jpg", "image_00901.jpg"]

# Delete the files that are unwanted
for name in BAD_FILES:
    for path in IMAGES.rglob(f"*{name}"):
        path.unlink()
        print("Deleted:", path)

# Remove the same rows from the CSV
df = pd.read_csv(DATA_PATH / "BFree_viral_images.csv")

# Generate filenames matching image indices
df["filename"] = [f"image_{i:05d}.jpg" for i in df.index]

# Filter out unwanted images
df = df[~df["filename"].isin(BAD_FILES)]

# Save cleaned metadata
df.to_csv(DATA_PATH / "step1_clean.csv", index=False)
print("Rows left:", len(df))
