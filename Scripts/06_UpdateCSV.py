# This script removes unnecessary columns from the final dataset CSV, retaining only the metadata needed for subsequent analysis.

# Import required libraries
import pandas as pd
from pathlib import Path

# Define data directory and CSV file
CSV = Data / "BFree_viral_images_600.csv"

# Load dataset metadata
df = pd.read_csv(CSV)

# Remove unnecessary metadata columns
df = df.drop(columns=["date", "days_since_1st_post", "w", "h", "md5", "url"], errors="ignore")

# Save updated CSV
df.to_csv(CSV, index=False)
