# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 13:08:51 2023

@author: rodrjl
"""

import requests
from bs4 import BeautifulSoup

# Define the URL of the Twitter tweet containing the video
tweet_url = 'https://twitter.com/clairemetzwesh/status/801513850914873344'

# Send an HTTP GET request to the tweet URL
response = requests.get(tweet_url)

if response.status_code == 200:
    # Parse the HTML content of the tweet using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the video element in the HTML (you may need to inspect the Twitter webpage to find the correct element)
    video_element = soup.find('div', {'class': 'tweet'})
    
    if video_element:
        # Extract the video URL (you may need to inspect the Twitter webpage to find the correct attribute)
        video_url = video_element['data-url']
        
        # Download the video using the obtained URL
        video_response = requests.get(video_url)
        
        if video_response.status_code == 200:
            with open('downloaded_video.mp4', 'wb') as f:
                f.write(video_response.content)
                print('Video downloaded successfully.')
        else:
            print('Failed to download the video.')
    else:
        print('Video element not found in the tweet.')
else:
    print('Failed to retrieve the tweet.')
