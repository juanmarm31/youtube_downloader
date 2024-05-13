# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:07:20 2023

@author: rodrjl
"""

import twint

# Configure
c = twint.Config()
c.Store_object = True
c.Custom["tweet"] = ["id", "video_url"]
c.Custom["user"] = ["id"]
c.Limit = 20
c.Username = "katelynngorton"

# Run
twint.run.Search(c)

# Get the data
tweets = twint.output.tweets_list

# Extract the video URL
for tweet in tweets:
    if 'video_url' in tweet.__dict__:
        print(tweet.video_url)
