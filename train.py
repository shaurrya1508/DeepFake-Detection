import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
import os

# =====================================
# DATASET PATH
# =====================================

DATASET_DIR = os.path.expanduser(
    "~/Desktop/deepfake/frames"
)

# =====================================
# IMAGE SETTINGS
# =====================================

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# =====================================
# DATA GENERATOR
# =====================================

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=10,
    zoom_range=0.1,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

val_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# =====================================
# LOAD EXISTING MODEL
# =====================================

print("\n[INFO] Loading existing model...")

model = load_model("deepfake_detector.h5")

print("[INFO] Existing model loaded successfully!")

# =====================================
# UNFREEZE LAST LAYERS FOR FINE-TUNING
# =====================================

base_model = model.layers[0]

base_model.trainable = True

# Freeze early layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

print("[INFO] Fine-tuning last 30 layers...")

# =====================================
# COMPILE MODEL
# =====================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# =====================================
# TRAIN MODEL
# =====================================

print("\n[INFO] Training started...\n")

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=10
)

# =====================================
# SAVE UPDATED MODEL
# =====================================

model.save("deepfake_detector_v2.h5")

print("\n[INFO] Model saved as deepfake_detector_v2.h5")