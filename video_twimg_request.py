# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:41:09 2023

@author: rodrjl
"""

import subprocess
import re
import os

# Twitter video URL (e.g., the link to the tweet containing the video)
twitter_video_url = "https://twitter.com/katelynngorton/status/1068523656404381697"

# Run youtube-dl to get the M3U8 URL
try:
    output = subprocess.check_output(['youtube-dl', '-g', twitter_video_url], stderr=subprocess.STDOUT)
    video_url = output.decode('utf-8').strip()
    
    # Check if it's an M3U8 URL
    if video_url.endswith('.m3u8'):
        print("M3U8 URL:", video_url)
    else:
        print("This video is not in M3U8 format.")
except subprocess.CalledProcessError as e:
    print("Error:", e.output.decode('utf-8'))




