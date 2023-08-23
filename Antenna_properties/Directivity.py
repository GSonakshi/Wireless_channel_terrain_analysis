# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""

"""
ref[1] http://www.antenna-theory.com/basics/directivity.php
Function to calculate peak directivity.
Includes simple examples to check the results.
"""
from math import sin, pi, log10, radians
import numpy as np
from Antenna_properties.Antenna_pattern import Available_Antenna_patterns


class get_antenna_properties:
    def Get_antenna_pattern(self, RadPatternFunction):
        '''The getattr() method returns the value of the named attribute of an object.
        If not found, it returns the default value provided to the function.'''

        RadPatternFunction = getattr(Available_Antenna_patterns,
                                     RadPatternFunction.__name__)  # get radiation pattern function as an attribute
        theta2d, phi2d, power2d = RadPatternFunction()
        return theta2d, phi2d, power2d

    def Directivity_calculation(self, RadPattern):

        theta2d, phi2d, power2d = get_antenna_properties.Get_antenna_pattern(self,RadPattern)

        """
        This function calculates directivity in dBi value.
        (based on the ArrayCalc calc_directivity.m file)
        It also calculates maximum directivity and its direction in 3D space.
        """

        delta_theta = 5  # Step value of theta (Deg)
        delta_phi = 5  # Step value for phi (Deg)

        dth = radians(delta_theta)
        dph = radians(delta_phi)

        Psum = 0
        Pmax = 0
        Thmax = 0
        Phmax = 0
        Efficiency = 100
        for phi in range(0, 360, delta_phi):  # Phi Integration Loop 0-360 degrees
            for theta in range(0, 180, delta_theta):  # Theta Integration Loop 0-180 degrees
                Theta = int(theta / 5)
                Phi = int(phi / 5)

                eField = power2d[Theta, Phi]  # Total E-field at point
                Pthph = eField * np.conjugate(eField)  # Convert to power

                if Pthph > Pmax:
                    Pmax = Pthph  # Store peak value
                    Thmax = theta  # Store theta value for the maximum
                    Phmax = phi  # Store phi value for the maximum

                Psum = Psum + Pthph * np.sin(np.radians(theta)) * dth * dph

        Pmax = Pmax * (Efficiency / 100)  # Apply antenna efficiency

        directivity = Pmax / (Psum / (4 * np.pi))  # Directivity (linear ratio)
        directivity_dBi = 10 * np.log10(directivity)  # Directivity (dB wrt isotropic)
        print("At Theta = " + str(Thmax) + ", Phi = " + str(Phmax))

        return directivity_dBi