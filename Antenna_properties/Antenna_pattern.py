# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""



from math import sin, sqrt, radians
import numpy as np
import pandas as pd


class Available_Antenna_patterns:
    @staticmethod
    def Example_pattern_SqrtSin():
        """
        See Fig1 @ http://www.antenna-theory.com/basics/directivity.php
        Expect Directivity to be 1.05dB.
        """
        df = pd.read_csv('Antenna_properties/EIRP_Data.csv')
        theta1d = df['Theta']
        theta1d = np.array(theta1d);
        theta2d = theta1d.reshape([37, 73])
        THETA = np.deg2rad(theta2d)

        phi1d = df['Phi']
        phi1d = np.array(phi1d);
        phi2d = phi1d.reshape([37, 73])

        power2d = np.sqrt(np.sin(np.radians(THETA)))*10
        return theta2d,phi2d,power2d

    @staticmethod
    def Example_pattern_SinSqr():
        """
        See Fig1 @ http://www.antenna-theory.com/basics/directivity.php
        Expect Directivity to be 2.707dB.
        """
        df = pd.read_csv('Antenna_properties/EIRP_Data.csv')
        theta1d = df['Theta']
        theta1d = np.array(theta1d);
        theta2d = theta1d.reshape([37, 73])
        THETA = np.deg2rad(theta2d)

        phi1d = df['Phi']
        phi1d = np.array(phi1d);
        phi2d = phi1d.reshape([37, 73])

        power2d = np.sin(np.radians(THETA)) ** 10

        return theta2d,phi2d,power2d

    @staticmethod
    def Isotropic_Pattern():
        """
        Isotropic directional pattern. i.e. radiation is same in all directions.
        Expect directivity to be 0dB.
        """
        df = pd.read_csv('Antenna_properties/EIRP_Data.csv')
        theta1d = df['Theta']
        theta1d = np.array(theta1d);
        theta2d = theta1d.reshape([37, 73])
        THETA = np.deg2rad(theta2d)

        phi1d = df['Phi']
        phi1d = np.array(phi1d);
        phi2d = phi1d.reshape([37, 73])

        power2d = np.ones_like(THETA)
        power2d = 10*power2d
        return theta2d,phi2d,power2d

    @staticmethod
    def Antenna_pattern_RAW_data():
        """
        Reading Antenna Pattern from RAW data, made available from actual readings of a
        antenna pattern of an antenna.
        """
        df = pd.read_csv('Antenna_properties/raw_data_antenna_pattern.csv')
        theta1d = df['Theta']
        theta1d = np.array(theta1d);
        theta2d = theta1d.reshape([37, 73])

        phi1d = df['Phi']
        phi1d = np.array(phi1d);
        phi2d = phi1d.reshape([37, 73])

        power1d = df['Power']
        power1d = np.array(power1d);
        power2d = power1d.reshape([37, 73])

        return theta2d,phi2d,power2d

    @staticmethod
    def Patch_Antenna_pattern_data():
        """
        Reading Antenna Pattern from EIRP_Data.csv, made available from internet and resembles a patch antenna.
        """
        df = pd.read_csv('Antenna_properties/EIRP_Data.csv')
        theta1d = df['Theta']
        theta1d = np.array(theta1d);
        theta2d = theta1d.reshape([37, 73])

        phi1d = df['Phi']
        phi1d = np.array(phi1d);
        phi2d = phi1d.reshape([37, 73])

        power1d = df['Power']
        power1d = np.array(power1d);
        power2d = power1d.reshape([37, 73])

        return theta2d,phi2d,power2d

