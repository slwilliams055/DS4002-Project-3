
# Import libraries
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import time

# Set file paths
DATA_PATH = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")

INPUT_FILE = DATA_PATH / "BFree_viral_images.csv"
OUTPUT_FOLDER = DATA_PATH / "BFree_Images"

# Load dataset
df = pd.read_csv(INPUT_FILE)

# Create output folder if it doesn't exist
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize download counts
counts = {"REAL": 0, "FAKE": 0}
failed = 0

# Set up session for downloading images
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# Loop through each image in the dataset
for i, row in df.iterrows():
    label = str(row["label"]).upper()

    # Skip images without valid labels
    if label not in ["REAL", "FAKE"]:
        continue

    # label stays in the filename so you can still tell them apart
    save_path = OUTPUT_FOLDER / {label}_image_{i:05d}.jpg"

    try:
        # Download and save image if not already saved
        if not save_path.exists():
            response = session.get(str(row["url"]), timeout=20)
            response.raise_for_status()

            with Image.open(BytesIO(response.content)) as img:
                img.convert("RGB").save(save_path, "JPEG", quality=90)

        # Update count for each label
        counts[label] += 1

    except Exception:
        # Track failed downloads
        failed += 1

    # Print progress every 50 images
    if (i + 1) % 50 == 0:
        print(Processed {i + 1} of {len(df)}")

    # Pause between requests
    time.sleep(0.2)

# Print download summary
print("REAL images:", counts["REAL"])
print("FAKE images:", counts["FAKE"])
print("Total saved:", sum(counts.values()))
print("Failed downloads:", failed)
print("Folder:", OUTPUT_FOLDER)
