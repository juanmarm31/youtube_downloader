# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:11:27 2023

@author: rodrjl
"""


import subprocess

def download_twitter_video(video_url):
    try:
        command = f"youtube-dl -o '%(title)s.%(ext)s' {video_url}"
        subprocess.call(command, shell=True)
        print("Video downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    twitter_video_url = input("Enter the Twitter video URL: ")
    download_twitter_video(twitter_video_url)
