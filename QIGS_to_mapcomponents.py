from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter, QgsProviderRegistry
from qgis.core import QgsCoordinateReferenceSystem
import json


# Get the project instance
project = QgsProject.instance()
# Print the current project file name (might be empty in case no projects have been loaded)
# print(project.fileName())

# Load external project
project.read('testdata/test1.qgs')

# list of layer names using list comprehension
l = [layer.name() for layer in project.mapLayers().values()]
# dictionary with key = layer name and value = layer object
layers_list = {}
for l in project.mapLayers().values():
  layers_list[l.name()] = l


# loop the list looking for vector Layers with unsupported CRS:
for l in layers_list: 
  
  if layers_list[l].type() == QgsMapLayerType.VectorLayer:
    if layers_list[l].crs().authid() != 'EPSG:4326': 
        
          # Reproject the layer
            crs = QgsCoordinateReferenceSystem('EPSG:4326')
            reprojected_path = f'./testdata/{layers_list[l].name()}_reprojected.gpkg'
            QgsVectorFileWriter.writeAsVectorFormat(layers_list[l], reprojected_path, 'UTF-8', crs, 'GPKG')

           # Load the reprojected layer back into the project
            reprojected_layer = QgsVectorLayer(reprojected_path, f'{layers_list[l].name()}_reprojected', 'ogr')
            project.addMapLayer(reprojected_layer)

# A new list is created, including the new reprojected layers:
new_layers_list = {}
for l in project.mapLayers().values():
  new_layers_list[l.name()] = l

# the new list is looped and the vector layer with supported geomtrie exported as geojson:
for l in new_layers_list: 
  thisLayer = new_layers_list[l]
  if thisLayer.type() == QgsMapLayerType.VectorLayer:
    if thisLayer.crs().authid() == 'EPSG:4326':
      
        exporter = QgsJsonExporter(thisLayer)
        features = thisLayer.getFeatures()
        geojson = exporter.exportFeatures(features)
        name = thisLayer.name()
        file = open(f'./output/{name}.json', 'w')
        file.write(geojson)    
  
  elif thisLayer.type() == QgsMapLayerType.RasterLayer:
    print(f"hi there, im {thisLayer.name()}, a {thisLayer.type()} Layer") 
    source = thisLayer.source()
    name = thisLayer.name()
    data = {'source': source, 'type': 'wms'}
    json_string = json.dumps(data)
    with open(f'./output/{name}.json', 'w') as file:
      file.write(json_string) 
