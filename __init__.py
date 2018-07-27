# -*- coding: utf-8 -*-

def classFactory(iface):


    from .GeomFilterEPSG import GeomFilterEPSG
    return GeomFilterEPSG(iface)
