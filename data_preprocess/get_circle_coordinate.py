from qgis.core import *
from qgis.gui import QgsMapCanvas
import numpy as np

def get_viewport_coordinates(global_x, global_y, distance):
    # Create QgsPointXY objects for global coordinates
    global_point1 = QgsPointXY(global_x, global_y)
    
    # Calculate point2 using global coordinates and distance
    point1 = np.array([global_x, global_y])
    direction = np.array([1, 0])  # Adjust the direction as needed
    point2 = point1 + distance * 0.3048 * direction
    
    global_point2 = QgsPointXY(point2[0], point2[1])

    return global_point1, global_point2

def transform_coordinates(global_point, canvas):
    # Create a coordinate transform object to convert global coordinates to viewport coordinates
    transform = QgsCoordinateTransform(
        QgsProject.instance().crs(),  # Source CRS (project CRS)
        canvas.mapSettings().destinationCrs(),  # Destination CRS (viewport CRS)
        QgsProject.instance()
    )

    # Transform the global coordinates to viewport coordinates
    viewport_point = transform.transform(global_point)

    return viewport_point

def calculate_pixel_coordinates(viewport_point, viewport_extent, canvas_size):
    # Calculate the pixel coordinates within the viewport
    pixel_x = ((viewport_point.x() - viewport_extent.xMinimum()) / viewport_extent.width()) * canvas_size.width()
    pixel_y = ((viewport_extent.yMaximum() - viewport_point.y()) / viewport_extent.height()) * canvas_size.height()

    return pixel_x, pixel_y

# Get the current map canvas
canvas = iface.mapCanvas()

# Get the extent of the current viewport
viewport_extent = canvas.extent()

# Get the width and height of the canvas in pixels
canvas_size = QSize(canvas.width(), canvas.height())

# Specify the global geographic coordinates (replace with your actual coordinates)
global_x = -9060722
global_y = 3957673

# Specify the desired distance in meters
distance = 1354

# Get global and viewport coordinates
global_point1, global_point2 = get_viewport_coordinates(global_x, global_y, distance)

print("Global Coordinate 1:", global_point1)
print("Global Coordinate 2:", global_point2)

# Transform global coordinates to viewport coordinates
viewport_point1 = transform_coordinates(global_point1, canvas)
viewport_point2 = transform_coordinates(global_point2, canvas)

# Calculate pixel coordinates
pixel_x1, pixel_y1 = calculate_pixel_coordinates(viewport_point1, viewport_extent, canvas_size)
pixel_x2, pixel_y2 = calculate_pixel_coordinates(viewport_point2, viewport_extent, canvas_size)

# Print or use the pixel coordinates
print("Pixel Coordinates 1:", pixel_x1, pixel_y1)
print("Pixel Coordinates 2:", pixel_x2, pixel_y2)
