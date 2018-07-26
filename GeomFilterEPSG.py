# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry, QgsField, QgsVectorLayer  
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool


class GeomFilterEPSG():
    

	def __init__(self, iface):
		self.iface = iface
		
	def initGui(self): 
		
		self.toolbar = self.iface.addToolBar("My_ToolBar")
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/GeomFilterEPSG/icon.png'
        self.action = QAction (QIcon (icon_path),u"filtro.", pai)
        self.action.setObjectName ("filtro.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        #Padrões fixados
        
        # Add textbox to toolbar
        self.toolbar.addAction(self.action)

        self.action.toggled.connect(self.enableElements)
        self.enableElements(False)
		




	vlyr = QgsVectorLayer("Polygon?crs=EPSG:31982", "temporary_polygons", "memory")
	dprov = vlyr.dataProvider()

	# Add field to virtual layer 
	dprov.addAttributes([QgsField("name", QVariant.String),
						QgsField("size", QVariant.Double)])

	vlyr.updateFields()

	myRubberBand = QgsRubberBand( self.iface.mapCanvas(), QGis.Polygon )
	color = QColor(78, 97, 114)
	color.setAlpha(190)
	myRubberBand.setColor(color)
	myRubberBand.setFillColor(QColor(255, 0, 0, 40))
	myRubberBand.setBorderColor(QColor(255, 0, 0, 200))
	# Access MapTool  
	previousMapTool = self.iface.mapCanvas().mapTool()
	myMapTool = QgsMapToolEmitPoint( self.iface.mapCanvas() )
	isEditing = 0
	# create empty list to store coordinates 
	coordinates = []
	# Access ID 
	fields = dprov.fields() 


def disconect(self):

	self.iface.mapCanvas().unsetMapTool(self.myMapTool)
	self.iface.mapCanvas().xyCoordinates.disconnect (mouseMove)
	self.myRubberBand.reset()


def unChecked(self):
	pass

def unload(self):
	pass


def drawBand( currentPos, clickedButton ):
    self.iface.mapCanvas().xyCoordinates.connect( drawBand )

    if myRubberBand and myRubberBand.numberOfVertices():
        myRubberBand.removeLastPoint()
        myRubberBand.addPoint( QgsPoint(currentPos) )


def mouseClick( currentPos, clickedButton ):
    global isEditing
    if clickedButton == Qt.LeftButton:# and myRubberBand.numberOfVertices() == 0: 
        myRubberBand.addPoint( QgsPoint(currentPos) )
        isEditing = 1
        
    elif clickedButton == Qt.RightButton and myRubberBand.numberOfVertices() > 2:
        isEditing = 0
        
        # open input dialog     
        (description, False) = QInputDialog.getText(iface. mainWindow(), "Description", "Description for Polygon at x and y", QLineEdit.Normal, 'My Polygon') 

        #create feature and set geometry             
        poly = QgsFeature() 
        geomP = myRubberBand.asGeometry()
        poly.setGeometry(geomP) 
        print geomP.exportToWkt()
        
        #set attributes
        indexN = dprov.fieldNameIndex('name') 
        indexA = dprov.fieldNameIndex('size') 
        poly.setAttributes([QgsDistanceArea().measurePolygon(coordinates), indexA])
        poly.setAttributes([description, indexN])

        # add feature                 
        dprov.addFeatures([poly])
        vlyr.updateExtents()

        #add layer      
        vlyr.triggerRepaint()
        QgsMapLayerRegistry.instance().addMapLayers([vlyr])
        myRubberBand.reset(QGis.Polygon)

def mouseMove( currentPos ):
    global isEditing
    if isEditing == 1:
        myRubberBand.movePoint( QgsPoint(currentPos) )

# myMapTool.canvasClicked.connect( mouseClick )
# iface.mapCanvas().xyCoordinates.connect( mouseMove )

# iface.mapCanvas().setMapTool( myMapTool )

		
	