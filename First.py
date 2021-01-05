from qgis import processing
infeature = '/Users/dj/Documents/QGIS/Shapefile/Russia/Moscow_stations_15_copy2.shp'
#infeature = '/Users/dj/Documents/QGIS/Shapefile/World/worldwide_stations_projected.shp'

#Firtst, make sure stations are in right coordinate system
result = processing.runAndLoadResults("qgis:reprojectlayer",
{'INPUT': infeature,
 'TARGET_CRS': 'epsg:3035',
 'OUTPUT': 'memory:Reprojectedpolyline'
})

#Create Delaunay Triangle
result = processing.runAndLoadResults("qgis:delaunaytriangulation",
{'INPUT': result['OUTPUT'],
 'OUTPUT': 'memory:DelaunayTriangle'
})

result = processing.runAndLoadResults("qgis:polygonstolines",
{'INPUT': result['OUTPUT'],
 'OUTPUT': 'memory:polyline'
})

result = processing.runAndLoadResults("qgis:explodelines",
{'INPUT': result['OUTPUT'],
 'OUTPUT': 'memory:explodepolylines'
})

result = processing.runAndLoadResults("qgis:deleteduplicategeometries",
{'INPUT': result['OUTPUT'],
 'OUTPUT': 'memory:cleanpolylines'
})

'''
result = processing.runAndLoadResults("qgis:reprojectlayer",
{'INPUT': result['OUTPUT'],
 'TARGET_CRS': 'epsg:2448',
 'OUTPUT': 'memory:Reprojectedpolyline'
})
'''

#Network output, not temporary layer
Network = '/Users/dj/Documents/QGIS/Shapefile/Russia/Moscow_stations_15_network_update2.shp'
processing.runAndLoadResults("qgis:exportaddgeometrycolumns",
{'INPUT': result['OUTPUT'],
 'CALC_METHOD': 0,
 'OUTPUT': Network
})

'''

#Create cover area
Selected = processing.runAndLoadResults("qgis:extractbyexpression",
{'INPUT': Network,
 'EXPRESSION':'"length"<30000',
 'OUTPUT': 'memory: selectedfeature'
})

templayer = processing.runAndLoadResults("qgis:polygonize",
{'INPUT': Selected['OUTPUT'],
 'OUTPUT': 'memory: Polygon'
})

dissolvelayer = processing.runAndLoadResults("qgis:dissolve",
{'INPUT': templayer['OUTPUT'],
 'OUTPUT': 'memory: dissolvePolygon'
})

intersection = processing.runAndLoadResults("qgis:intersection",
{'INPUT': dissolvelayer['OUTPUT'],
 'OVERLAY': countryboundary,
 'OUTPUT': 'memory: intersectedPolygon'
})

polygongeo = processing.runAndLoadResults("qgis:exportaddgeometrycolumns",
{'INPUT': intersection['OUTPUT'],
 'CALC_METHOD': 0,
 'OUTPUT': 'memory: polygongeo'
})
#print(result)




'''