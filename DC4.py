# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:34:07 2023

@author: rodrjl
"""

import csv
import os
from pytube import YouTube
from tqdm import tqdm

# Map country names to country codes
country_codes = {
    "USA": "us",
    "Spain": "sp",
    "Japan": "ja",
    "China": "ch",
    "India": "in",
    "Italy": "it",
    "France": "fr",
    "Germany": "ge",
    "Canada": "ca"
}

# Functions for YouTube videos
def download_youtube(url, output_dir, csv_writer, video_count, pbar):
    try:
        yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
        
        # Request an MP4 stream
        stream = yt.streams.filter(file_extension="mp4").first()
        video_title = yt.title

        # Extract relevant tags
        tags = row['Tags']
        tags_lower = tags.lower()
        country_code = None
        if 'firefighter' in tags_lower:
            tags = 'f'
        elif 'ambulance' in tags_lower:
            tags = 'a'
        elif 'police' in tags_lower:
            tags = 'p'

        # Extract the first 2 letters of the country name
        for country, code in country_codes.items():
            if country.lower() in tags_lower:
                country_code = code
                break

        # Generate the filename
        if country_code:
            filename = f"{video_count}_{country_code}_{tags}.mp4"  # Ensure MP4 extension
        else:
            filename = f"{video_count}_unknown_{tags}.mp4"  # Ensure MP4 extension

        # Download the video
        stream.download(output_path=output_dir, filename=filename)

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
            youtube_urls.append(row)

total_videos = len(youtube_urls)

# Create a CSV file to log which videos were found
csv_log_path = os.path.join(input_folder, 'video_log.csv')
with open(csv_log_path, mode='w', newline='') as csv_file:
    fieldnames = ['Original url', 'Found']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    with tqdm(total=total_videos, desc="Downloading YouTube Videos") as pbar:
        for video_count, row in enumerate(youtube_urls, 1):
            download_youtube(row['Original url'], output_folder, csv_writer, video_count, pbar)

print("All videos downloaded successfully.")

