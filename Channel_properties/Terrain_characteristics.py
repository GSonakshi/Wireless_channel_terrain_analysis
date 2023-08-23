# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""

import numpy as np
from sys import exit
import cv2
import warnings


class Terrain_map:

    @staticmethod
    def get_htmap(img_path):
        '''Read grayscale image using image processing library OpenCv
        for python i.e, cv2.
        It reads the grayscale image as a numpy array,
        where each element in the array matrix corresponds to the
        brightness value in that pixel.
        Now, black representing minimum height (minimum brightness value)
        and white representing maximum height (maximum brightness value) '''

        # second argument is flag
        '''
        cv2.IMREAD_COLOR: It specifies to load a color image. Any transparency of image will be neglected. It is the default flag. Alternatively, we can pass integer value 1 for this flag.
        cv2.IMREAD_GRAYSCALE: It specifies to load an image in grayscale mode. Alternatively, we can pass integer value 0 for this flag.
        cv2.IMREAD_UNCHANGED: It specifies to load an image as such including alpha channel. Alternatively, we can pass integer value -1 for this flag.
        '''
        image = cv2.imread(img_path, 0)
        if image is None:
            print("WARRNING: File path not found or Format error Add .png/.jpg file")
            warnings.filterwarnings("ignore")
            exit(1)
            return None
        if image is not None:
            data = np.asarray(image)
            # self.htmap = np.max(data)-data
            htmap = data
            return htmap

   

    @staticmethod
    def get_position(Transmitter, Receiver, height_map, Transmitter_height, Receiver_height):
        '''
        "Here we will add the z profile of the terrain and the height of antenna " \
        "for both transmitter and receiver."
        '''
        
        Transmitter_Z = height_map[Transmitter[0]][Transmitter[1]]
        Receiver_Z = height_map[Receiver[0]][Receiver[1]]
        Transmitter.append(Transmitter_Z + Transmitter_height)
        Receiver.append(Receiver_Z + Receiver_height)

        return list(Transmitter), list(Receiver)

    @staticmethod
    def equation_of_line(Transmitter, Receiver):
        '''This function equates the two dimensional line segment between receiver
        and transmitter, as we know, that the line segment
        is the shortest path between the two points. Therefore, we get a list
        of  x and y cordinates which lie on this line segment'''
        # Eqaution of line segment between transmitter and reciever

        if Transmitter[0] == Receiver[0] and Transmitter[1] == Receiver[1]:
            print('Error')
            warnings.filterwarnings("Transmitter and receiver at same point")
            exit(1)
            return None

        if Transmitter[0] == Receiver[0]:
            start = Transmitter[1]
            stop = Receiver[1]
            samples = np.abs(stop - start) + 1
            Y = np.uint8(np.linspace(start, stop, num=samples))  # y axis
            X = np.full(samples, Transmitter[0], dtype=np.uint8)
            return X, Y

        else:
            start = Transmitter[0]
            stop = Receiver[0]
            samples = np.abs(stop - start) + 1
            X = np.linspace(start, stop, num=samples, dtype=int)  # x axis
            m = np.float((np.int(Transmitter[1]) - np.int(Receiver[1])) / (
                    np.int(Transmitter[0]) - np.int(Receiver[0])))  # slope
            c = Transmitter[1] - (m * Transmitter[0])  # line constant
            # equation of line
            Y = (m * X + c)
            Y = Y.astype(int)
            return X, Y

    @staticmethod
    def data_elevation(htmap, X, Y):
        '''In this function we make a list of height values (z coordinate)  of
        the x and y coordinated from the line
        segment equated in the above funtion,
        starting from transmitter towards receiver.'''
        Z_data = []
        for each_x, each_y in zip(X.tolist(), Y.tolist()):
            Z_data.append(htmap[each_x][each_y])

        return Z_data
