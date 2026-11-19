
# B-Free AI-Generated Image Dataset

## Summary

Our dataset was obtained from the B-Free project developed by Guillaro et al., which investigates methods for detecting AI-generated images [2]. The dataset was downloaded from their GitHub repository and contains real photographs and images labeled as fake, along with a corresponding CSV file containing metadata such as image filenames, classification labels (REAL/FAKE), source identifiers, dates, dimensions, and URLs. We performed minor data cleaning by removing solid-color images that had no corresponding identifiers in the CSV and appeared to have been included unintentionally. Because their origins were unclear and they were not represented in the dataset's metadata, we excluded them from our analysis. We then randomly selected 300 real and 300 fake images to create a balanced dataset of 600 images and updated the CSV to include only the selected images. The final dataset is stored in our shared repository as a folder containing the image folder titled `BFree_images_600` and a corresponding metadata file named `BFree_images_600.csv`. This cleaned dataset will serve as the starting point for further preprocessing and model development.

## Provenance

The dataset was obtained from the [B-Free GitHub repository](https://github.com/grip-unina/B-Free/blob/main/training_data/README.md), developed by Guillaro et al. as part of their research on AI-generated image detection [2]. We downloaded the image files and corresponding CSV containing classification labels, source identifiers, and other image metadata. After reviewing the dataset, we removed solid-color images that lacked corresponding CSV identifiers and appeared to have been included unintentionally. We then randomly selected 300 real and 300 fake images to create a balanced dataset of 600 images and updated the CSV to retain only the selected records. The final metadata file contains only three variables, including `filename`, `label`, and `source_id`. The original image content and associated metadata were otherwise preserved. The cleaned image dataset is stored in our shared GitHub repository as an image folder titled `BFree_images_600` and a corresponding metadata file named `BFree_images_600.csv`, with the selection and cleaning procedures documented for reproducibility.

## License

The B-Free GitHub repository is publicly available through the Image Processing Research Group at the University of Naples Federico II (GRIP-UNINA). The repository uses a custom license permitting informational and nonprofit use of its software, provided that copyright notices are retained and the original authors are credited. Commercial use requires additional authorization. Our project is intended for academic, noncommercial research, and we will credit the original authors and repository in accordance with these terms.

## Data Dictionary

The final dataset to be used in the analysis consists of 600 image records stored in a CSV file with three variables (`filename`, `label`, and `source_id`) and a corresponding folder containing the 600 image files.

| Variable | Data Type | Description | Considerations |
|----------|-----------|-------------|----------------|
| `filename` | String | Unique identifier specifying the filename and location of the image within the dataset. | Can be used to organize the images for model training and remove unwanted images during preprocessing. |
| `label` | String | Classifies the image as real (REAL) or AI-generated (FAKE). | **Target variable** for binary image classification. Can be encoded as REAL = 1 and FAKE = 0. |
| `source_id` | String | Unique identifier associated with the image's original source. | Can be used to identify related images or images from the same source. We should ensure that related images are not included in both training and testing sets to prevent leakage. |
| `date` | Datetime | Date and time associated with the image record, including time zone. | Not directly relevant to the model, but helpful for EDA to understand posting timelines and image circulation. Not used for model training. |
| `days_since_1st_post` | Numeric | Number of days since the first recorded posting of the source image. | Not directly relevant to the model, but helpful for EDA to understand posting timelines and image circulation. Not used for model training. |
| `w` | Numeric | Original image width in pixels. | Identifies images that are larger than 224 pixels in width and need to be resized. Not used as a model feature. |
| `h` | Numeric | Original image height in pixels. | Identifies images that are larger than 224 pixels in height and need to be resized. Not used as a model feature. |
| `md5` | String | Unique hash value representing the file's contents. | Can be used to identify duplicate files and remove them during preprocessing. Not used for model training. |
| `url` | String | Web address where the image was originally accessed. | Can be used to access or download the image if necessary. Not used for model training. |

**Note:** Only `filename`, `label`, and `source_id` are retained in the final metadata file. The remaining variables were included in the original dataset but removed during preprocessing.

## Ethical Statement

The B-Free dataset contains real and AI-generated images collected from online sources, which may include copyrighted material or identifiable individuals. Although the dataset is publicly accessible, the repository's license does not necessarily grant permission to redistribute all third-party images. We will consider these restrictions when sharing our dataset and provide appropriate attribution. Additionally, differences in image sources, quality, and content may introduce biases that influence classification performance. We will acknowledge these limitations and avoid presenting our model as a definitive method for determining whether an image is authentic.

## Exploratory Plots

We conducted exploratory data analysis on the original, unprocessed images to examine differences between real and AI-generated images before model training. First, we plotted image width against height to assess variation in resolution and identify potential differences between classes. We also compared aspect ratio distributions to examine differences in image shape and inform our resizing approach. Finally, we compared average image brightness between classes to investigate whether basic visual characteristics could introduce unintended biases. Together, these analyses help identify potential confounding factors and guide preprocessing decisions before training our ResNet50 model.
<img width="2400" height="1800" alt="original_image_dimensions" src="https://github.com/user-attachments/assets/e443de1b-6aa6-4bcf-8d04-ad641c97e6e7" />
<img width="2400" height="1500" alt="image_brightness_distribution" src="https://github.com/user-attachments/assets/ea572137-5664-4cff-8ceb-64aded9da165" />
