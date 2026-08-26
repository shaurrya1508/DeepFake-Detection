import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# =====================================
# CONFIG
# =====================================

DATASET_DIR = "/Users/shaurya/Desktop/deepfake/frames"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# =====================================
# LOAD MODEL
# =====================================

print("[INFO] Loading model...")

model = load_model("deepfake_detector_v2.h5")

print("[INFO] Model loaded successfully!")

# =====================================
# VALIDATION DATA
# NO AUGMENTATION
# =====================================

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation",
    shuffle=False
)

print("\n[INFO] Class mapping:")
print(val_data.class_indices)

# =====================================
# MODEL EVALUATION
# =====================================

print("\n[INFO] Evaluating model...\n")

loss, accuracy = model.evaluate(
    val_data,
    verbose=1
)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print(f"Loss     : {loss:.4f}")
print(f"Accuracy : {accuracy * 100:.2f}%")

# =====================================
# PREDICTIONS
# =====================================

val_data.reset()

predictions = model.predict(
    val_data,
    verbose=1
)

predicted_classes = (predictions >= 0.5).astype(int).flatten()

true_classes = val_data.classes

# =====================================
# CLASSIFICATION REPORT
# =====================================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(
    classification_report(
        true_classes,
        predicted_classes,
        target_names=["REAL", "FAKE"]
    )
)

# =====================================
# CONFUSION MATRIX
# =====================================

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(
    confusion_matrix(
        true_classes,
        predicted_classes
    )
)