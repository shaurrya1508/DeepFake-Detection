# DeepFake Detection System

## Overview

DeepFake Detection System is an AI-powered application designed to identify manipulated or AI-generated videos. The system extracts frames from uploaded videos, processes facial features, and uses a deep learning model to classify content as either **Real** or **DeepFake**.

This project demonstrates the practical application of **Computer Vision**, **Deep Learning**, and **Web Development** to combat misinformation and synthetic media.

---

## Features

* Upload video files for analysis
* Automatic frame extraction
* Face detection and preprocessing
* Deep learning-based classification
* Real vs DeepFake prediction
* Interactive web interface
* End-to-end AI pipeline

---

## Tech Stack

### Backend

* Python
* Flask
* OpenCV
* TensorFlow / Keras
* NumPy

### Frontend

* React.js
* Vite
* JavaScript
* CSS

### Machine Learning

* Convolutional Neural Networks (CNN)
* Image Processing
* Binary Classification

---

## Project Structure

```text
DeepFake-Detection/
│
├── frontend/
├── app.py
├── train.py
├── predict.py
├── extract_frames.py
├── package.json
├── package-lock.json
├── README.md
└── .gitignore
```

## Workflow

1. User uploads a video.
2. Frames are extracted from the video.
3. Relevant facial information is processed.
4. The trained deep learning model analyzes the frames.
5. Predictions are aggregated.
6. Final result is displayed as:

   * Real
   * DeepFake

---

## Installation

### Clone Repository

```bash
git clone https://github.com/shaurrya1508/DeepFake-Detection.git
cd DeepFake-Detection
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## Running the Project

### Backend

```bash
python app.py
```

### Frontend

```bash
cd frontend
npm run dev
```

---

## Results

The model analyzes video frames and predicts whether the uploaded content is authentic or manipulated.

Example Output:

```text
Prediction: DeepFake
Confidence: 92%
```

---

## Future Improvements

* Real-time webcam detection
* Higher accuracy models
* Support for larger video formats
* Cloud deployment
* Explainable AI visualizations
* Mobile application support

---

## Applications

* Social media verification
* Digital forensics
* Journalism and fact-checking
* Cybersecurity
* Content authenticity verification

---

## Author

**Shaurya Sharma**

* BE Information Technology
* AI/ML Enthusiast
* Roller Hockey National Medalist & Team India Selection
* Passionate about Artificial Intelligence, Machine Learning, and Computer Vision

---

## License

This project is intended for educational and research purposes.
