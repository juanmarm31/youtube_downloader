# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:10:13 2023

@author: rodrjl
"""
import re
from selenium import webdriver

def extract_m3u8_link(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no browser window)

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the page to load (you may need to adjust the sleep time)
    import time
    time.sleep(5)

    page_source = driver.page_source
    driver.quit()

    m3u8_links = re.findall(r'(https?://[^"]+\.m3u8)', page_source)
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
