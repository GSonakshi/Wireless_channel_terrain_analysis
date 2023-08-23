# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""

"""
# To  check desired libraries
my_file = open("requirements.txt", "r")
content = my_file.read()
required = content.split(",")
my_file.close()
depends = ["".join(each).split(".")[0][:-1].strip() for each in "".join(os.popen("pip list")).split("\n")]
"""

import Plots_graphs.plots as plot
from Antenna_properties.Antenna_pattern import Available_Antenna_patterns
from Antenna_properties.Directivity import get_antenna_properties
from Channel_properties.Channel_characteristics import get_channel_properties
from Channel_properties.Terrain_characteristics import Terrain_map

if __name__ == '__main__':
    '''defined objects for each class imported'''
    Channel_info = get_channel_properties()
    Antenna_type = Available_Antenna_patterns()
    Antenna_info = get_antenna_properties()
    Terrain_map = Terrain_map()

    '''Enter Transmitter and receiver coordinates
    Assume origin on top left corner (o) of height map/image
            -----> y axis
        !   o_______________
        !   |              |
        !   |  Height map/ |
        V   |   Image      |
     x axis |              |
            |______________|

            Assume one unit as one meter, 
            for example, Transmitter is at [3,50] this means ít is 3 meters in direction of x axis 
            and 50 meters in direction of y axis from origin.
            '''
    Transmitter = [8, 6]
    Receiver = [100, 110]

    '''Enter Transmitter antenna nad receiver antenna height'''
    height_receiver_antenna = 1  # in meters
    height_transmitter_antenna = 10  # in meters

    '''
    Insert Grayscale image path
    # feed grayscale image from file
    '''
    imagepath = 'Channel_properties/download.jpg'
    Height_map = Terrain_map.get_htmap(imagepath)
    '''feed image from Intel Realsense camera'''
    # imagepath = cam.Capture_image()
    # Height_map = imagepath
    '''
        wavelength = Wavelength in meters

        c = Speed of Light (299,792,458 m/s)

        frequency = Frequency (MHz)

    '''
    c = 299792458  # in m/s
    frequency = 6007864889.78  # in Hz
    wavelength = c / frequency  # in meters as we are considering 6GHz frequency (4G)
    # 4g use frequencies in the microwave spectrum

    ''' terrain parameters and transmitter receiver antenna position are extracted from the image'''

    Transmitter, Receiver = Terrain_map.get_position(Transmitter, Receiver, Height_map,
                                                     height_transmitter_antenna, height_receiver_antenna)

    ''' X an Y are list of coordinates on equation of line between transmitter and receiver'''
    X, Y = Terrain_map.equation_of_line(Transmitter, Receiver)

    ''' elevation_data is the lost of height profile of the terrain on line joining transmitter and receiver '''
    elevation_data = Terrain_map.data_elevation(Height_map, X, Y)

    '''channel characteristics are extracted as follow
        z_coordinate_los is the list of Z coordinates with respect to X and Y on line of sight'''
    # line of sight detection
    z_coordinate_los, distance_t_r = Channel_info.LOS_elevation(X, Transmitter, Receiver)
    los_nlos = Channel_info.def_los_nlos(elevation_data, z_coordinate_los)

    # Fresnel Zone clearance calculation
    radii = Channel_info.Fresnel_Zone_calculation(wavelength, z_coordinate_los)

    # to read raw data radiation pattern in .csv file for faster iterations
    # Antenna_properties.Patch_antenna.antenna_raw_data_read("Antenna_properties/PatternRawData/20190218_UHF_Patch_Metra_Lin_860M-880M_Pol1.NSI")

    '''write one of the following name of radiation pattern for transmitter and receiver
        Antenna_pattern_RAW_data
        Example_pattern_SqrtSin
        Example_pattern_SinSqr
        Isotropic_Pattern
        Patch_Antenna_pattern_data
        '''
    Transmitter_radiation_pattern = Antenna_type.Isotropic_Pattern
    Receiver_radiation_pattern = Antenna_type.Isotropic_Pattern

    # Peak Directivity and its direction in terms of angle azimuth and elevation
    '''Here, we will find the maximum value of directivity and its direction.
    We are considering the same coordinate/cartesian model as described in Terrain map 
    function'''

    # print("Directivity for Transmitter Antenna" + Transmitter_radiation_pattern.__name__)
    directivity_tx = Antenna_info.Directivity_calculation(Transmitter_radiation_pattern)  # dBi
    # print("Directivity for Transmitter Antenna" + Receiver_radiation_pattern.__name__)
    directivity_rx = Antenna_info.Directivity_calculation(Receiver_radiation_pattern)

    # Based on Fresnel Zone clearance ratio Path loss model is applied
    '''Will add different models in upcoming days'''
    Free_space_path_loss = Channel_info.free_space_loss(distance_t_r, frequency)  # dB
    Two_ray_path_loss = Channel_info.Two_ray_multipath_model_path_loss(distance_t_r, directivity_tx, directivity_rx,
                                                                       height_receiver_antenna,
                                                                       height_transmitter_antenna)  # dB

    '''Link Budget Calculation
    Negative value of Link budget suggests that the system is insufficient.'''
    Transmitted_power = 20  # dBm

    Path_loss = Free_space_path_loss
    Received_power = Channel_info.Received_power(Transmitted_power, directivity_tx, directivity_rx, Path_loss)
    print('Link Budget is ' + str(Received_power) + ' dB')

    Two_path_model_elevation = Channel_info.Two_ray_model_complete_path(Transmitter, Receiver, X,
                                                                        height_receiver_antenna,
                                                                        height_transmitter_antenna)

    '''Plots'''
    '''Uncomment the command for plots of different characteristics of wireless communication link'''
    """ plot line of sight"""
    plot.plot_los(Height_map, X, Y, z_coordinate_los, Transmitter, Receiver)
    # plot.plot_los_slice(Height_map, X, Y, z_coordinate_los, Transmitter, Receiver, elevation_data)
    # plot.two_d_plot_los(X,z_coordinate_los,elevation_data,Transmitter,Receiver)

    """ plot Fresnel Zone"""
    # plot.plot_fresnel_zone(radii, Transmitter, Receiver, Height_map, X, Y, z_coordinate_los)
    # plot.two_d_fresnel_zone(radii,Transmitter,Receiver,elevation_data,z_coordinate_los,X)

    """Plot antenna pattern"""
    # plot.plot_antenna_pattern(Height_map,Transmitter, Receiver,Transmitter_radiation_pattern,Receiver_radiation_pattern)

    """Plot two path model"""
    # plot.plot_two_path_model(X,Y,Two_path_model_elevation,Height_map,Transmitter, Receiver)
    # plot.two_d_two_path_model(Transmitter, Receiver,X, elevation_los, elevation_data,Two_path_model_elevation)
    fig, ax = plot.plot_terrain(Height_map)
