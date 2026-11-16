import pandas as pd
from pathlib import Path

DATA_PATH = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")
IMAGES = DATA_PATH / "BFree_Images"

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
df["filename"] = [f"image_{i:05d}.jpg" for i in df.index]
df = df[~df["filename"].isin(BAD_FILES)]
df.to_csv(DATA_PATH / "step1_clean.csv", index=False)
print("Rows left:", len(df))
