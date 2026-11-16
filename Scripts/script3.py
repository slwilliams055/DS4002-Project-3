import pandas as pd
from pathlib import Path

DATA_PATH = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")
IMAGES = DATA_PATH / "BFree_Images"

renamed = 0
skipped = 0

# Strip REAL_/FAKE_ prefix and move everything into the main folder
for path in list(IMAGES.rglob("*.jpg")):
    name = path.name
    for prefix in ("REAL_", "FAKE_"):
        if name.startswith(prefix):
            name = name[len(prefix):]
    new_path = IMAGES / name

    if path == new_path:
        continue
    if new_path.exists():
        skipped += 1          # a file with the clean name already exists, leave this one
        print("Skipped (already exists):", path.name)
        continue

    path.rename(new_path)
    renamed += 1

# Remove empty REAL/FAKE subfolders if they exist
for sub in ("REAL", "FAKE"):
    folder = IMAGES / sub
    if folder.exists() and not any(folder.iterdir()):
        folder.rmdir()

print("Renamed:", renamed)
print("Skipped:", skipped)

# Check: does the folder line up with the CSV?
files = {p.name for p in IMAGES.glob("*.jpg")}
print("Images in folder:", len(files))
print("Still prefixed:", sum(f.startswith(("REAL_", "FAKE_")) for f in files))

df = pd.read_csv(DATA_PATH / "step1_clean.csv")
df["label"] = df["label"].astype(str).str.upper().map({"REAL": 1, "FAKE": 0})
matched = df[df["filename"].isin(files)]
print("CSV rows that match an image:", len(matched))
print(matched["label"].value_counts())
