from qgis.core import QgsPointXY, QgsRectangle
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
zoom_levels = [100, 200, 400]
zoom_level = 100


      

for feat_idx, feature in enumerate(pivots.getFeatures()):
        
        id, length_ft, NumTowers, WetRad_ft, Degrees, Comment, CountyName = feature.attributes()
        print('ID: ', id, length_ft)
        geom = feature.geometry()
        center_x, center_y = geom.asPoint()
        center_point = QgsPointXY(center_x, center_y)
     
        canvas = iface.mapCanvas()
        extent = QgsRectangle(center_point.x() - zoom_level, center_point.y() - zoom_level,
                                  center_point.x() + zoom_level, center_point.y() + zoom_level)

        canvas.setExtent(extent)
        canvas.refresh()
        canvas.zoomToFeatureExtent(extent)
        canvas.repaint()
        canvas.saveAsImage(f'/home/kashis/Desktop/misc/Capstone/GIS-AI project/Pivot GIS Project/images/{id}_{zoom_level}.png')
        spin(5)
        d = {'id': id, 'length_ft': length_ft, 'NumTowers': NumTowers, 'WetRad_ft': WetRad_ft, 'Degrees': Degrees, 'CountyName': CountyName}
        with open(f'/home/kashis/Desktop/misc/Capstone/GIS-AI project/Pivot GIS Project/images/{id}_{zoom_level}.pkl', 'wb') as file: 
            pickle.dump(d, file) 
            
        if feat_idx == 20:
            break

    
