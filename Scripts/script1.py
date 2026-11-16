import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
import time

DATA_PATH = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")

INPUT_FILE = DATA_PATH / "BFree_viral_images.csv"
OUTPUT_FOLDER = DATA_PATH / "BFree_Images"

df = pd.read_csv(INPUT_FILE)

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

counts = {"REAL": 0, "FAKE": 0}
failed = 0

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

for i, row in df.iterrows():
    label = str(row["label"]).upper()

    if label not in ["REAL", "FAKE"]:
        continue

    # label stays in the filename so you can still tell them apart
    save_path = OUTPUT_FOLDER / {label}_image_{i:05d}.jpg"

    try:
        if not save_path.exists():
            response = session.get(str(row["url"]), timeout=20)
            response.raise_for_status()

            with Image.open(BytesIO(response.content)) as img:
                img.convert("RGB").save(save_path, "JPEG", quality=90)

        counts[label] += 1

    except Exception:
        failed += 1

    if (i + 1) % 50 == 0:
        print(Processed {i + 1} of {len(df)}")

    time.sleep(0.2)

print("REAL images:", counts["REAL"])
print("FAKE images:", counts["FAKE"])
print("Total saved:", sum(counts.values()))
print("Failed downloads:", failed)
print("Folder:", OUTPUT_FOLDER)
