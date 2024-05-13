# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:36:00 2023

@author: rodrjl
"""

import csv
import requests

# Function to check if a URL is a valid video URL
def is_video_url(url):
    return 'youtube.com' in url or 'facebook.com' in url or 'twitter.com' in url

# Function to check the availability of a video URL
def check_video_availability(url):
    if 'youtube.com' in url:
        video_id = url.split('?v=')[-1]
        response = requests.get(f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}')
        if response.status_code == 200:
            return 'found'
        elif 'Video not found' in response.text:
            return 'not found'
        else:
            return 'private'
    elif 'facebook.com' in url:
        response = requests.get(url)
        if 'This content is no longer available' in response.text:
            return 'not found'
        elif 'This is a private video' in response.text:
            return 'private'
        else:
            return 'found'
    elif 'twitter.com' in url:
        response = requests.get(url)
        if 'This Tweet is unavailable' in response.text:
            return 'not found'
        elif 'This Tweet is from a protected account' in response.text:
            return 'private'
        else:
            return 'found'
    else:
        return 'not supported'

# Read the CSV file
with open('DW_Sirens_RealRecordings.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Create an output CSV file
    with open('output_log.csv', 'w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['Tags', 'Original url', 'Video Status']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        
        for row in csv_reader:
            url = row['Original url']
            
            if is_video_url(url):
                video_status = check_video_availability(url)
                row['Video Status'] = video_status
                csv_writer.writerow(row)
            else:
                row['Video Status'] = 'not supported'
                csv_writer.writerow(row)
