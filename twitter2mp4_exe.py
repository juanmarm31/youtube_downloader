# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:23:28 2023

@author: rodrjl
"""

import csv
import os

def is_twitter_url(url):
    return 'twitter.com' in url

# Specify the path to the csv file
csv_file_path = '/home/rodrjl/MDS/Dataset_collection/DW_Sirens_RealRecordings.csv'

# Specify the output folder
output_folder = '/home/rodrjl/MDS/Dataset_collection/output/twitter'

# Create a log file for Twitter videos
log_file_path = '/home/rodrjl/MDS/Dataset_collection/vid_log_twitter.csv'
log_fieldnames = ['Original url', 'Found']

# Create the log file with headers
with open(log_file_path, 'w', newline='') as log_file:
    log_writer = csv.DictWriter(log_file, fieldnames=log_fieldnames)
    log_writer.writeheader()

# Read the csv file and process Twitter URLs
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        url = row['Original url']

        if is_twitter_url(url):
            command = f"python twitter2mp4.py {url} -d {output_folder}"
            result = os.system(command)
            found = 'Found' if result == 0 else 'Not Found'

            # Append the result to the log file
            with open(log_file_path, 'a', newline='') as log_file:
                log_writer = csv.DictWriter(log_file, fieldnames=log_fieldnames)
                log_writer.writerow({'Original url': url, 'Found': found})
        else:
            print(f"Skipped non-Twitter URL: {url}")

