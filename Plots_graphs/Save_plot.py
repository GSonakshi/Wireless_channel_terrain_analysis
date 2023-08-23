# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:22:39 2020

@author: Sonakshi Gupta
"""


import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image
import shutil

def create_images(Plot,Function_name):
    if os.path.exists("Plots_graphs/GIF"):
        shutil.rmtree("Plots_graphs/GIF")
    os.mkdir("Plots_graphs/GIF")
    for angle in range(0, 360):
        Plot.view_init(0, angle)
        plt.draw()
        #plt.pause(.001)
        PATH = "Plots_graphs/GIF/"
        plt.savefig(PATH+Function_name+str(angle)+".png")
    create_gif(PATH,Function_name)
    create_video(PATH,Function_name)
    #remove the images created in the process
    shutil.rmtree("Plots_graphs/GIF")

def create_gif(PATH,Function_name):
    # Create the frames
    frames = []

    for i in range(1,360):
        new_frame = Image.open(PATH+Function_name+str(i)+".png")
        frames.append(new_frame)
    Gif_name = 'Plots_graphs/demo_'+Function_name+'.gif'
    if os.path.exists(Gif_name):
        os.remove(Gif_name)
    # Save into a GIF file that loops forever
    frames[0].save(Gif_name, format='GIF', append_images=frames[1:], save_all=True, duration=50, loop=0)


def create_video(PATH,Function_name):
    img_array = []
    for filename in range(1,360):
        img = cv2.imread(PATH+Function_name+str(filename)+".png")
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    video_name = 'Plots_graphs/Demo_'+Function_name+'.avi'
    if os.path.exists(video_name):
        os.remove(video_name)
    out = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()