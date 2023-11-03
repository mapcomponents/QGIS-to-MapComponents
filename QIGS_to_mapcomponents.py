from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter, QgsProviderRegistry
from qgis.core import QgsCoordinateReferenceSystem
import json
from urllib.parse import urlparse, parse_qs


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
   
    source = thisLayer.source()
    parsedUrl = urlparse('http://domain.de/?' + source)
    url_parameters = parse_qs(parsedUrl.query)

    print(url_parameters)
    name = thisLayer.name()
    layers = []
    if 'layers' in  url_parameters: 
      for layer in url_parameters['layers'] :
       layers.append({'visible': True , name: layer})

    data = {'layerType': 'wms', 'wmsUrl': url_parameters['url'][0][0], 'layers': layers, 'crs': url_parameters['crs'][0]}
    if 'type' in  url_parameters: 
    
      data['type'] = url_parameters['type'][0]

    if 'zmin' in  url_parameters: 
     data['minZoom'] = url_parameters['zmin'][0]

    if 'zmax' in  url_parameters: 
     data['maxZoom'] = url_parameters['zmax'][0]

    json_string = json.dumps(url_parameters)
    with open(f'./output/{name}.json', 'w') as file:
      file.write(json_string) 
