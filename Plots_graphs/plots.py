# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:57:37 2020

@author: Sonakshi Gupta
"""

import Plots_graphs.Save_plot as save
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Antenna_properties.Directivity import get_antenna_properties

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

Antenna_info = get_antenna_properties()


def plot_terrain(Height_map):
    """Plot terrain data in 3d"""
    Terrain_x_max = len(Height_map)
    Terrain_y_max = len(Height_map[0])
    Terrain_x = np.arange(Terrain_x_max)
    Terrain_y = np.arange(Terrain_y_max)
    Terrain_x_mesh, Terrain_y_mesh = np.meshgrid(Terrain_x, Terrain_y)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.xlabel("X")
    plt.ylabel("Y")
    ax.plot_surface(Terrain_x_mesh, Terrain_y_mesh, Height_map, rstride=1, cstride=1, cmap='terrain', edgecolor='none')
    #ax.plot_wireframe(Terrain_x_mesh, Terrain_y_mesh, Height_map)
    return fig, ax


def plot_Transmitter_Receiver(Transmitter, Receiver, ax1):
    """Plots transmitter and receiver"""
    ax1.plot((Transmitter[0], Transmitter[0]), (Transmitter[1], Transmitter[1]), (Transmitter[2], 0), '-k')
    ax1.plot((Receiver[0], Receiver[0]), (Receiver[1], Receiver[1]), (Receiver[2], 0), '-k')
    ax1.text(Transmitter[0], Transmitter[1], Transmitter[2], 'Transmitter')
    ax1.text(Receiver[0], Receiver[1], Receiver[2], 'Receiver')
    return ax1


def two_d_plot_los(X, elevation_los, elevation_data, Transmitter, Receiver):
    """Plot line of sight in 2d"""
    plt.plot(X, elevation_los, label='Line of sight')
    plt.plot(X, elevation_data, label='Terrain elevation')
    plt.plot([Transmitter[0], Transmitter[0]], [0, Transmitter[2]])  # plot transmitter
    plt.text(Transmitter[0], Transmitter[2], 'Transmitter')
    plt.plot([Receiver[0], Receiver[0]], [0, Receiver[2]])  # plot reciever
    plt.text(Receiver[0], Receiver[2], 'Receiver')
    plt.legend()
    plt.xlabel('Distance between the transmitter and receiver (X)')
    plt.ylabel('Height from ground (Z)')
    plt.title('Line of sight and its obstructions')
    plt.grid()
    plt.show()


def plot_los_slice(Height_map, X, Y, elevation_los, Transmitter, Receiver, elevation_data):
    fig, ax = plot_terrain(Height_map)
    v = []
    ax = plot_Transmitter_Receiver(Transmitter, Receiver, ax)
    X_mesh = np.array([X, X])
    Y_mesh = np.array([Y, Y])
    Z_mesh = np.array([elevation_los, elevation_data])
    ax.plot_surface(X_mesh, Y_mesh, Z_mesh, color='red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Height')
    # save.create_images(ax, "plot_los")     # To save the plot in .gif or .avi file
    plt.show()
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)


def plot_los(Height_map, X, Y, elevation_los, Transmitter, Receiver):
    fig, ax = plot_terrain(Height_map)
    ax = plot_Transmitter_Receiver(Transmitter, Receiver, ax)
    ax.plot3D(X, Y, elevation_los, 'red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Height')
    # save.create_images(ax, "plot_los")     # To save the plot in .gif or .avi file
    plt.show()
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.001)


def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmart = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmart + kmart.dot(kmart) * ((1 - c) / (s ** 2))
    return rotation_matrix


def two_d_fresnel_zone(radii, Transmitter, Receiver, elevation_data, elevation_los, X):
    fresnel_zone_upper_bound = []
    for (item1, item2) in zip(elevation_los, radii):
        fresnel_zone_upper_bound.append(item1 + item2)

    fresnel_zone_lower_bound = []
    for (item1, item2) in zip(elevation_los, radii):
        fresnel_zone_lower_bound.append(item1 - item2)

    plt.plot(X, fresnel_zone_upper_bound, 'red', label='Fresnel zone')
    plt.plot(X, fresnel_zone_lower_bound, 'red')

    plt.plot(X, elevation_data, label='Terrain')

    plt.plot([Transmitter[0], Transmitter[0]], [0, Transmitter[2]])  # plot transmitter
    plt.text(Transmitter[0], Transmitter[2], 'Transmitter')
    plt.plot([Receiver[0], Receiver[0]], [0, Receiver[2]])  # plot reciever
    plt.text(Receiver[0], Receiver[2], 'Receiver')

    plt.legend()
    plt.xlabel('Distance between the transmitter and receiver (X)')
    plt.ylabel('Height from ground (Z)')
    plt.title('Fresnel zone and its obstructions')
    plt.grid()
    plt.show()


def plot_fresnel_zone(radii, Transmitter, Receiver, Height_map, center_x, center_y, elevation_los):
    '''
    Fresnel Zone is created as 2D rings on each point on line of sight (LOS)
    So for presentation of Fresnel Zone in the 3d plots,
    Each of the Fresnel Zone is created and then rotated in 3D space of
    the terrain.

    Here, we use rotation matrix function to rotate each 2D ring of Frsnel Zone
    '''
    fig, ax = plot_terrain(Height_map)
    ax = plot_Transmitter_Receiver(Transmitter, Receiver, ax)
    rotation = rotation_matrix_from_vectors(Transmitter, Receiver)
    for j in range(len(radii)):
        theta = np.linspace(0, 2 * np.pi, 80)
        y = radii[j] * np.cos(theta)
        z = radii[j] * np.sin(theta)
        x = np.zeros_like(theta)

        for i in range(len(theta)):
            [x[i], y[i], z[i]] = rotation.dot([x[i], y[i], z[i]]) + [center_x[j], center_y[j], elevation_los[j]]
            ax.plot(x, y, z, 'red')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Height')
    # save.create_images(ax, "plot_fresnel_zone")       # To save the plot in .gif or .avi file
    plt.show()


def angle_axis_quat(theta, axis):
    """
    Given an angle and an axis, it returns a quaternion.
    """
    axis = np.array(axis) / np.linalg.norm(axis)
    return np.append([np.cos(theta / 2)], np.sin(theta / 2) * axis)


def mult_quat(q1, q2):
    """
    Quaternion multiplication.
    """
    q3 = np.copy(q1)
    q3[0] = q1[0] * q2[0] - q1[1] * q2[1] - q1[2] * q2[2] - q1[3] * q2[3]
    q3[1] = q1[0] * q2[1] + q1[1] * q2[0] + q1[2] * q2[3] - q1[3] * q2[2]
    q3[2] = q1[0] * q2[2] - q1[1] * q2[3] + q1[2] * q2[0] + q1[3] * q2[1]
    q3[3] = q1[0] * q2[3] + q1[1] * q2[2] - q1[2] * q2[1] + q1[3] * q2[0]
    return q3


def rotate_quat(quat, vect):
    """
    Rotate a vector with the rotation defined by a quaternion.
    """
    # Transfrom vect into an quaternion
    vect = np.append([0], vect)
    # Normalize it
    norm_vect = np.linalg.norm(vect)
    vect = vect / norm_vect
    # Computes the conjugate of quat
    quat_ = np.append(quat[0], -quat[1:])
    # The result is given by: quat * vect * quat_
    res = mult_quat(quat, mult_quat(vect, quat_)) * norm_vect
    return res[1:]


def plot_antenna_pattern_Transmitter(Transmitter, Receiver, ax, Transmitter_radiation_pattern):
    # Read data file and plot
    theta2d, phi2d, power2d = Antenna_info.Get_antenna_pattern(Transmitter_radiation_pattern)

    R = power2d
    THETA = np.deg2rad(theta2d)
    PHI = np.deg2rad(phi2d)

    X = R * np.sin(THETA) * np.cos(PHI)
    Y = R * np.sin(THETA) * np.sin(PHI)
    Z = R * np.cos(THETA)

    axis = np.subtract(Transmitter, Receiver)
    theta = 1.5

    for i in range(len(PHI)):
        for j in range(len(X[0])):
            [X[i, j], Y[i, j], Z[i, j]] = rotate_quat(angle_axis_quat(theta, axis), [X[i, j], Y[i, j], Z[i, j]])
            [X[i, j], Y[i, j], Z[i, j]] = np.array([X[i, j], Y[i, j], Z[i, j]]) + Transmitter

    ax.plot_surface(X, Y, Z)
    # save.create_images(ax, "plot_antenna_pattern")        # To save the plot in .gif or .avi file
    return ax


def plot_antenna_pattern(Height_map, Transmitter, Receiver, Transmitter_radiation_pattern, Receiver_radiation_pattern):
    fig, ax = plot_terrain(Height_map)
    ax = plot_Transmitter_Receiver(Transmitter, Receiver, ax)
    ax = plot_antenna_pattern_Transmitter(Transmitter, Receiver, ax, Transmitter_radiation_pattern)
    ax = plot_antenna_pattern_Receiver(Transmitter, Receiver, ax, Receiver_radiation_pattern)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Height')
    plt.show()


def plot_antenna_pattern_Receiver(Transmitter, Receiver, ax2, Receiver_radiation_pattern):
    # Read data file and plot
    theta2d, phi2d, power2d = Antenna_info.Get_antenna_pattern(Receiver_radiation_pattern)

    R = power2d * 0.4
    THETA = np.deg2rad(theta2d)
    PHI = np.deg2rad(phi2d)

    X = R * np.sin(THETA) * np.cos(PHI)
    Y = R * np.sin(THETA) * np.sin(PHI)
    Z = R * np.cos(THETA)

    axis = np.subtract(Receiver, Transmitter)
    theta = 1.5708

    for i in range(len(PHI)):
        for j in range(len(X[0])):
            # [X[i, j], Y[i, j], Z[i, j]] = rotate_quat(angle_axis_quat(theta, axis), [X[i, j], Y[i, j], Z[i, j]])
            [X[i, j], Y[i, j], Z[i, j]] = np.array([X[i, j], Y[i, j], Z[i, j]]) + Receiver

    ax2.plot_surface(X, Y, Z)
    return ax2


def plot_two_path_model(X, Y, complete_path_Z, Height_map, Transmitter, Receiver):
    """
    This function creates 3D plot of two path model.
    Here, We take a mid point between the transmitter and receiver and the demonstrate a ray reflected from that point.
    """

    fig, ax = plot_terrain(Height_map)
    ax = plot_Transmitter_Receiver(Transmitter, Receiver, ax)
    ax.plot3D(X, Y, complete_path_Z, 'red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('Height')
    save.create_images(ax, "plot_two_path_model")     # To save the plot in .gif or .avi file
    plt.show()
    for angle in range(0, 360):
        ax.view_init(30, angle)
        plt.draw()
        plt.pause(.001)


def two_d_two_path_model(Transmitter, Receiver, X, elevation_los, elevation_data, complete_path_Z):
    plt.plot(X, elevation_los, label='Line of sight')
    plt.plot(X, elevation_data, label='Terrain elevation')
    plt.plot(X, complete_path_Z, label='Two ray path')
    plt.plot([Transmitter[0], Transmitter[0]], [0, Transmitter[2]])  # plot transmitter
    plt.text(Transmitter[0], Transmitter[2], 'Transmitter')
    plt.plot([Receiver[0], Receiver[0]], [0, Receiver[2]])  # plot reciever
    plt.text(Receiver[0], Receiver[2], 'Receiver')
    plt.legend()
    plt.xlabel('Distance between the transmitter and receiver (X)')
    plt.ylabel('Height from ground (Z)')
    plt.title('Two ray path and line of sight')
    plt.grid()
    plt.show()
