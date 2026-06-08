#!/usr/bin/env python3

import argparse
import os
import urllib.request
import tempfile
import time
import sys
import json
from tqdm import tqdm
from os.path import join

# URLs and filenames
FILELIST_URL = 'misc/filelist.json'
DEEPFAKES_DETECTION_URL = 'misc/deepfake_detection_filenames.json'

DEEPFAKES_MODEL_NAMES = [
    'decoder_A.h5',
    'decoder_B.h5',
    'encoder.h5'
]

# Parameters
DATASETS = {
    'original_youtube_videos': 'misc/downloaded_youtube_videos.zip',
    'original_youtube_videos_info': 'misc/downloaded_youtube_videos_info.zip',
    'original': 'original_sequences/youtube',
    'DeepFakeDetection_original': 'original_sequences/actors',
    'Deepfakes': 'manipulated_sequences/Deepfakes',
    'DeepFakeDetection': 'manipulated_sequences/DeepFakeDetection',
    'Face2Face': 'manipulated_sequences/Face2Face',
    'FaceShifter': 'manipulated_sequences/FaceShifter',
    'FaceSwap': 'manipulated_sequences/FaceSwap',
    'NeuralTextures': 'manipulated_sequences/NeuralTextures'
}

ALL_DATASETS = [
    'original',
    'DeepFakeDetection_original',
    'Deepfakes',
    'DeepFakeDetection',
    'Face2Face',
    'FaceShifter',
    'FaceSwap',
    'NeuralTextures'
]

COMPRESSION = ['raw', 'c23', 'c40']
TYPE = ['videos', 'masks', 'models']
SERVERS = ['EU', 'EU2', 'CA']


def parse_args():
    parser = argparse.ArgumentParser(
        description='Downloads FaceForensics++ public data release.'
    )

    parser.add_argument('output_path', type=str)
    parser.add_argument(
        '-d', '--dataset',
        type=str,
        default='Deepfakes',
        choices=list(DATASETS.keys()) + ['all']
    )

    parser.add_argument(
        '-c', '--compression',
        type=str,
        default='c23',
        choices=COMPRESSION
    )

    parser.add_argument(
        '-t', '--type',
        type=str,
        default='videos',
        choices=TYPE
    )

    parser.add_argument(
        '-n', '--num_videos',
        type=int,
        default=None
    )

    parser.add_argument(
        '--server',
        type=str,
        default='EU',
        choices=SERVERS
    )

    args = parser.parse_args()

    # Server URLs
    if args.server == 'EU':
        server_url = 'https://canis.vc.in.tum.de:8100/'
    elif args.server == 'EU2':
        server_url = 'https://kaldir.vc.in.tum.de/faceforensics/'
    else:
        server_url = 'https://falas.cmpt.sfu.ca:8100/'

    args.tos_url = server_url + 'webpage/FaceForensics_TOS.pdf'
    args.base_url = server_url + 'v3/'
    args.deepfakes_model_url = (
        server_url + 'v3/manipulated_sequences/Deepfakes/models/'
    )

    return args


def reporthook(count, block_size, total_size):
    global start_time

    if count == 0:
        start_time = time.time()
        return

    duration = time.time() - start_time
    progress_size = int(count * block_size)

    speed = int(progress_size / (1024 * duration)) if duration > 0 else 0

    percent = int(count * block_size * 100 / total_size)

    sys.stdout.write(
        f"\rProgress: {percent}% | "
        f"{progress_size / (1024 * 1024):.2f} MB | "
        f"{speed} KB/s"
    )

    sys.stdout.flush()


def download_file(url, out_file, report_progress=False):
    out_dir = os.path.dirname(out_file)
    os.makedirs(out_dir, exist_ok=True)

    if os.path.isfile(out_file):
        tqdm.write(f"Skipping existing file: {out_file}")
        return

    fh, out_file_tmp = tempfile.mkstemp(dir=out_dir)
    os.close(fh)

    if report_progress:
        urllib.request.urlretrieve(url, out_file_tmp, reporthook=reporthook)
    else:
        urllib.request.urlretrieve(url, out_file_tmp)

    os.rename(out_file_tmp, out_file)


def download_files(filenames, base_url, output_path):
    os.makedirs(output_path, exist_ok=True)

    for filename in tqdm(filenames):
        download_file(
            base_url + filename,
            join(output_path, filename)
        )


def main(args):

    print("Accept FaceForensics++ Terms of Service:")
    print(args.tos_url)
    input("Press ENTER to continue...")

    datasets = (
        [args.dataset]
        if args.dataset != 'all'
        else ALL_DATASETS
    )

    for dataset in datasets:

        dataset_path = DATASETS[dataset]

        print(f"\nDownloading dataset: {dataset}")

        # Load file list
        if 'DeepFakeDetection' in dataset_path or 'actors' in dataset_path:

            filepaths = json.loads(
                urllib.request.urlopen(
                    args.base_url + DEEPFAKES_DETECTION_URL
                ).read().decode("utf-8")
            )

            if 'actors' in dataset_path:
                filelist = filepaths['actors']
            else:
                filelist = filepaths['DeepFakeDetection']

        else:
            file_pairs = json.loads(
                urllib.request.urlopen(
                    args.base_url + FILELIST_URL
                ).read().decode("utf-8")
            )

            filelist = []

            for pair in file_pairs:

                if 'original' in dataset_path:
                    filelist += pair
                else:
                    filelist.append('_'.join(pair))
                    filelist.append('_'.join(pair[::-1]))

        if args.num_videos:
            filelist = filelist[:args.num_videos]

        dataset_url = (
            args.base_url +
            f"{dataset_path}/{args.compression}/{args.type}/"
        )

        dataset_output_path = join(
            args.output_path,
            dataset_path,
            args.compression,
            args.type
        )

        filelist = [f + '.mp4' for f in filelist]

        print(f"Saving to: {dataset_output_path}")

        download_files(
            filelist,
            dataset_url,
            dataset_output_path
        )


if __name__ == "__main__":
    args = parse_args()
    main(args)