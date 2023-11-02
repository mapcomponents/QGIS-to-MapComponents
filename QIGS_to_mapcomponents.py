from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter, QgsCoordinateTransformContext
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

print(layers_list)

for l in layers_list: 
    if layers_list[l].type() == QgsMapLayerType.VectorLayer:
        if layers_list[l].crs().authid() != 'EPSG:4326':

            targetCRS = QgsCoordinateReferenceSystem('EPSG:4326')         
            reprojected_path = './testdata/test_reprojected.gpkg'
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.fileEncoding = 'UTF-8'
            options.driverName = 'GPKG'
            options.layerOptions = ["PRECISION=NO"]
            context = QgsCoordinateTransformContext()
            context.addCoordinateOperation(layers_list[l].crs(), targetCRS, "Transformed to EPSG:4362", True )
            QgsVectorFileWriter.writeAsVectorFormatV3(layers_list[l], reprojected_path, context, options)

            # Load the reprojected layer back into the project
            reprojected_layer = QgsVectorLayer(reprojected_path, layers_list[l].name(), 'ogr')
            QgsProject.instance().addMapLayer(reprojected_layer)

            exporter = QgsJsonExporter(layers_list[l])
            features = layers_list[l].getFeatures()
            json = exporter.exportFeatures(features)
            name = layers_list[l].name()
            file = open(f'./output/{name}.json', 'w')
            file.write(json)

    if layers_list[l].type() == QgsMapLayerType.RasterLayer:
        # Do raster Layer stuff
        print("im a raster layer")

    
            
new_layer_list = {}
l = [layer.name() for layer in project.mapLayers().values()]
# dictionary with key = layer name and value = layer object

for l in project.mapLayers().values():
  new_layer_list [l.name()] = l