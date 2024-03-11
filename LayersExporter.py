import json
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsMapLayer, QgsCoordinateReferenceSystem, QgsJsonExporter, QgsProcessingFeedback
from .bridgestyle.qgis import layerStyleAsMapbox
from urllib.parse import urlparse, parse_qs

class LayersExporter:

    @classmethod
    def reproject_layers(self, project: QgsProject, temporalFolder: str):

        # list of layer names using list comprehension
        l = [layer.name() for layer in project.mapLayers().values()]
        # dictionary with key = layer name and value = layer object
        layers_list = {}
        for l in project.mapLayers().values():
            layers_list[l.name()] = l

        # loop the list looking for vector Layers with unsupported CRS:
        for l in layers_list:
            thisLayer: QgsMapLayer = layers_list[l]
            if thisLayer.type() == QgsMapLayerType.VectorLayer:
                if thisLayer.crs().authid() != 'EPSG:4326':

                    style_path = f'{temporalFolder}/{thisLayer.name()}.qml'
                    thisLayer.saveNamedStyle(style_path)
                   
                    # Reproject the layer
                    crs = QgsCoordinateReferenceSystem('EPSG:4326')
                    reprojected_path = f'{temporalFolder}/{thisLayer.name()}.gpkg'
                    QgsVectorFileWriter.writeAsVectorFormat(
                        thisLayer, reprojected_path, 'UTF-8', crs, 'GPKG')
                    project.removeMapLayer(thisLayer)
                    # Load the reprojected layer back into the project
                    reprojected_layer = QgsVectorLayer(
                    reprojected_path, f'{thisLayer.name()}', 'ogr')

                    reprojected_layer.loadNamedStyle(style_path)                    
                    project.addMapLayer(reprojected_layer)
                    

    @classmethod
    
    def export_layer(self, project: QgsProject, thisLayer: QgsMapLayer, outputFolder: str, feedback:  QgsProcessingFeedback):
        if thisLayer.type() == QgsMapLayerType.VectorLayer:                     
            # the new list is looped and the vector layer with supported geomtrie exported as geojson:
            if thisLayer.crs().authid() == 'EPSG:4326':
                                           
                                exporter = QgsJsonExporter(thisLayer)
                                features = thisLayer.getFeatures()                                    
                                geojson = exporter.exportFeatures(features)
                                name = thisLayer.name()                               
                                config = {"name": name,                                        
                                        "visible": self.is_layer_visible(project, thisLayer),
                                        "geomType": self.getVectorLayerType(geojson),
                                        "paint": json.loads(layerStyleAsMapbox(thisLayer)[0]),   
                                        "type": "geojson",
                                        "geojson": json.loads(geojson)                   
                                        }                          
                        
                                file = open(f'{outputFolder}/{name}.json', 'w')
                                file.write(json.dumps(config))
                                          
            
        
        elif thisLayer.type() == QgsMapLayerType.RasterLayer:
            # read wms layer infos and export them as a json object:        
                
                    source = thisLayer.source()
                    parsedUrl = urlparse('http://domain.de/?' + source)
                    url_parameters = parse_qs(parsedUrl.query)

                    new_url_parameters = {key: value[0]
                                        for key, value in url_parameters.items()}

                    name = thisLayer.name()

                    layers = []
                    # recover the original layers list from the url:
                    if 'layers' in url_parameters:
                        for layer in url_parameters['layers']:
                            #layers.append({'visible': True, "name": layer})
                            layers.append(layer)
                        new_url_parameters['layers'] = ", ".join(layers)

                    # if not new_url_parameters.get("name"):
                    #     new_url_parameters["name"] = name
                    

                    url = new_url_parameters["url"]
                    del new_url_parameters["url"]
                    new_url_parameters["transparent"] = "TRUE"


                    wmsLayer = {"urlParameters": new_url_parameters,
                            "url": url,
                            "name": name,
                            "attr": thisLayer.attribution(),
                            "title": thisLayer.title(),
                            "type": "wms"}
                    
                    json_string = json.dumps(wmsLayer)
                    with open(f'{outputFolder}/{name}.json', 'w') as file:
                        file.write(json_string)             
                
    
    @classmethod
    def is_layer_visible(self, project: QgsProject, layer: QgsMapLayer):
    #Checks if the layer is currently set visible in the layer tree.
        layer_tree_root = project.layerTreeRoot()
        layer = layer_tree_root.findLayer(layer)

        if layer is not None:
            return bool(layer.isVisible())
        else:    
            return True
    
    @classmethod
    def getVectorLayerType(self, geojson):
        try:
            jsonData = json.loads(geojson)
            geomType = jsonData["features"][0]["geometry"]["type"] 
            
            if geomType in ["Polygon", "MultiPolygon"]:
                return "fill"
            elif geomType in ["LineString", "MultiLineString"]:
                return "line"
            elif geomType == "Point":
                return "circle"
            else:
                return None 
        except:
            return "circle" 