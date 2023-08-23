# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""

import numpy as np


# from sys import exit
# import cv2
# import warnings


class get_channel_properties:
    @staticmethod
    def LOS_elevation(X, Transmitter, Receiver):
        '''In this function we make a list of height(elevation) or Z coordinates values
        for each point on X-Y plane of line of sight between transmitter and receiver,
        starting from transmitter towards receiver.'''
        iteration_length = np.size(X)
        dist_t_r = np.sqrt(
            np.square((Transmitter[0]) - (Receiver[0])) + np.square(
                (Transmitter[1]) - (Receiver[1])) + np.square((Transmitter[2]) - (Receiver[2])))  # distance between transmitter and reciever
        Z_los = np.linspace(Transmitter[2], Receiver[2], iteration_length)
        return Z_los.tolist(), dist_t_r

    @staticmethod
    def Fresnel_Zone_calculation(wavelength, Z_los):
        ''' Calculate fresnel zone-1, Fresnel Zone radius on each point on line of sight
        (LOS) is calculted and returned.'''

        radii = np.zeros_like(Z_los)
        for i in range(len(Z_los)):
            d1 = i
            d2 = (len(Z_los) - d1-1)
            r = np.sqrt((wavelength * d1 * d2) / (d1 + d2))
            radii[i] = r

        return radii

    @staticmethod
    def free_space_loss(dist_t_r, frequency):
        '''we have used friis formula to calculate
        free space loss: 20log(4*pi*d_in_km/wavelength)
        Distance between transmitter and receiver is in meters'''
        dist_t_r_m = dist_t_r  # distance in m
        frequency_Hz = frequency  # frequency in Hz
        Loss_fs = 20 * np.log10((4 * np.pi * dist_t_r_m * frequency_Hz)/299792458)
        print('Free space loss =', Loss_fs, 'dB')
        return Loss_fs

    @staticmethod
    def def_los_nlos(Z_coordinates_terrain, Z_coordinate_los):
        '''Here, we compare the height values in both the lists at each point
        on the line segment (in 3d space) joining transmitter and receiver,
        and print the results'''
        for i in range(len(Z_coordinate_los)):
            if Z_coordinate_los[i] >= Z_coordinates_terrain[i]:
                length = i + 1
            else:
                result = 0
                length = i
                print("LOS obstructed")
                return result
                break
        if length == (len(Z_coordinate_los)):
            result = 1
            print("LOS established")
            return result

    @staticmethod
    def Received_power(Transmitted_power, directivity_tx, directivity_rx, Path_loss):
        return Transmitted_power + directivity_tx + directivity_rx - Path_loss

    @staticmethod
    def Two_ray_multipath_model_path_loss(dist_t_r, directivity_tx, directivity_rx, receiver_height, transmitter_height):
        test = np.sqrt(receiver_height*transmitter_height)
        Gain_transmitter = directivity_tx
        Gain_receiver = directivity_rx
        Path_loss = 40*np.log10(dist_t_r) - 10*np.log10(Gain_transmitter*Gain_receiver*np.square(receiver_height)*np.square(transmitter_height))
        print('2 Ray ground reflection model path loss =', Path_loss, 'dB')
        return Path_loss
    


    @staticmethod
    def Two_ray_model_complete_path(Transmitter, Receiver, X,height_receiver_antenna,height_transmitter_antenna):
        """
        This function creates complete path for reflected ray in two ray multi-path model.
        Here, We take the point of reflection between the transmitter and receiver, such that
        angle of incident =  angle of reflection
            Tx
            |\
            | \      Rx
         ht |  \    /|
            |   \  / | hr
            |____\/__|
              d1   d2
                 /\
                 |
                 break point


             ht/d1 = hr/d2
             d1 =  d/(1+(hr/ht))
             d2 =  d/(1+(ht/hr))

        Ref: Rappaport, Theodore S. Wireless communications: principles and practice. Vol. 2. New Jersey: prentice hall PTR, 1996.
        """
        ratio = height_transmitter_antenna/height_receiver_antenna  #ht/hr
        iteration_length = np.size(X)
        iteration_length_d1 = np.abs((iteration_length * ratio)/(ratio+1)).astype(int)
        iteration_length_d2 = iteration_length - iteration_length_d1

        break_point = [np.abs((Transmitter[0] + (ratio*Receiver[0])) // (ratio+1)).astype(int),np.abs((Transmitter[1] + (ratio*Receiver[1])) // (ratio+1)).astype(int),np.abs((Transmitter[2]-height_transmitter_antenna + (ratio*(Receiver[2]-height_receiver_antenna))) // (ratio+1)).astype(int) ]  # records x and y coordinates of break point
        #break_point.append(Height_map[break_point[0]][break_point[1]])  # records z coordinate of break_point


        '''Now we need the z coordinates of complete path of the reflected ray
        i,e. incident ray path + reflection path'''
        incident_ray_z = np.linspace(Transmitter[2], break_point[2], iteration_length_d1)
        reflected_ray_z = np.linspace(break_point[2], Receiver[2], iteration_length_d2)
        complete_path_Z = np.append(incident_ray_z, reflected_ray_z)

        return complete_path_Z

  
    
        