# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:14:11 2023

@author: rodrjl
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def download_twitter_video(url):
    # Initialize a headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # Open Twitter URL
        driver.get(url)

        # Wait for the video to load (you may need to adjust this)
        driver.implicitly_wait(10)

        # Find the video element
        video_element = driver.find_element_by_tag_name('video')

        # Get the video source URL
        video_url = video_element.get_attribute('src')

        if video_url:
            # Download the video using your preferred method
            # You can use libraries like requests or urllib
            # Here's a basic example using requests
            import requests

            response = requests.get(video_url)
            with open("downloaded_video.mp4", "wb") as video_file:
                video_file.write(response.content)

            print("Video downloaded successfully!")
        else:
            print("Video source URL not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    driver.quit()

if __name__ == "__main__":
    twitter_url = input("Enter the Twitter video URL: ")
    download_twitter_video(twitter_url)
