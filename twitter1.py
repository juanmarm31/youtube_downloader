# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:01:21 2023

@author: rodrjl
"""

import requests
from bs4 import BeautifulSoup
import re

def extract_m3u8_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                m3u8_links = re.findall(r'(https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.m3u8)', script.string)
                if m3u8_links:
                    return m3u8_links[0]
    return None

# Example usage
twitter_url = "https://twitter.com/katelynngorton/status/1068523656404381697"
m3u8_link = extract_m3u8_link(twitter_url)

if m3u8_link:
    print(f"M3U8 link found: {m3u8_link}")
else:
    print("No M3U8 link found on the provided URL.")

