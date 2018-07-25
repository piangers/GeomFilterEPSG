# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QColor, QInputDialog, QLineEdit
from qgis.core import QGis, QgsMapLayerRegistry, QgsDistanceArea, QgsFeature, QgsPoint, QgsGeometry
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool


class GeomFilterEPSG():
    

	def __init__(self, iface):
        
        self.iface = iface
        
    def initGui(self): 

        self.toolbar = self.iface.addToolBar("My_ToolBar")
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/MeasureArea/icon.png'
        self.action = QAction (QIcon (icon_path),u"Calcula em metros quadrados, tamanho da area ou areas.", pai)
        self.action.setObjectName ("Retorna a area do poligono.")
        self.action.setStatusTip(None)
        self.action.setWhatsThis(None)
        self.action.setCheckable(True)
        #Padrões fixados
        self.textbox = QLineEdit(self.iface.mainWindow())
        # Set width
        self.textbox.setFixedWidth(120)
        # Add textbox to toolbar
        self.toolbar.addAction(self.action)
        self.toolbar.addWidget(self.textbox)
        # Set tooltip
        self.action.toggled.connect(self.enableElements)
        self.enableElements(False)
        self.textbox.textChanged.connect(self.enableTool) # acho que é aqui o sinal a ser trabalhado
        self.action.toggled.connect(self.enableTool)                                           
  
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
