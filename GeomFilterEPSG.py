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
        #self.myMapTool = QgsMapToolEmitPoint( self.iface.mapCanvas() )
        self.initVariables()
        self.initSignals()
        
        
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
        self.toolbar.addAction(self.action)

        self.previousMapTool = self.iface.mapCanvas().mapTool()
        self.myMapTool = QgsMapToolEmitPoint( self.iface.mapCanvas() )
        self.isEditing = 0
       

    def initSignals(self):
        self.action.toggled.connect(self.RubberBand)
        self.myMapTool.canvasClicked.connect( self.mouseClick )

    def RubberBand(self, bolean):
        if bolean:
            self.myRubberBand = QgsRubberBand( self.iface.mapCanvas(), QGis.Polygon )
            color = QColor(78, 97, 114)
            color.setAlpha(190)
            self.myRubberBand.setColor(color)
            self.myRubberBand.setFillColor(QColor(255, 0, 0, 40))
            self.myRubberBand.setBorderColor(QColor(255, 0, 0, 200))
            
            # Set MapTool
            self.iface.mapCanvas().setMapTool( self.myMapTool )
            self.iface.mapCanvas().xyCoordinates.connect( self.mouseMove )
        else:
            self.disconnect()

    def disconnect(self):

        self.iface.mapCanvas().unsetMapTool(self.myMapTool)
        try:
            self.iface.mapCanvas().xyCoordinates.disconnect (self.mouseMove)
        except:
            pass

        try:
            self.myRubberBand.reset()
        except:
            pass

    def unChecked(self):
        pass

    def unload(self):
        self.disconnect()        

    def mouseClick( self, currentPos, clickedButton ):
        if clickedButton == Qt.LeftButton:# and myRubberBand.numberOfVertices() == 0: 
            self.myRubberBand.addPoint( QgsPoint(currentPos) )
            self.coordinates.append( QgsPoint(currentPos) )
            self.isEditing = 1
            
        elif clickedButton == Qt.RightButton and self.myRubberBand.numberOfVertices() > 2:
            self.isEditing = 0
            
            # open input dialog     
            #(description, False) = QInputDialog.getText(self.iface.mainWindow(), "Description:", "For Polygon", QLineEdit.Normal, 'Polygon') 

            #create feature and set geometry             
            poly = QgsFeature() 
            geomP = self.myRubberBand.asGeometry()
            poly.setGeometry(geomP)
            g=geomP.exportToWkt()
            #print g
            canvas=self.iface.mapCanvas()
            c=canvas.mapRenderer().destinationCrs().authid()
            rep = c.replace("EPSG:","")
            print "\n"
            
            string = U"st_intersects(geom,st_geomfromewkt('SRID="+rep+";"+g+"'))"
            print string
           
            self.layers = self.iface.mapCanvas().layers()
            
            for layer in self.layers:
                layer.setSubsetString(string)
            
            # layers = iface.mapCanvas().layers()
            # for layer in layers:
            #    layer.setSubsetString('"Art" = \'Ki\'')
            
           

            self.myRubberBand.reset(QGis.Polygon)

    def mouseMove( self, currentPos ):
        if self.isEditing == 1:
            self.myRubberBand.movePoint( QgsPoint(currentPos) )



		
	