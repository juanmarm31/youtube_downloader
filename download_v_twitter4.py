# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 12:04:50 2023

@author: rodrjl
"""

import requests
import re
import os
from datetime import datetime

def download_twitter_video(url, output_directory):
    if "twitter.com" in url:
        url = url
    else:
        try:
            url = requests.head(url).headers['location']
        except Exception as e:
            print("Error:", str(e))
            return

    if "twitter.com" in url:
        # Fetch the Twitter video page
        response = requests.get(url)
        if response.status_code != 200:
            print("Error: Could not fetch the Twitter video page")
            return

        html = response.text

        # Find the video URL in the HTML
        video_url_match = re.search(r'data-src="([^"]+)"', html)
        if video_url_match:
            video_url = video_url_match.group(1)
        else:
            print("Error: No video URL found on the Twitter page")
            return
    else:
        print("Error: Invalid Twitter URL")
        return

    try:
        file_size_request = requests.get(video_url, stream=True)
        if file_size_request.status_code == 200:
            block_size = 1024
            filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            output_path = os.path.join(output_directory, filename) + '.mp4'

            with open(output_path, 'wb') as f:
                for data in file_size_request.iter_content(block_size):
                    f.write(data)
            print("Video downloaded successfully to:", output_path)
        else:
            print("Error: Failed to fetch the video content")
    except Exception as e:
        print("Error:", str(e))

# Example usage:

tweet_url = "https://twitter.com/katelynngorton/status/1068523656404381697"
save_path = 'H:\\MDS\\Dataset_collection\\output'  # Use double backslashes in paths on Windows

download_twitter_video(tweet_url, save_path)