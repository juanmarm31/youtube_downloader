# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 10:46:20 2023

@author: rodrjl
"""
#python -m pip install --upgrade pytube

import youtube_dl
from pytube import YouTube

def download_twitter_video2(url,dir):
    # Set the URL of the video you want to download
    url = url
    # Download the video using pytube
    yt = YouTube(url,use_oauth=True, allow_oauth_cache=True)
    
    stream = yt.streams.get_highest_resolution()
    stream.download()

def download_twitter_video(video_url,path_to_save):
    # create a dictionary of youtube-dl options
    ydl_opts = {
        #'format': 'bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]',
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4'
    }
    
    # download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def download_twitter_video1(link, path):
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    # download the video
    video.download(path)

# Example usage:
link = 'https://twitter.com/katelynngorton/status/1068523656404381697'
path = 'H:\\MDS\\Dataset_collection\\output\\twitter'  # Use double backslashes in paths on Windows

download_twitter_video(link, path)



