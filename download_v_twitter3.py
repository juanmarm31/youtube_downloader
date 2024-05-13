# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:53:50 2023

@author: rodrjl
"""

# commands to install pip install youtube-dl


import youtube_dl

def download_twitter_video(video_url, path_to_save):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }

    # Download the video using youtube-dl
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Example usage:
tweet_url = 'https://twitter.com/katelynngorton/status/1068523656404381697'
save_path = 'H:\\MDS\\Dataset_collection\\output'  # Use double backslashes in paths on Windows

download_twitter_video(tweet_url, save_path)

