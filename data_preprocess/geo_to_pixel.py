


from qgis.core import QgsCoordinateTransform, QgsProject
from qgis.gui import QgsMapCanvas

# Get the current map canvas
canvas = iface.mapCanvas()

# Get the extent of the current viewport
viewport_extent = canvas.extent()

# Get the width and height of the canvas in pixels
canvas_width = canvas.width()
canvas_height = canvas.height()

# Specify the global geographic coordinates (replace with your actual coordinates)
global_x = -9060722
global_y = 3957673

# Create a QgsPointXY with the global coordinates
global_point = QgsPointXY(global_x, global_y)




# Create a coordinate transform object to convert global coordinates to viewport coordinates
transform = QgsCoordinateTransform(
    QgsProject.instance().crs(),  # Source CRS (project CRS)
    canvas.mapSettings().destinationCrs(),  # Destination CRS (viewport CRS)
    QgsProject.instance()
)

# Transform the global coordinates to viewport coordinates
viewport_point = transform.transform(global_point)

# Calculate the pixel coordinates within the viewport
pixel_x = ((viewport_point.x() - viewport_extent.xMinimum()) / viewport_extent.width()) * canvas_width
pixel_y = ((viewport_extent.yMaximum() - viewport_point.y()) / viewport_extent.height()) * canvas_height

# Print or use the pixel coordinates
print("Pixel Coordinates:", pixel_x, pixel_y)