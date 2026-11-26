# DS-Project-3
## Contents
This project uses ResNet50 convolutional neural network with TensorFlow and Keras to classify images as either real or AI-generated. This project uses a subset of the B-free images dataset, which contains authentic and AI-generated images that have circulated online, as well as a csv containing the corresponding image identities and sources.

This repository includes: 
- The original and preprocessed B-free data subset.
- Python scripts for data preprocessing, ResNet50 modeling, and evaluation.
- Documentation describing the dataset, preprocessing steps, and modeling approach.
- Model outputs, including training and validation performance visualizations, classification accuracy metrics, confusion matrices, and summary results. 
- References and project documentation needed to understand and reproduce the analysis

The analysis uses a balanced subset of 600 images (290 real and 310 AI-generated) from the B-free dataset [2] to develop a ResNet50 convolutional neural network using transfer learning. The dataset is divided into training, validation, and testing sets, with images grouped by source to prevent data leakage. The model is trained to distinguish real photographs from AI-generated images and evaluated on unseen test data using precision, recall, F1-score, and a confusion matrix. Model performance is also compared against a majority-class baseline, with training and validation results examined to assess potential overfitting. 

## Software and Platform Selection
### Software Types Used
- Visual Studio Code (VS Code)
- Python 3.13
- Git/GitHub
- Windows 11 / macOS 26.2
### Add-on packages
- TensorFlow 2.21.0
- Keras 3.15.1
- pandas 3.0.3
- numpy 2.4.6
- matplotlib 3.11.2
- Pillow 13.0.0
- scikit-learn 1.9.1
- Seaborn 0.13.2
### Platforms used
Visual Studio Code (VS Code) with Python 3.13 and the VS Code integrated terminal, running on Windows 11 and macOS 26.2. 

## Map of Documentation
* DS Project Repository
  * Data: Original Data & Final Dataset used for analysis.
    * BFree_Original:
      * BFree_viral_images.csv:  csv containing labels and sources to 1100 images in the oroginal dataset
      * DataRetrieval.md: instrucitons for obtaining original 1100 image data set from https://github.com/grip-unina/B-Free/blob/main/README.md
      * downolad.ipynb: file used in DataRetrieval.md to download original image folder. 
    * BFree_images_600.csv: csv corresponding to the preprocessed dataset obtained from BFree. 
    * BFree_images_600: Folder containing the 600 selected images (300 real, 300 fake) from the BFree image dataset. This is the "image data subset."
    * README.md
  * Output:
    * README.md
  * Scripts:
    * 01_ImageDownload.py
    * 02_RemoveImages.py
    * 03_Cleaning.py
    * 04_Selecting600.py
    * 05_Resizing.py
    * 06_UpdateCSV.py
  * LICENSE
  * README.md
  * REFERENCES
## Instruction for Reproducing Results
### Software and Environment
- Python 3.13
- Visual Studio Code (VS Code)
- Required Python packages:
  - tensorflow 2.21.0
  - Keras 3.15.1
  - pandas 3.0.3
  - numpy 2.4.6
  - matplotlib 3.11.2
  - Pillow 13.0.0
  - scikit-learn 1.9.1
  - Seaborn 0.13.2
### Reproduce Final Analysis
The preprocessed BFree dataset and csv required for modeling is provided in the Data folder. Users do not need to download or preprocess the original BFree dataset to reproduce the final modeling results. 
1. Clone or download this GitHub repository and open the project folder in Visual Studio Code or PyCharm.
2. Confirm that BFree_images_600.csv and the BFree_images_600 image folder are located in the Data folder.
3. Install the required Python packages run the final modeling script from the Scripts/resnet_model.py
4. The modeling script will:
 - Load the processed dataset containing 600 images (290 REAL and 310 FAKE).
 - Check the image files and preprocess them to 224 × 224 pixels.
 - Divide the images into training, validation, and testing sets based on their source identifiers to reduce data leakage.
 - Train a ResNet50 convolutional neural network using pretrained ImageNet weights.
 - Evaluate model performance using accuracy, precision, recall, F1-score, and a confusion matrix.
 - Compare the model's test accuracy against a majority-class baseline.
 - Generate training and validation accuracy and loss graphs.
5. Check that results are saved into the Output folder.
### Expected Results

In the original recorded run, the model achieved a test accuracy of 97.81%, compared with a majority-class baseline accuracy of 51.82%. The model achieved a precision of 1.0000, recall of 0.9545, and F1-score of 0.9767 for REAL images. However, when the model was run again, the accuracy was only 63% so model performance can vary in different runs, and identical or consistent results are not guaranteed.
