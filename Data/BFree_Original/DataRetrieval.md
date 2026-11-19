
# BFree Dataset Download Instructions

## Dataset Overview

This project uses the BFree viral images dataset. Due to the size of the dataset, the images are not stored directly in this GitHub repository. Instead, the original image metadata and download script are provided to allow users to reproduce the dataset locally.

## Files Provided

- `BFree_viral_images.csv` — Image URLs, filenames, and MD5 hashes.
- `download_images.ipynb` — Jupyter Notebook containing the image download script.

## Download Instructions

### 1. Download the Repository

Clone or download this GitHub repository to your local computer.

### 2. Install Required Libraries

Open a terminal in VS Code and run:

```bash
python -m pip install pandas numpy tqdm requests requests-html pillow ipykernel lxml_html_clean
```

### 3. Open the Download Script

Open `download_images.ipynb` in VS Code with the Python and Jupyter extensions installed.

Select your Python kernel in the upper-right corner.

### 4. Set the Download Directory

In the notebook, change the `root` variable to your desired download location:

```python
root = './images/'
os.makedirs(root, exist_ok=True)
```

Make sure `BFree_viral_images.csv` is accessible from the notebook's working directory.

### 5. Run the Notebook

Execute the notebook cells in order to download the images.

The script will:
- Read image URLs from the CSV file.
- Attempt to download the corresponding images.
- Save downloaded files to the specified directory.
- Verify downloaded files using MD5 hashes.
- Remove files that fail verification.

## Notes

- Some image URLs may be inaccessible or expired.
- Download times depend on dataset size and network speed.
- Some Facebook-hosted images may require additional processing or authentication.
- The download script may require updates if the source websites have changed.
- The images are not included in this repository.

## Original Dataset Source

[Insert original GitHub repository URL]

Please refer to the original dataset source for attribution, licensing, and usage restrictions.

