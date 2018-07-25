# -*- coding: UTF-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *

class GeometryFilter():
    
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberband = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberband.setColor(Qt.red)
        self.rubberband.setWidth(1)
        self.point = None
        self.points = []

    def canvasPressEvent(self, e):
        self.point = self.toMapCoordinates(e.pos())
        m = QgsVertexMarker(self.canvas)
        m.setCenter(self.point)
        m.setColor(QColor(0,255,0))
        m.setIconSize(5)
        m.setIconType(QgsVertexMarker.ICON_BOX)
        m.setPenWidth(3)
        self.points.append(self.point)
        self.isEmittingPoint = True
        self.showPoly()
        
    def showPoly(self):
        self.rubberband.reset(QGis.Polygon)
        for point in self.points[:-1]:
        self.rubberband.addPoint(point, False)
        self.rubberband.addPoint(self.points[-1], True)
        self.rubberband.show()


# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool


# Create new virtual layer 
vlyr = QgsVectorLayer("Polygon", "temporary_polygons", "memory")
dprov = vlyr.dataProvider()

# Add field to virtual layer 
dprov.addAttributes([QgsField("name", QVariant.String),
                     QgsField("size", QVariant.Double)])

vlyr.updateFields()

# Access MapTool  
previousMapTool = iface.mapCanvas().mapTool()
myMapTool = QgsMapToolEmitPoint( iface.mapCanvas() )


# create empty list to store coordinates 
coordinates = []

# Access ID 
fields = dprov.fields() 

def drawBand( currentPos, clickedButton ):
    iface.mapCanvas().xyCoordinates.connect( drawBand )

    if myRubberBand and myRubberBand.numberOfVertices():
        myRubberBand.removeLastPoint()
        myRubberBand.addPoint( currentPos )


def mouseClick( currentPos, clickedButton ):
    if clickedButton == Qt.LeftButton and len(coordinates) == 0: 
        # create the polygon rubber band associated to the current canvas
        global myRubberBand 
        myRubberBand = QgsRubberBand( iface.mapCanvas(), QGis.Polygon )
        # set rubber band style
        color = QColor(78, 97, 114)
        color.setAlpha(190)
        myRubberBand.setColor(color)
        #Draw rubberband
        myRubberBand.addPoint( QgsPoint(currentPos) )
        coordinates.append(currentPos)
        print coordinates
    if clickedButton == Qt.LeftButton and len(coordinates) > 0:
        myRubberBand.addPoint( QgsPoint(currentPos) )
        coordinates.append(currentPos)
        print coordinates

    if clickedButton == Qt.RightButton:

         # open input dialog     
        (description, False) = QInputDialog.getText(iface.mainWindow(), "Description", "Description for Polygon at x and y", QLineEdit.Normal, 'My Polygon') 

        #create feature and set geometry             
        poly = QgsFeature() 
        geomP = QgsGeometry.fromPolygon([coordinates])
        poly.setGeometry(geomP) 

        #set attributes
        indexN = dprov.fieldNameIndex('name') 
        indexA = dprov.fieldNameIndex('size') 
        poly.setAttributes([QgsDistanceArea().measurePolygon(coordinates), indexA])
        poly.setAttributes([description, indexN])

        # add feature                 
        dprov.addFeatures([poly])
        vlyr.updateExtents()

        #add layer  
            
        # iface.mapCanvas().refresh()
        vlyr.triggerRepaint()
        QgsMapLayerRegistry.instance().addMapLayers([vlyr])

        #delete list
        del coordinates[:]


myMapTool.canvasClicked.connect( mouseClick )
iface.mapCanvas().setMapTool( myMapTool )
