from qgis.core import QgsPointXY, QgsRectangle, QgsMapToPixel, QgsMapSettings
from PyQt5.QtCore import Qt
import pickle
from PyQt5 import QtWidgets
import time


def spin(seconds):
    """Pause for set amount of seconds, replaces time.sleep so program doesn't stall"""

    time_end = time.time() + seconds
    while time.time() < time_end:
        QtWidgets.QApplication.processEvents()
        
        
layers = QgsProject.instance().mapLayers()
l = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
 
layers_list = {}
for l in QgsProject.instance().mapLayers().values():
    layers_list[l.name()] = l
    
pivots = layers_list['Pivots2018']
features = pivots.getFeatures()
zoom_level = 1000

for feat_idx, feature in enumerate(pivots.getFeatures()):
        
        id, length_ft, NumTowers, WetRad_ft, Degrees, Comment, CountyName = feature.attributes()
        print('New ID---------------------: ', feat_idx, id)
        geom = feature.geometry()
        center_x, center_y = geom.asPoint()
        center_point = QgsPointXY(center_x, center_y)
     
        canvas = iface.mapCanvas()
        extent = QgsRectangle(center_point.x() - zoom_level, center_point.y() - zoom_level,
                                  center_point.x() + zoom_level, center_point.y() + zoom_level)
        
 

        
        #print('Number of pivots: ', len(list(features_within_extent)))
        # 8850, 5703 feet
        # 1546, 1003 pixels
        # 5.724, 5.686
        # pixel_to_feet_factor = 5.7
        
        canvas.setExtent(extent)
        canvas.refresh()
        canvas.zoomToFeatureExtent(extent)
        canvas.repaint()
        spin(5)
        canvas.saveAsImage(f'/home/kashis/Desktop/misc/Capstone/GIS-AI project/Pivot GIS Project/images/{id}_{zoom_level}.png')
        
        pkl_file = open(f'/home/kashis/Desktop/misc/Capstone/GIS-AI project/Pivot GIS Project/images/{id}_{zoom_level}.pkl', 'wb')
        center_pivots = []
        
        layer = iface.activeLayer()
        request = QgsFeatureRequest(iface.mapCanvas().extent())
        request.setFlags(QgsFeatureRequest.ExactIntersect)
        
        viewport_extent = canvas.extent()
        canvas_width = canvas.width()
        canvas_height = canvas.height()
        
        for f in pivots.getFeatures(request):
            id, length_ft, NumTowers, WetRad_ft, Degrees, Comment, CountyName = f.attributes()
            print('X and Y: ', f.geometry().asPoint())
            if not id:
                continue
            if not WetRad_ft:
                WetRad_ft = None
                
            global_point = f.geometry().asPoint()

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
            
            print('PIXEL: ', pixel_x, pixel_y)
            pixel_to_feet_factor = 5.7
            radius_pixels = pixel_to_feet_factor * length_ft
            d = {'id': id, 'length_ft': length_ft, 'NumTowers': NumTowers, 'WetRad_ft': 1, 'Degrees': Degrees, 'CountyName': CountyName, 'pixel_x': pixel_x, 'pixel_y': pixel_y, 'pixel_rad': radius_pixels, 'geo_coords': list(global_point)}
            center_pivots.append(d)
        
        pickle.dump(center_pivots, pkl_file)
    
        
        


