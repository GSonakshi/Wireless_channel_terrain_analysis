import sys

sys.path.insert(1, 'C:/Users/arp/Desktop/sandbox')  # path of main folder where main.py file is
from Channel_properties.Terrain_characteristics import Terrain_map
from Channel_properties.Channel_characteristics import get_channel_properties
import unittest
import numpy as np


class Test_Terrain_map(unittest.TestCase):
    def test_get_htmap(self):
        '''test get_htmap function'''
        self.assertIsNotNone(Terrain_map.get_htmap("test.png"))
        self.assertRaises(SystemExit, Terrain_map.get_htmap, 'invalid file name or extension')

    def test_get_position(self):
        '''This function simply return the positions according to the parameters '''
        htmap = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        T, R = Terrain_map.get_position([1,1], [1,2], htmap, 1, 2)
        self.assertListEqual(T, [1, 1, 4 + 1])
        self.assertListEqual(R, [1, 2, 5 + 2])

    def test_equation_of_line(self):
        '''Test the generated equation of line '''
        t = np.array([1, 1, 7])
        r = np.array([3, 1, 7])
        x, y = Terrain_map.equation_of_line(t, r)
        x = np.ndarray.tolist(x)
        self.assertListEqual(x, [1, 2, 3])
        y = np.ndarray.tolist(y)
        self.assertListEqual(y, [1, 1, 1])


    def test_data_elevation(self):
        ''' test if elevation data according to height map'''
        htmap = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        x = np.array([0, 1, 2])
        y = np.array([1, 1, 1])
        elevation_data = Terrain_map.data_elevation(htmap, x, y)
        self.assertListEqual(elevation_data, [1, 4, 7])



class Test_get_channel_properties(unittest.TestCase):
    def test_LOS_elevation(self):
        '''This function creates two sets of 3d line equation
        from 3d coordinates and test the function LOS_elevation'''

        # set 1
        t1 = np.array([1, 1, 7])
        r1 = np.array([3, 1, 7])
        x1 = np.array([1, 2, 3])
        y1 = np.array([1, 1, 1])

        # set 2
        t2 = np.array([1, 1, 10])
        r2 = np.array([8, 8, 3])
        x2 = np.array([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(get_channel_properties.LOS_elevation(x1, t1, r1), ([7, 7, 7], 2.0))
        self.assertEqual(get_channel_properties.LOS_elevation(x2, t2, r2), ([10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0], 12.12435565298214))

    def test_def_los_nlos(self):
        '''test if the both line of sight and elevation  data are compared properly or not'''
        elevation_data = [1, 2, 3, 4, 3, 2, 1]
        elevation_los = [1, 2, 3, 4, 5, 6, 7]
        iteration = 7
        result = get_channel_properties.def_los_nlos(elevation_data, elevation_los)
        self.assertEqual(result, 1)


    def test_Fresnel_Zone_calculation(self):
        '''test if the function for first fresnel zone calculation is working correct '''
        elevation_los = [3, 3, 6]
        wvlnt = 50
        radii = np.ndarray.tolist(get_channel_properties.Fresnel_Zone_calculation(wvlnt, elevation_los))
        self.assertListEqual(radii, [0, 5.0, 0])


    def test_free_space_pathloss(self):
        '''If fresnel zone is obstructed more than 60% then we cannot
        apply friis formula'''
        self.assertEqual(get_channel_properties.free_space_loss(10, 6007864889.78), 68.02218636797475)
        self.assertEqual(get_channel_properties.free_space_loss(100, 8000000000), 90.50958296172224)

    """
# class Test_get_antenna_pattern(unittest.TestCase):
if __name__ == '__main__':
    unittest.main()
    """