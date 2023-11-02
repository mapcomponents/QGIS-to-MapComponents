from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter
from qgis.core import QgsCoordinateReferenceSystem


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

#print(layers_list)

for l in layers_list: 
    if layers_list[l].crs().authid() != 'EPSG:4326':
        print(layers_list[l].type())
        if layers_list[l].type() == QgsMapLayerType.VectorLayer:
            crs = QgsCoordinateReferenceSystem('EPSG:4326')
            reprojected_path = './testdata/test_reprojected.gpkg'
            QgsVectorFileWriter.writeAsVectorFormat(layers_list[l], reprojected_path, 'UTF-8', crs, 'GPKG')

            exporter = QgsJsonExporter(layers_list[l])
            features = layers_list[l].getFeatures()
            json = exporter.exportFeatures(features)
            name = layers_list[l].name()
            file = open(f'./output/{name}.json', 'w')
            file.write(json)
            
new_layer_list = {}
l = [layer.name() for layer in project.mapLayers().values()]
# dictionary with key = layer name and value = layer object

for l in project.mapLayers().values():
  new_layer_list [l.name()] = l