# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 17:50:02 2023

@author: rodrjl
"""

import os
import subprocess

input_folder = "/home/rodrjl/MDS/Dataset_collection/output/twitter"  # Change this to the path of your input folder
output_folder = "/home/rodrjl/MDS/Dataset_collection/output/twitter_wav"  # Change this to the path of your output folder

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Get a list of all MP4 files in the input folder
mp4_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]

for mp4_file in mp4_files:
    input_file = os.path.join(input_folder, mp4_file)
    output_file = os.path.join(output_folder, os.path.splitext(mp4_file)[0] + ".wav")

    # Run FFmpeg command to convert MP4 to WAV
    cmd = f'ffmpeg -i "{input_file}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{output_file}"'
    subprocess.call(cmd, shell=True)

print("Conversion complete.")
