# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:00:25 2023

@author: rodrjl
"""



#-------------Libraries---------
# pip install pytube
# pip install facebook-downloader

import tkinter
from tkinter import *
from tkinter import filedialog,messagebox
from tkinter import ttk
import os
import requests
import re
from datetime import datetime
import pytube
from pytube import YouTube
import youtube_dl
import subprocess

from bs4 import BeautifulSoup
import urllib

import urllib.parse

#-------------------andere Libraries
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import structural_similarity as ssim



#-----------------Functions

def variables(): 
    global path, path1, path2, path3, path4
    #---------------Getting the parameters
    Social_Media  =  Netz.get()
    Resolution    =  Reso.get()
    Type          =  Typ.get()
    url           =  input_url.get()
    path          =  download_path.get()
    path1         =  download_path1.get()
    path2         =  download_path2.get()
    path3         =  download_path3.get()
    path4         =  download_path4.get()
        
    return Social_Media, Resolution, Type, url, path


def download_facebook(url,Resolution,formato,path):
    if "www.facebook.com" in url:
            url=url
    else:
        try:
          url=requests.head(url).headers['location']
        except:
            details.config(text="Something error error")
    x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)
    if x:
          html = requests.get(url).content.decode('utf-8')
    else:
        details.config("cannot fetch the video url")
    hd=re.search('hd_src:"https',html)
    sd=re.search('sd_src:"https',html)
    list = []
    thelist = [ hd, sd]
    for id,val in enumerate(thelist):
                if val != None:
                    list.append(id)    
    print(list)
    if len(list)==2:
        details.config(text="HD & SD available")
    elif list[0]==0:
        details.config(text="HD available")
    elif list[0]==1:
        details.config(text="SD available")  
    elif len(list)==0:
         details.config(text="Error: No video available")   
    if Resolution <= 576:
        video_url = re.search(rf'sd_src:"(.+?)"', html).group(1)
    elif Resolution >= 720:
        video_url = re.search(rf'hd_src:"(.+?)"', html).group(1)
        
    file_size_request = requests.get(video_url, stream=True)
    block_size = 1024   
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    with open(os.path.join(path,filename) + '.' + formato, 'wb') as f:
        for data in file_size_request.iter_content(block_size):   
            f.write(data)
            
def download_youtube(url,resolution,formato,dir):
    # Set the URL of the video you want to download
    url = url
    # Download the video using pytube
    yt = YouTube(url,use_oauth=True, allow_oauth_cache=True)
    
    if formato == 'mp3' or formato == 'wav':
        # youtube = pytube.YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.filter(only_audio=True).first()
    if formato == 'mp4' or formato == 'avi' or formato == 'webm':
        # youtube = pytube.YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.filter(file_extension=formato, resolution=resolution).first()
        
    stream.download()
    
# def download_youtube1(video_url,video_resolution,video_format,path_to_save):
#     # create a dictionary of youtube-dl options
#     ydl_opts = {
#         #'format': 'bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]',
#         'format': 'bestvideo+bestaudio/best',
#         'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
#         'merge_output_format': video_format,
#     }
    
#     # download the video
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])


# def download_youtube2(url,resolution,formato,path):
#     # Set the URL of the video you want to download
#     link = url
#     path = "https://www.youtube.com/watch?v=8wsYT1PRjIg"
    
#     youtubeObject = YouTube(link)
#     youtube = pytube.YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
#     youtubeObject = youtubeObject.streams.get_highest_resolution()
    
#     try:
#         youtubeObject.download()
#     except:
#         print("An error has ocurred")
#     print("Download is complete3d successful")
    

def download_twitter(video_url, resolution,formato,path):
    # Download the video using requests
    file_size_request = requests.get(video_url, stream=True)

    block_size = 1024   
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    filename = "twitter.mp4"
        
    with open(os.path.join(path,filename) +'.' + formato, 'wb') as f:
        for data in file_size_request.iter_content(block_size):   
            f.write(data)


def download_twitter3(video_url,video_resolution,video_format,path_to_save):
    # create a dictionary of youtube-dl options
    ydl_opts = {
        #'format': 'bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]',
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
        'merge_output_format': video_format
    }
    
    # download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def download_twitter4(url,resolution,formato,dir):
    # Set the URL of the video you want to download
    url = url
    # Download the video using pytube
    yt = YouTube(url,use_oauth=True, allow_oauth_cache=True)
    
    stream = yt.streams.get_highest_resolution()
    stream.download()

    
def download_cspan(url,resolution, formato, path):
    # Send GET request to C-SPAN website and get HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract URL of video in specified resolution and format
    video_url = None
    for source in soup.find_all('source'):
        if source.get('res') == resolution and source.get('type') == f'video/{formato}':
            video_url = source.get('src')
            break
    
    if video_url is None:
        print(f"No video found in resolution {resolution} and format {formato}")
        return
    
    # Download video file
    file_name = f"C-SPAN-{resolution}.{formato}"
    urllib.request.urlretrieve(video_url, file_name)
    
    print(f"Video downloaded as {file_name}")
    
    
def download_cspan1(video_url,resolution,format_code,path):
        try:
            # Specify the format code and resolution
            options = f'-f{format_code}+bestvideo[height<={resolution}]+bestaudio[ext=m4a]'
    
            # Use youtube-dl to download the video with specified options
            subprocess.run(['youtube-dl', video_url, options])
            print("Video downloaded successfully!")
        except Exception as e:
            print(f"Error: {e}")


def download_cspan2(video_url,video_resolution,video_format,path_to_save):
    # create a dictionary of youtube-dl options
    ydl_opts = {
        #'format': 'bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]',
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{path_to_save}/%(title)s.%(ext)s',
        'merge_output_format': video_format,
    }
    
    # download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

#------------------Generic function to download videos

def clr():
    clear = lambda: os.system('cls')
    clear()

def errors1():
    B  = input_url.get()
    B0 = download_path.get()
    
    if B == '' :
        messagebox.showerror("Error", "There is no url detected to download the video. Please add a valid URL.")
        main.destroy()
        main.quit()
        clr()
        return
    if B0 == '':
        messagebox.showerror("Error", "There is no path selected to save the video. Please add a path to download the video.")
        main.destroy()
        main.quit()
        clr()
        return
    
def errors2():
    B1 = download_path1.get()
    B2 = download_path2.get()
    
    if (B1 == '') or (B2 == ''):
        messagebox.showerror("Error", "There is no path selected to calculate the spectrums of the audio files. Plase add the paths of the audios.")
        main.destroy()
        main.quit()
        clr()
        return
    

def errors3():
    B3 = download_path3.get()
    B4 = download_path4.get()
    
    if B3 == '' or B4 == '':
        messagebox.showerror("Error", "There is no path selected to calculate metrics of the audio files. Please add the paths of the audios.")
        main.destroy()
        main.quit()
        clr()
        return

#-------------------------Download video main function

def download_videos():
    errors1()
    
    Social_Media,Resolution,Type,url,path = variables()
    
    if "www.facebook.com" in url and Social_Media=="Facebook":
        download_facebook(url,Resolution,Type,path)
        messagebox.showinfo("Facebook: Downloaded","Successfully downloaded in "+str(path))
    
    elif Social_Media=="YouTube":
        download_youtube(url,Resolution,Type,path)
        messagebox.showinfo("Youtube: Downloaded","Successfully downloaded in "+str(path))
    
    elif Social_Media=="Twitter":
        download_twitter4(url,Resolution,Type,path)
        
        messagebox.showinfo("Twitter: Downloaded","Successfully downloaded in "+str(path))
    
    elif "c-span.org" in url and Social_Media=="C-SPAN":
        download_cspan2(url,Resolution,Type,path)
        
        messagebox.showinfo("C-SPAN: Downloaded","Successfully downloade in "+str(path))
    
    
def Browse():
    download_dir=tkinter.filedialog.askdirectory(initialdir="YOUR DIR PATH")
    download_path.set(download_dir)
    
def Browse1():
    global download_dir1
    download_dir1=tkinter.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Audio files",
                                                        "*.wav*"),
                                                       ("all files",
                                                        "*.*")))
    download_path1.set(download_dir1)
    
def Browse2():
    global download_dir2
    download_dir2=tkinter.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Audio files",
                                                        "*.wav*"),
                                                       ("all files",
                                                        "*.*")))
    download_path2.set(download_dir2)
    
def Browse3():
    global download_dir3
    download_dir3=tkinter.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Audio files",
                                                        "*.wav*"),
                                                       ("all files",
                                                        "*.*")))
    download_path3.set(download_dir3)
    
def Browse4():
    global download_dir4
    download_dir4=tkinter.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Audio files",
                                                        "*.wav*"),
                                                       ("all files",
                                                        "*.*")))
    download_path4.set(download_dir4)
    
    
def disabled_res():
    Social_Media,Resolution,Type,url,path = variables()
    if Social_Media == "YouTube":
        drop2.config(state='normal')
    elif Social_Media == "Facebook":
        drop2.config(state='normal')
    elif Social_Media == "C-SPAN":
        drop2.config(state='disabled')
    elif Social_Media == "Twitter":
        drop2.config(state='disabled')
    

def reshp(spec1,spec2):
    
    matrix1 = spec1
    matrix2 = spec2
    #--------------Re shaping matrix

    # get the total number of elements in each matrix
    total_spec1 = np.prod(spec1.shape)
    total_spec2 = np.prod(spec2.shape)
    # print(total_spec1)
    # print(total_spec2)
    
    # if the total number of elements is different, reshape the matrix with fewer elements
    if total_spec1 > total_spec2:
        num_cols_to_add = matrix1.shape[1] - matrix2.shape[1]
        zeros_to_add = np.zeros((matrix2.shape[0], num_cols_to_add))
        matrix2 = np.concatenate((matrix2, zeros_to_add), axis=1)
    elif total_spec1 < total_spec2:
        num_cols_to_add = matrix2.shape[1] - matrix1.shape[1]
        zeros_to_add = np.zeros((matrix1.shape[0], num_cols_to_add))
        matrix1 = np.concatenate((matrix1, zeros_to_add), axis=1)
    else:
        messagebox.showinfo("The shape of the spectrograms are the same")
        print("The shapes of the spectrograms are the same")
        
    return matrix1,matrix2
    
def spect():
    errors2()
    global sr1,sr2
    # Load the two audio files
    filename1 = download_path1.get()
    filename2 = download_path2.get()
    
    # loading of audio files at native sample rate
    y1, sr1 = librosa.load(filename1, sr=None)
    y2, sr2 = librosa.load(filename2, sr=None)

    # Calculate the spectrograms
    spec1 = np.abs(librosa.stft(y1))
    spec2 = np.abs(librosa.stft(y2))

    #----------Re-shaping function
    matrix1, matrix2 = reshp(spec1,spec2)
    
    spec1 = matrix1
    spec2 = matrix2
    
    return spec1, spec2

def spect2():
    errors3()
    global sr1,sr2
    # Load the two audio files
    filename1 = download_path3.get()
    filename2 = download_path4.get()


    y1, sr1 = librosa.load(filename1, sr=None)
    y2, sr2 = librosa.load(filename2, sr=None)


    # Compute the spectrograms
    spec1 = librosa.stft(y1)
    spec2 = librosa.stft(y2)

    #----------Re-shaping function
    matrix1, matrix2 = reshp(spec1,spec2)
    
    spec1 = matrix1
    spec2 = matrix2
    
    return spec1, spec2

def plot_spect():
    spec1, spec2 = spect()

    # Plot the spectrograms side by side
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
    librosa.display.specshow(librosa.amplitude_to_db(spec1, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
    ax[0].set(title=download_dir1)
    librosa.display.specshow(librosa.amplitude_to_db(spec2, ref=np.max), y_axis='log', x_axis='time', ax=ax[1])
    ax[1].set(title=download_dir2)
    plt.show()


def MSE():
    spec1, spec2 = spect2()
    
    # Compute the spectrograms for each audio file
    spec1_abs = np.abs(spec1)
    spec2_abs = np.abs(spec2)

    # Compute the mean squared error (MSE) between the two spectrograms
    mse = np.mean((spec1_abs - spec2_abs) ** 2)
    mse = round(mse,2)
    return mse
    
def SSIM():
    
    spec1, spec2 = spect2()
    
    #-----------Structural Similarity Index metric

    # Compute the spectrograms for each audio file
    spec1_abs = np.abs(spec1)
    spec2_abs = np.abs(spec2)
    
    # Convert to dB scale
    S_db1 = librosa.amplitude_to_db(spec1_abs)
    S_db2 = librosa.amplitude_to_db(spec2_abs)

    # Calculate Structural Similarity Index metric
    ssim_score = ssim(S_db1, S_db2, data_range=S_db2.max() - S_db2.min())
    ssim_score = round(ssim_score,2)

    ssim_score_percentage = ssim_score*100
    ssim_score_percentage = round(ssim_score_percentage,2)
    return ssim_score, ssim_score_percentage

def D_C():
    spec1, spec2 = spect2()
    
    # Compute the spectrograms for each audio file
    spec1_abs = np.abs(spec1)
    spec2_abs = np.abs(spec2)
    
    # Compute the similarity between the two spectrograms
    # using the cosine similarity measure
    similarity = np.dot(spec1_abs.flatten(), spec2_abs.flatten()) / (np.linalg.norm(spec1_abs) * np.linalg.norm(spec2_abs))
    similarity_percentage = similarity * 100
    
    similarity = round(similarity,2)
    similarity_percentage = round(similarity_percentage,2)
    
    return similarity, similarity_percentage


def separation_bands():
    spec1, spec2 = spect2()
    
    
    #---------------------------Separtation in bands

    # Compute the power spectrograms
    power_spectrogram_1 = np.abs(spec1)**2
    power_spectrogram_2 = np.abs(spec2)**2

    # Compute the frequency bands
    freqs = librosa.core.fft_frequencies(sr=sr1, n_fft=spec1.shape[0])
    bands = np.zeros(4)


    # Creation of bands
    band1 = Band1.get()
    band2 = Band2.get()
    band3 = Band3.get()
    
    if band1 == 0 or band2 == 0 or band3 == 0:
        messagebox.showerror("Error", "THere is no values for Band 1, Band 2 and Band 3.")
        main.destroy()
        # clr()

    # Finding the bands of the different frequencies
    bands[1] = np.where(freqs < band1)[0][-1]
    bands[2] = np.where(freqs < band2)[0][-1]
    bands[3] = np.where(freqs < band3)[0][-1]
    # bands[3] = len(freqs) - 1

    # Compute the similarity scores and MSE

    scores = []
    for i in range(3):
        band_1 = power_spectrogram_1[int(bands[i])+1:int(bands[i+1])+1, :]
        band_2 = power_spectrogram_2[int(bands[i])+1:int(bands[i+1])+1, :]
        mse = np.mean((band_1 - band_2)**2)
        score = 100 - mse*100/np.mean((band_1 + band_2)**2)
        scores.append(score)
            
    A = round(scores[0],2)
    B = round(scores[1],2)
    C = round(scores[2],2)
        
    return A,B,C


def comp_spect():
    
    spec1, spec2  = spect2()
    mse1var       = tkinter.DoubleVar()
    ssim_scorevar = tkinter.DoubleVar()
    ssim_score_percentagevar = tkinter.DoubleVar()
    B1var         = tkinter.DoubleVar()
    B2var         = tkinter.DoubleVar()
    B3var         = tkinter.DoubleVar()
    similarityvar = tkinter.DoubleVar()
    similarity_percentagevar = tkinter.DoubleVar()
    
    
    mse1 = MSE()
    ssim_score, ssim_score_percentage = SSIM()
    B1, B2, B3 = separation_bands()
    similarity, similarity_percentage = D_C()
    
    mse1var.set(mse1)
    ssim_scorevar.set(ssim_score)
    ssim_score_percentagevar.set(ssim_score_percentage)
    B1var.set(B1)
    B2var.set(B2)
    B3var.set(B3)  
    similarityvar.set(similarity)   
    similarity_percentagevar.set(similarity_percentage)
    
    
    MSELabel=tkinter.Label(my_frame3, textvariable = mse1var)
    MSELabel.grid(row=5, column=1)
    
    
    SSIMLabel=tkinter.Label(my_frame3,textvariable = ssim_scorevar)
    SSIMLabel.grid(row=6,column=1)
    
    
    SSIMLabel1=tkinter.Label(my_frame3,textvariable=ssim_score_percentagevar)
    SSIMLabel1.grid(row=6,column=3)
    
    SLabel=tkinter.Label(my_frame3,textvariable=similarityvar)
    SLabel.grid(row=7, column=1)
    
    SLabel1=tkinter.Label(my_frame3,textvariable=similarity_percentagevar)
    SLabel1.grid(row=7, column=3)


    #----------------------------------Similarities between bands
    
    SBLabel10=tkinter.Label(my_frame3,textvariable=B1var)
    SBLabel10.grid(row=12, column=0)
    

    SBLabel20=tkinter.Label(my_frame3,textvariable=B2var)
    SBLabel20.grid(row=12, column=1)
    

    SBLabel30=tkinter.Label(my_frame3,textvariable=B3var)
    SBLabel30.grid(row=12, column=2)


    
    #------------------------------------Metrics to compare


    #-----------------First metric MSE

    # Compute the spectrograms for each audio file
    spec1_abs = np.abs(spec1)
    spec2_abs = np.abs(spec2)

    # Compute the mean squared error (MSE) between the two spectrograms
    mse = np.mean((spec1_abs - spec2_abs) ** 2)

    # Print the result
    print("\n\nThe mean squared error between the two spectrograms is: ", mse)
    # NOTE: the mean squared error is a measure of the similarity between 
    # the two spectrograms, where a smaller value indicates a higher similarity.



    #-----------Structural Similarity Index metric

    # Convert to dB scale
    S_db1 = librosa.amplitude_to_db(np.abs(spec1))
    S_db2 = librosa.amplitude_to_db(np.abs(spec2))

    # Calculate Structural Similarity Index metric
    ssim_score = ssim(S_db1, S_db2, data_range=S_db2.max() - S_db2.min())

    ssim_score_percentage = ssim_score*100

    print(f"\nThe Structural Similarity Index between the two spectrograms is: {ssim_score}")
    print(f"The Structural Similarity Index between the two spectrograms is: {ssim_score_percentage} %\n")
    # NOTE: the SSIM score ranges from 0 to 1, with higher scores 
    # indicating greater similarity between the two images.


    # Compute the similarity between the two spectrograms
    # using the cosine similarity measure
    similarity = np.dot(spec1_abs.flatten(), spec2_abs.flatten()) / (np.linalg.norm(spec1_abs) * np.linalg.norm(spec2_abs))
    similarity_percentage = similarity * 100

    print(f"\nThe similarity between the two audio files is: {similarity}")
    print(f"The similarity in % between the two audio files is: {similarity_percentage}\n")

    #---------------------------Separtation in bands

    # Compute the power spectrograms
    power_spectrogram_1 = np.abs(spec1)**2
    power_spectrogram_2 = np.abs(spec2)**2

    # Compute the frequency bands
    freqs = librosa.core.fft_frequencies(sr=sr1, n_fft=spec1.shape[0])
    bands = np.zeros(4)


    # Creation of bands
    band1 = 200
    band2 = 2000
    band3 = 20000


    # Finding the bands of the different frequencies
    bands[1] = np.where(freqs < band1)[0][-1]
    bands[2] = np.where(freqs < band2)[0][-1]
    bands[3] = np.where(freqs < band3)[0][-1]
    # bands[3] = len(freqs) - 1

    # Compute the similarity scores and MSE

    scores = []
    for i in range(3):
        band_1 = power_spectrogram_1[int(bands[i])+1:int(bands[i+1])+1, :]
        band_2 = power_spectrogram_2[int(bands[i])+1:int(bands[i+1])+1, :]
        mse = np.mean((band_1 - band_2)**2)
        score = 100 - mse*100/np.mean((band_1 + band_2)**2)
        scores.append(score)

    # Print the similarity scores
    print("Similarity in low frequencies: %.2f%%" % scores[0])
    print("Similarity in medium frequencies: %.2f%%" % scores[1])
    print("Similarity in high frequencies: %.2f%%" % scores[2])


#-------------------------------------------END OF THE FUNCTIONS


#----------Start of the interface
main = tkinter.Tk()

main.title("Download & Upload Videos")
root = tkinter.Frame()
root.pack()

#-----------------------------Create tabs

my_notebook = ttk.Notebook(root)
my_notebook.pack()

my_frame1 = tkinter.Frame(my_notebook)
my_frame2 = tkinter.Frame(my_notebook)
my_frame3 = tkinter.Frame(my_notebook)

my_frame1.pack(fill="both", expand=1)
my_frame2.pack(fill="both", expand=1)
my_frame3.pack(fill="both", expand=1)

my_notebook.add(my_frame1,text="Download")
my_notebook.add(my_frame2,text="Spectrogram")
my_notebook.add(my_frame3,text="Comparison")



#-------------------------------------TAB 1



#---------------------- Parameters

path_1           = tkinter.StringVar()
path_2           = tkinter.StringVar()
path_3           = tkinter.StringVar()
path_4           = tkinter.StringVar()
path_5           = tkinter.StringVar()
Netz             = tkinter.StringVar()
Reso             = tkinter.IntVar()
Typ              = tkinter.StringVar()
Band1            = tkinter.DoubleVar()
Band2            = tkinter.DoubleVar()
Band3            = tkinter.DoubleVar()

#-----------------------Initialization

Band1.set(200)
Band2.set(2000)
Band3.set(20000)

#------------------------Social Media

options1 = [
    "Twitter", 
    "Facebook", 
    "YouTube", 
    "C-SPAN", 
    ]

#-------------------------Resolution

options2 = [
    '144', 
    '240', 
    '360', 
    '480', 
    '576',
    '720',
    '1080'
    ]

#---------------------------Format

options3 = [
    'mp3',
    'wav',
    'mp4',
    'avi',
    'webm'
    ]

D0label=tkinter.Label(my_frame1,text="Enter the url of the video: ")
D0label.grid(row=0, column=0,columnspan=8)


input_url=tkinter.StringVar()
video_url=tkinter.Entry(my_frame1,textvariable=input_url,width=80,justify='center')
video_url.grid(row=1, column=0,columnspan=8)

D1label=tkinter.Label(my_frame1, text="Parameters")
D1label.grid(row=2, column=0,columnspan=4)

D2label=tkinter.Label(my_frame1, text="Social Media")
D2label.grid(row=3, column=0)

Netz.set(options1[2])
drop1 = tkinter.OptionMenu(my_frame1, Netz, *options1)#, command=disabled_res)
drop1.grid(row=3, column=1)

D3label=tkinter.Label(my_frame1, text="Resolution")
D3label.grid(row=4, column=0)

Reso.set(options2[2])
drop2 = tkinter.OptionMenu(my_frame1, Reso, *options2)
drop2.grid(row=4, column=1)

D4label=tkinter.Label(my_frame1, text="Type")
D4label.grid(row=5, column=0)

Typ.set(options3[2])
drop3 = tkinter.OptionMenu(my_frame1, Typ, *options3)
drop3.grid(row=5, column=1)

D5label=tkinter.Label(my_frame1,text="Choose Browse path")
D5label.grid(row=6, column=0)


download_path=tkinter.StringVar()
BtnBrowse=tkinter.Button(my_frame1,text="Browse",command=Browse)
BtnBrowse.grid(row=6, column=2)
download_pathEntry=tkinter.Entry(my_frame1,textvariable=download_path,width=80,justify='center')
download_pathEntry.grid(row=7, column=0,columnspan=6)

details=tkinter.Label(my_frame1)
details.grid(row=9, column=1)

BtnDownload=tkinter.Button(my_frame1,text="Download",command = download_videos)
BtnDownload.grid(row=10, column=1)

#-------------------------------------TAB 2

D0label1=tkinter.Label(my_frame2,text="Browse first audio: ")
D0label1.grid(row=0, column=0)

download_path1=tkinter.StringVar()
BtnBrowse1=tkinter.Button(my_frame2,text="Audio 1",command=Browse1)
BtnBrowse1.grid(row=0, column=1)
download_pathEntry1=tkinter.Entry(my_frame2,textvariable=download_path1,width=80,justify='center')
download_pathEntry1.grid(row=1, column=0,columnspan=6)


D0label2=tkinter.Label(my_frame2,text="Browse second audio: ")
D0label2.grid(row=2, column=0)

download_path2=tkinter.StringVar()
BtnBrowse2=tkinter.Button(my_frame2,text="Audio 2",command=Browse2)
BtnBrowse2.grid(row=2, column=1)
download_pathEntry2=tkinter.Entry(my_frame2,textvariable=download_path2,width=80,justify='center')
download_pathEntry2.grid(row=3, column=0,columnspan=6)


BtnPlotSpec=tkinter.Button(my_frame2,text="Plot Spect",command = plot_spect)
BtnPlotSpec.grid(row=4, column=1)


#-------------------------------------TAB 3

D0label3=tkinter.Label(my_frame3,text="Browse first audio: ")
D0label3.grid(row=0, column=0)

download_path3=tkinter.StringVar()
BtnBrowse3=tkinter.Button(my_frame3,text="Audio 1",command=Browse3)
BtnBrowse3.grid(row=0, column=1)
download_pathEntry3=tkinter.Entry(my_frame3,textvariable=download_path3,width=80,justify='center')
download_pathEntry3.grid(row=1, column=0,columnspan=6)


D0label4=tkinter.Label(my_frame3,text="Browse second audio: ")
D0label4.grid(row=2, column=0)

download_path4=tkinter.StringVar()
BtnBrowse4=tkinter.Button(my_frame3,text="Audio 2",command=Browse4)
BtnBrowse4.grid(row=2, column=1)
download_pathEntry4=tkinter.Entry(my_frame3,textvariable=download_path4,width=80,justify='center')
download_pathEntry4.grid(row=3, column=0,columnspan=6)


BtnCompSpec=tkinter.Button(my_frame3,text="Comparison",command = comp_spect)
BtnCompSpec.grid(row=4, column=1)

#---------------Metrics to compare spectrograms based on a transform 

MSELabel0=tkinter.Label(my_frame3,text="MSE= ")
MSELabel0.grid(row=5, column=0)


SSIMLabel0=tkinter.Label(my_frame3,text="SSIM= ")
SSIMLabel0.grid(row=6, column=0)


SSIMLabel1=tkinter.Label(my_frame3,text="SSIM [%]= ")
SSIMLabel1.grid(row=6, column=2)


SLabel0= tkinter.Label(my_frame3,text="Similarity= ")
SLabel0.grid(row=7, column=0)

SLabel2= tkinter.Label(my_frame3,text="Similarity [%]= ")
SLabel2.grid(row=7, column=2)



SBLabel=tkinter.Label(my_frame3,text="Separation in bands= ")
SBLabel.grid(row=8, column=0, columnspan= 8)



SBLabel1=tkinter.Label(my_frame3,text="Band 1= ")
SBLabel1.grid(row=9, column=0)

SBLabel2=tkinter.Label(my_frame3,text="Band 2= ")
SBLabel2.grid(row=9, column=1)

SBLabel3=tkinter.Label(my_frame3,text="Band 3= ")
SBLabel3.grid(row=9, column=2)

SBLabelEntry1=tkinter.Entry(my_frame3,textvariable=Band1,justify='center')
SBLabelEntry1.grid(row=10, column=0)

SBLabelEntry2=tkinter.Entry(my_frame3,textvariable=Band2,justify='center')
SBLabelEntry2.grid(row=10, column=1)

SBLabelEntry3=tkinter.Entry(my_frame3,textvariable=Band3,justify='center')
SBLabelEntry3.grid(row=10, column=2)



SBLabel10=tkinter.Label(my_frame3,text="Sim B1= ")
SBLabel10.grid(row=11, column=0)

SBLabel20=tkinter.Label(my_frame3,text="Sim B2= ")
SBLabel20.grid(row=11, column=1)

SBLabel30=tkinter.Label(my_frame3,text="Sim B3= ")
SBLabel30.grid(row=11, column=2)


root.mainloop()