# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 14:41:54 2023

@author: rodrjl
"""

import csv
import os
from pytube import YouTube
from tqdm import tqdm

# Functions for YouTube videos
def download_youtube(url, output_dir, csv_writer, video_count, pbar):
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.filter(file_extension="mp4").first()
        video_title = yt.title

        # Download the video
        stream.download(output_path=output_dir)

        # Write to CSV that the video was found
        csv_writer.writerow({'Original url': url, 'Found': 'Found'})

        pbar.set_description(f"Downloading Video: {video_count}/{total_videos} - {video_title}")
        pbar.update(1)
    except Exception as e:
        # Write to CSV that the video could not be found
        csv_writer.writerow({'Original url': url, 'Found': 'Not Found'})

# Input and output directories
input_folder = 'H:\MDS\Dataset_collection'
output_folder = 'H:\MDS\Dataset_collection\output\youtube'

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the CSV file and download videos
youtube_urls = []

with open(os.path.join(input_folder, 'DW_Sirens_RealRecordings.csv'), mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if 'youtube.com' in row['Original url']:
            youtube_urls.append(row['Original url'])

total_videos = len(youtube_urls)

# Create a CSV file to log which videos were found
csv_log_path = os.path.join(input_folder, 'video_log.csv')
with open(csv_log_path, mode='w', newline='') as csv_file:
    fieldnames = ['Original url', 'Found']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    with tqdm(total=total_videos, desc="Downloading YouTube Videos") as pbar:
        for video_count, url in enumerate(youtube_urls, 1):
            download_youtube(url, output_folder, csv_writer, video_count, pbar)

print("All videos downloaded successfully.")



