# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:13:18 2023

@author: rodrjl
"""

import csv

# Initialize counters for each platform
youtube_count = 0
facebook_count = 0
twitter_count = 0

# Read the CSV file
with open('DW_Sirens_RealRecordings.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Iterate through each row in the CSV
    for row in csv_reader:
        url = row['Original url']
        
        if 'youtube.com' in url:
            youtube_count += 1
        elif 'facebook.com' in url:
            facebook_count += 1
        elif 'twitter.com' in url:
            twitter_count += 1

total_vids = youtube_count + facebook_count + twitter_count


# Print the counts for each platform
print(f'YouTube Count: {youtube_count}')
print(f'Facebook Count: {facebook_count}')
print(f'Twitter Count: {twitter_count}')

print(f'Total video Count: {total_vids}')