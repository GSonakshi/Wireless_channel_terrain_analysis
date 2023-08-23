# Wireless channel terrain analysis


**Aim:** Terrain analysis with a transmitter and receiver. The goal is to project topographic information of the terrain along with channel characteristics between transmitter and receiver. 

**Procedure:** Using OpenCV python library cv2. Read the image, we get numpy array of pixcel informatoin of the image. The pixel information can be interprted as depth information in that pixel, as we ar using grayscale heightmap image. Now, the heightmap represents higher altitude with light shade (white colour), but in the numpy array it has lesser value than the dark pixels, therefore, we need to invert the numpy array values by subtracting each value with the maximum value. 
We define coordinates in (x,y) plane for transmitter and receiver. Assuming orrigin on top left corner ad x axis  vertically downwards and y asis horizontal. Then we calculate the line segment between transmitter and reciever, and then calculate the elevation data for line of sight from transmitter to receiver. then, we compare the elevation information from the heightmap on the line segment with the line of sight and return the results