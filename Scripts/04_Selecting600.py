# Import required libraries
import shutil
import pandas as pd
from pathlib import Path

# Define input and output directories
DATA_PATH = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")
IMAGES = DATA_PATH / "BFree_Images"
OUT_IMAGES = DATA_PATH / "BFree_Images_600"

# Set target dataset size
TOTAL = 600

# Load cleaned metadata
df = pd.read_csv(DATA_PATH / "step1_clean.csv")

# Label: REAL = 1, and FAKE = 0
df["label"] = df["label"].astype(str).str.upper().map({"REAL": 1, "FAKE": 0})
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

# Keep only rows whose image actually downloaded
df = df[df["filename"].apply(lambda f: (IMAGES / f).exists())]
print("Rows with an image on disk:", len(df))
print(df["label"].value_counts())
if len(df) == 0:
    raise SystemExit("No matching images found. Did step 3 run?")

# Separate images by label
real = df[df["label"] == 1]
fake = df[df["label"] == 0]

# Take up to 300 REAL, then fill the rest of the 600 with FAKE
n_real = min(len(real), TOTAL // 2)
n_fake = TOTAL - n_real

# Randomly sample and shuffle selected images
df = pd.concat([real.sample(n=n_real, random_state=42), fake.sample(n=n_fake, random_state=42),]).sample(frac=1, random_state=42).reset_index(drop=True)   # shuffle rows

# Copy the 600 images into one new folder
OUT_IMAGES.mkdir(exist_ok=True)
for f in df["filename"]:
    shutil.copy(IMAGES / f, OUT_IMAGES / f)

# Keep only the columns we need
df = df[["filename", "label", "source_id"]]
df.to_csv(DATA_PATH / "BFree_viral_images_600.csv", index=False)

# Display final dataset size and label distribution
print("Images copied:", len(df))
print(df["label"].value_counts())
