import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# =========================
# CONFIGURATION
# =========================
MODEL_PATH = "deepfake_detector.h5"  # Your trained model
IMAGE_SIZE = 224
CLASS_NAMES = ["REAL", "FAKE"]

# =========================
# LOAD MODEL
# =========================
print("[INFO] Loading model...")
model = load_model(MODEL_PATH)
print("[INFO] Model loaded successfully!")


# =========================
# PREPROCESS IMAGE
# =========================
def preprocess_image(image_path):
    """
    Loads and preprocesses an image for prediction.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read image. Check file format.")

    # Convert BGR -> RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Resize image
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))

    # Normalize
    image = image.astype("float32") / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    return image


# =========================
# PREDICT FUNCTION
# =========================
def predict_image(image_path):
    """
    Predicts whether an image is REAL or FAKE.
    """

    processed_image = preprocess_image(image_path)

    prediction = model.predict(processed_image, verbose=0)

    # Binary Classification
    confidence = float(prediction[0][0])

    if confidence >= 0.5:
        label = CLASS_NAMES[1]  # FAKE
        score = confidence
    else:
        label = CLASS_NAMES[0]  # REAL
        score = 1 - confidence

    print("\n========== RESULT ==========")
    print(f"Prediction : {label}")
    print(f"Confidence : {score * 100:.2f}%")
    print("============================")


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    image_path = input("Enter image path: ").strip()

    try:
        predict_image(image_path)

    except Exception as e:
        print(f"[ERROR] {e}")
