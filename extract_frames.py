import cv2
import os
from tqdm import tqdm

# ===== PATHS =====

FAKE_VIDEO_DIR = os.path.expanduser(
    "~/Desktop/deepfake/deepfake_data/manipulated_sequences/Deepfakes/c23/videos"
)

REAL_VIDEO_DIR = os.path.expanduser(
    "~/Desktop/deepfake/deepfake_data/original_sequences/youtube/c23/videos"
)

FAKE_OUTPUT_DIR = os.path.expanduser(
    "~/Desktop/deepfake/frames/fake"
)

REAL_OUTPUT_DIR = os.path.expanduser(
    "~/Desktop/deepfake/frames/real"
)

# ==================


def extract_frames(video_dir, output_dir, label):

    os.makedirs(output_dir, exist_ok=True)

    videos = [v for v in os.listdir(video_dir) if v.endswith(".mp4")]

    for video_name in tqdm(videos, desc=f"Extracting {label}"):

        video_path = os.path.join(video_dir, video_name)

        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        saved_count = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            # Save every 10th frame
            if frame_count % 10 == 0:

                filename = f"{video_name[:-4]}_{saved_count}.jpg"

                save_path = os.path.join(output_dir, filename)

                cv2.imwrite(save_path, frame)

                saved_count += 1

            frame_count += 1

        cap.release()

    print(f"\nFinished extracting {label} frames")


# ===== RUN =====

extract_frames(FAKE_VIDEO_DIR, FAKE_OUTPUT_DIR, "FAKE")
extract_frames(REAL_VIDEO_DIR, REAL_OUTPUT_DIR, "REAL")

