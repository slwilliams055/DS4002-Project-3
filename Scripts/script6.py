import pandas as pd
from pathlib import Path

DATA_PATH = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")
CSV = DATA_PATH / "BFree_viral_images_600.csv"

df = pd.read_csv(CSV)

df = df.drop(columns=["date", "days_since_1st_post", "w", "h", "md5", "url"], errors="ignore")

df.to_csv(CSV, index=False)
