import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the matrix from the file
matrix = np.load('matrix_data.npy')

x, y = np.meshgrid(np.arange(matrix.shape[1]), np.arange(matrix.shape[0]))
hf = plt.figure(figsize=(19.2, 10.8))

manager = plt.get_current_fig_manager()
manager.window.state('zoomed')  # type: ignore # Maximizes the plot window


ha = hf.add_subplot(111, projection='3d')
ha.plot_surface(x, y, matrix, rstride=1, cstride=1,
        cmap='viridis', edgecolor='none')

ha.set_box_aspect([1, 1, 1])  # Adjust the values if necessary

# Set aspect ratio to maintain pixel scale in both axes
max_range = np.array([x.max()-x.min(), y.max()-y.min(), matrix.max()-matrix.min()]).max()
x_center = (x.max()+x.min()) / 2
y_center = (y.max()+y.min()) / 2
z_center = (matrix.max()+matrix.min()) / 2

ha.set_xlim(x_center - max_range/2, x_center + max_range/2)
ha.set_ylim(y_center - max_range/2, y_center + max_range/2)
# ha.set_zlim(z_center - max_range/2, z_center + max_range/2)


ha.view_init(elev=40, azim=-20)  # Set the elevation (vertical rotation) and azimuth (horizontal rotation)
ha.dist = 8.2  # Set the distance from the plot

plt.show()
# Create a figure and a 3D axis
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# Create meshgrid from matrix dimensions

# Plot a 3D surface
# ax.plot_surface(x, y, matrix, cmap='viridis')

# Show the plot
# plt.show()


