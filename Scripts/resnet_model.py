#Import the libraries we need

import pandas as pd
import numpy as np
from pathlib import Path

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# Load the CSV and images folder
CSV_FILE = Data / "BFree_viral_images_600.csv"
IMAGE_DIR = Data / "BFree_images_600"

df = pd.read_csv(CSV_FILE)

# Keep columns we need
df = df[["filename", "label", "source_id"]].copy()

# Remove rows with missing information
df = df.dropna(subset=["filename", "label", "source_id"]).copy()

# Check original labels
print("Original label distribution:")
print(df["label"].value_counts(dropna=False))

# Convert labels to strings so .str works
labels = df["label"].astype(str).str.strip().str.upper()

# Encode numeric labels: REAL = 1, and FAKE = 0
df["y"] = labels.map({"REAL": 1,"FAKE": 0,"1": 1,"0": 0})
# Check for unexpected labels
if df["y"].isna().any():
    raise ValueError(
        "Unexpected labels found: "
        f"{df.loc[df['y'].isna(), 'label'].unique()}")

df["y"] = df["y"].astype(int)

print("Encoded label distribution:")
print(df["y"].value_counts())

# Both classes must be present
if df["y"].nunique() != 2:
    raise ValueError("Dataset must contain both REAL and FAKE images.")


# Create image paths

df["image_path"] = df["filename"].apply(
    lambda filename: IMAGE_DIR / Path(str(filename)).name
)

# Remove missing or unreadable images
valid_rows = []

for index, row in df.iterrows():
    try:
        load_img(
            str(row["image_path"]),
            target_size=(224, 224),
            color_mode="rgb"
        )

        valid_rows.append(index)

    except (OSError, ValueError):
        print("Skipping image:", row["filename"])

df = df.loc[valid_rows].reset_index(drop=True)

print("Dataset Information:")
print("Total valid images:", len(df))
print("Unique sources:", df["source_id"].nunique())
print("REAL images:", (df["y"] == 1).sum())
print("FAKE images:", (df["y"] == 0).sum())

if df["y"].nunique() != 2:
    raise ValueError(
        "After checking images, both classes must remain."
    )



# Split by source_id in groups

def group_split(data, test_size, random_state):

    best_split = None
    best_score = float("inf")

    splitter = GroupShuffleSplit(
        n_splits=200,
        test_size=test_size,
        random_state=random_state
    )

    for train_index, test_index in splitter.split(
        data,
        data["y"],
        groups=data["source_id"]
    ):

        train_part = data.iloc[train_index]
        test_part = data.iloc[test_index]

        # Both partitions must contain both classes
        if (
            train_part["y"].nunique() < 2
            or test_part["y"].nunique() < 2
        ):
            continue

        # Prefer similar class proportions and
        # a split close to the desired image count.
        score = (
            abs(len(test_part) / len(data) - test_size)
            + abs(test_part["y"].mean() - data["y"].mean())
            + abs(train_part["y"].mean() - data["y"].mean())
        )

        if score < best_score:
            best_score = score
            best_split = (train_index, test_index)

    if best_split is None:
        raise ValueError(
            "Could not create a source-aware split "
            "containing both REAL and FAKE images."
        )

    return best_split


# First split: approximately 80% training/validation,
# 20% testing
train_val_idx, test_idx = group_split(
    df,
    test_size=0.20,
    random_state=42
)

train_val_df = df.iloc[train_val_idx].reset_index(drop=True)
test_df = df.iloc[test_idx].reset_index(drop=True)

# Second split: approximately 60% training,
# 20% validation, 20% testing overall
train_idx, val_idx = group_split(
    train_val_df,
    test_size=0.25,
    random_state=43
)

train_df = train_val_df.iloc[train_idx].reset_index(drop=True)
val_df = train_val_df.iloc[val_idx].reset_index(drop=True)

# Verify that source identifiers do not overlap
assert set(train_df["source_id"]).isdisjoint(
    val_df["source_id"]
)

assert set(train_df["source_id"]).isdisjoint(
    test_df["source_id"]
)

assert set(val_df["source_id"]).isdisjoint(
    test_df["source_id"]
)

print("\nData Split Information:")

for name, data in [
    ("Training", train_df),
    ("Validation", val_df),
    ("Testing", test_df)
]:
    print(
        name,
        "| Images:", len(data),
        "| Sources:", data["source_id"].nunique(),
        "| REAL:", (data["y"] == 1).sum(),
        "| FAKE:", (data["y"] == 0).sum()
    )


# Convert images into arrays and preprocess
# them for ResNet50.

def prepare_images(data):

    X = []

    for path in data["image_path"]:

        img = load_img(
            str(path),
            target_size=(224, 224),
            color_mode="rgb"
        )

        img_array = img_to_array(img)

        X.append(img_array)

    X = np.array(X, dtype=np.float32)

    # ResNet50-specific preprocessing
    X = preprocess_input(X)

    y = data["y"].values.astype(int)

    return X, y


X_train, y_train = prepare_images(train_df)
X_val, y_val = prepare_images(val_df)
X_test, y_test = prepare_images(test_df)

print("Image preprocessing completed.")
print("Training shape:", X_train.shape)
print("Validation shape:", X_val.shape)
print("Testing shape:", X_test.shape)



# Load pretrained ResNet50 model
base_model = ResNet50(weights="imagenet",include_top=False,input_shape=(224, 224, 3))

base_model.trainable = False

# Add binary classification layer
model = Sequential([base_model,GlobalAveragePooling2D(),Dense(1, activation="sigmoid")])

# Compile model
model.compile(optimizer=Adam(learning_rate=0.0001),loss="binary_crossentropy",metrics=["accuracy"])

model.summary()

# Train the ResNet50 model

early_stop = EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)

history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val), callbacks=[early_stop], verbose=1)

print("Training completed!")
print("Epochs completed:", len(history.history["loss"]))


# Test the model on new images

print("Starting final testing:")

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)

# Obtain predictions
y_prob = model.predict(X_test).flatten()
y_pred = (y_prob >= 0.5).astype(int)

print("FINAL TEST RESULTS")
print("-------------------------")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test Loss: {test_loss:.4f}")

print(f"Precision (REAL): {precision_score(y_test, y_pred, zero_division=0):.4f}")
print(f"Recall (REAL): {recall_score(y_test, y_pred, zero_division=0):.4f}")
print(f"F1-score (REAL): {f1_score(y_test, y_pred, zero_division=0):.4f}")

print("Classification Report:")
print(classification_report(y_test, y_pred, labels=[0, 1], target_names=["FAKE", "REAL"], zero_division=0))



# Compare with majority fake baseline

majority_class = np.bincount(y_train).argmax()

baseline_pred = np.full(len(y_test), majority_class)

baseline_accuracy = accuracy_score(y_test, baseline_pred)

print(" Majority Baseline Comparison:")
print(f"Baseline Accuracy: {baseline_accuracy:.4f}")
print(f"ResNet50 Accuracy: {test_accuracy:.4f}")



# Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["FAKE", "REAL"])

display.plot(cmap="Blues")
plt.title("ResNet50 Test Confusion Matrix")
plt.show()


# Graphs and Accuracy

plt.figure(figsize=(8, 5))
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Model Accuracy Over Epochs")
plt.legend()
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Model Loss Over Epochs")
plt.legend()
plt.show()

# Save the model

model.save("bfree_resnet50.keras")

print("Model training and testing completed!")
