from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import io

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()  # Adds HEIC/HEIF support to PIL
except ImportError:
    print("[WARN] pillow-heif not installed. HEIC images won't work. Run: pip install pillow-heif")

from tensorflow.keras.models import load_model

# ============================================================
# CONFIGURATION
# ============================================================
MODEL_PATH  = "deepfake_detector_v2.h5"  # change to deepfake_detector.h5 if needed
IMAGE_SIZE  = 224
CLASS_NAMES = ["REAL", "FAKE"]

app = Flask(__name__)
CORS(app)

# ============================================================
# LOAD MODEL (once at startup)
# ============================================================
print("[INFO] Loading model...")
model = load_model(MODEL_PATH)
print("[INFO] Model loaded successfully!")


# ============================================================
# PREPROCESS — accepts a PIL Image directly
# ============================================================
def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    img = pil_image.resize((IMAGE_SIZE, IMAGE_SIZE))
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)   # shape: (1, 224, 224, 3)
    return arr


# ============================================================
# PREDICT ENDPOINT
# ============================================================
@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    print(f"[DEBUG] Received file: {file.filename}, content_type: {file.content_type}")

    try:
        file.stream.seek(0)
        image_bytes = file.stream.read()

        if not image_bytes:
            return jsonify({"error": "Received empty file"}), 400

        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Run inference
        arr        = preprocess_image(image)
        prediction = model.predict(arr, verbose=0)
        confidence = float(prediction[0][0])

        if confidence >= 0.5:
            label = CLASS_NAMES[1]   # FAKE
            score = confidence
        else:
            label = CLASS_NAMES[0]   # REAL
            score = 1 - confidence

        result = {
            "prediction": label,
            "confidence": round(score * 100, 2)
        }

        print(f"[RESULT] {label} — {result['confidence']}%")
        return jsonify(result)

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": "Model inference failed"}), 500


# ============================================================
# HEALTH CHECK  →  GET http://127.0.0.1:5000/
# ============================================================
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Backend is running ✅"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)