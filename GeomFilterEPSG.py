# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit, QAction, QIcon
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry, QgsField, QgsVectorLayer  
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool


class GeomFilterEPSG():
    

    def __init__(self, iface):
        self.iface = iface
		
    def initGui(self): 
		
        # cria uma ação que iniciará a configuração do plugin 
        self.initVariables()
        self.initSignals()

        
        self.iface.mapCanvas().setMapTool( self.myMapTool )

    def initVariables(self):
        self.coordinates = []

        # Criação da action e da toolbar
        self.toolbar = self.iface.addToolBar("My_ToolBar")
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/GeomFilterEPSG/icon.png'
        self.action = QAction (QIcon (icon_path),u"Filtro EPSG.", pai)
        self.action.setObjectName ("Filtro EPSG.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        
        self.vlyr = QgsVectorLayer("Polygon?crs=EPSG:31982", "temporary_polygons", "memory")
        self.dprov = self.vlyr.dataProvider()

        # Add field to virtual layer 
        self.dprov.addAttributes([QgsField("name", QVariant.String),
                            QgsField("size", QVariant.Double)])

        self.vlyr.updateFields()
        # Access ID 
        self.fields = self.dprov.fields()

    def initSignals(self):
        self.action.toggled.connect(self.initRubberBand)
        self.myMapTool.canvasClicked.connect( self.mouseClick )
        self.iface.mapCanvas().xyCoordinates.connect( self.mouseMove )

    def initRubberBand(self):
        self.myRubberBand = QgsRubberBand( self.iface.mapCanvas(), QGis.Polygon )
        color = QColor(78, 97, 114)
        color.setAlpha(190)
        self.myRubberBand.setColor(color)
        self.myRubberBand.setFillColor(QColor(255, 0, 0, 40))
        self.myRubberBand.setBorderColor(QColor(255, 0, 0, 200))
        # Access MapTool  
        self.previousMapTool = self.iface.mapCanvas().mapTool()
        self.myMapTool = QgsMapToolEmitPoint( self.iface.mapCanvas() )
        self.isEditing = 0

    def disconnect(self):

        self.iface.mapCanvas().unsetMapTool(self.myMapTool)
        self.iface.mapCanvas().xyCoordinates.disconnect (self.mouseMove)
        self.myRubberBand.reset()


    def unChecked(self):
        pass

    def unload(self):
        self.disconnect()

    def mouseClick( self, currentPos, clickedButton ):
        global isEditing
        if clickedButton == Qt.LeftButton:# and myRubberBand.numberOfVertices() == 0: 
            self.myRubberBand.addPoint( QgsPoint(currentPos) )
            self.coordinates.append( QgsPoint(currentPos) )
            isEditing = 1
            
        elif clickedButton == Qt.RightButton and self.myRubberBand.numberOfVertices() > 2:
            isEditing = 0
            
            # open input dialog     
            (description, False) = QInputDialog.getText(self.iface.mainWindow(), "Description", "Description for Polygon at x and y", QLineEdit.Normal, 'My Polygon') 

            #create feature and set geometry             
            poly = QgsFeature() 
            geomP = self.myRubberBand.asGeometry()
            poly.setGeometry(geomP) 
            print geomP.exportToWkt()
            
            #set attributes
            indexN = self.dprov.fieldNameIndex('name') 
            indexA = self.dprov.fieldNameIndex('size') 
            poly.setAttributes([QgsDistanceArea().measurePolygon(self.coordinates), indexA])
            poly.setAttributes([description, indexN])

            # add feature                 
            self.dprov.addFeatures([poly])
            self.vlyr.updateExtents()

            #add layer      
            self.vlyr.triggerRepaint()
            QgsMapLayerRegistry.instance().addMapLayers([self.vlyr])
            self.myRubberBand.reset(QGis.Polygon)

    def mouseMove( self, currentPos ):
        if self.isEditing == 1:
            self.myRubberBand.movePoint( QgsPoint(currentPos) )

# myMapTool.canvasClicked.connect( mouseClick )
# iface.mapCanvas().xyCoordinates.connect( mouseMove )

# iface.mapCanvas().setMapTool( myMapTool )

		
	