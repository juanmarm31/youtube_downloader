# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 10:59:59 2023

@author: rodrjl
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt

def plot_audio_levels(audio_path):
    # Read the audio file using librosa
    data, sample_rate = librosa.load(audio_path, sr=44100)

    # Add a small constant to the absolute values to avoid division by zero
    epsilon = 1e-10
    audio_levels = 20 * np.log10(np.abs(data) + epsilon)

    # Create a time array for plotting
    time = np.arange(0, len(data)) / sample_rate

    # Plot the audio levels
    plt.figure(figsize=(10, 6))
    plt.plot(time, audio_levels)
    plt.title("Sound Levels in dB")
    plt.xlabel("Time (s)")
    plt.ylabel("dB")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    audio_path = "H:/MDS/Dataset_collection/output/twitter_wav/4OPu28fAodJXUWt1.wav"
    try:
        plot_audio_levels(audio_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


