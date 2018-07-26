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
        icon_path = ':/plugins/GeomFilterEPSG/icon.png'
        self.action = QAction (QIcon (icon_path),u"filtro.", pai)
        self.action.setObjectName ("filtro.")
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

	self.vlyr = QgsVectorLayer("Polygon?crs=EPSG:31982", "temporary_polygons", "memory")
	self.dprov = self.vlyr.dataProvider()

		# Add field to virtual layer 
	self.dprov.addAttributes([QgsField("name", QVariant.String),
							QgsField("size", QVariant.Double)])

	self.vlyr.updateFields()

	self.myRubberBand = QgsRubberBand( iface.mapCanvas(), QGis.Polygon )
	self.color = QColor(78, 97, 114)
	self.color.setAlpha(190)
	self.myRubberBand.setColor(color)
				
		# Access MapTool  
	self.previousMapTool = iface.mapCanvas().mapTool()
	self.myMapTool = QgsMapToolEmitPoint( iface.mapCanvas() )

		# VALORES ANTES PASSADOS EM FORMA DE SCRIPT
	self.myMapTool.canvasClicked.connect( mouseClick )
	self.iface.mapCanvas().setMapTool( myMapTool )

		# create empty list to store coordinates 
	coordinates = []

		# Access ID 
	self.fields = self.dprov.fields() 

	def drawBand( currentPos, clickedButton ):
		self.iface.mapCanvas().xyCoordinates.connect( drawBand )

		if self.myRubberBand and self.myRubberBand.numberOfVertices():
			self.myRubberBand.removeLastPoint()
			self.myRubberBand.addPoint( QgsPoint(currentPos) )


	def mouseClick( currentPos, clickedButton ):
		if clickedButton == Qt.LeftButton:# and myRubberBand.numberOfVertices() == 0: 
			myRubberBand.addPoint( QgsPoint(currentPos) )
			
		elif clickedButton == Qt.RightButton and myRubberBand.numberOfVertices() > 3:

			# open input dialog     
			(description, False) = QInputDialog.getText(iface. mainWindow(), "Description", "Description for Polygon at x and y", QLineEdit.Normal, 'My Polygon') 

			#create feature and set geometry             
			poly = QgsFeature() 
			geomP = myRubberBand.asGeometry()
			poly.setGeometry(geomP) 
			
			print myRubberBand.numberOfVertices()

			#set attributes
			indexN = dprov.fieldNameIndex('name') 
			indexA = dprov.fieldNameIndex('size') 
			poly.setAttributes([QgsDistanceArea().measurePolygon(coordinates), indexA])
			poly.setAttributes([description, indexN])

			# add feature                 
			self.dprov.addFeatures([poly])
			self.vlyr.updateExtents()

			#add layer      
			self.vlyr.triggerRepaint()
			QgsMapLayerRegistry.instance().addMapLayers([vlyr])
			self.myRubberBand.reset(QGis.Polygon)

#myMapTool.canvasClicked.connect( mouseClick )
#iface.mapCanvas().setMapTool( myMapTool )


    

	
