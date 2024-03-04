###TODO:
## create an index.json for each export folder (containing the nameof the files)


import os
import subprocess
from subprocess import PIPE
import shutil
   
import json
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter, QgsMapLayer, QgsLayerTree, QgsCoordinateReferenceSystem
import json
from urllib.parse import urlparse, parse_qs
from PyQt5.QtXml import *
from bridgestyle.qgis import layerStyleAsMapbox



class MapComponentizer():

    base_directory = './output'
    temp_directory = './tmp'
    templatePath = './templates/MapComponentizer'

    def main(self):

        # Get the project instance
        project = QgsProject.instance()
        
        # Print the current project file name (might be empty in case no projects have been loaded)
        print(project.fileName())

        # Load test project
        project.read('testdata/testProject.qgs')
        projectName = project.baseName()

        projectFolder, exportFolder = self.create_project_directory(projectName)

        self.export_project_details(project, exportFolder)
        self.reproject_layers(project)
        self.export_layers(project, exportFolder)
        
        
        #Create the MapComponents project using the selected template
        shutil.copytree(self.templatePath, f'{projectFolder}', dirs_exist_ok=True)
        subprocess.run(["mv", "exported", "public" ], cwd=f'{projectFolder}')
       
        #Start dev Server in the new app 
        subprocess.run(['yarn'], cwd=f'{projectFolder}')
        
        # open dev server in the browser
        url = "http://localhost:5173/"        
        try:
            subprocess.run(['xdg-open', url], check=True)            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        project.clear()
        shutil.rmtree(self.temp_directory)
        os.mkdir(self.temp_directory)

        subprocess.run(['yarn', 'dev'], cwd=f'{projectFolder}')     
        
         

    def reproject_layers(self, project: QgsProject):

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
                    reprojected_path = f'./tmp/{layers_list[l].name()}.gpkg'
                    QgsVectorFileWriter.writeAsVectorFormat(
                        layers_list[l], reprojected_path, 'UTF-8', crs, 'GPKG')

                    # Load the reprojected layer back into the project
                    reprojected_layer = QgsVectorLayer(
                        reprojected_path, f'{layers_list[l].name()}', 'ogr')
                    project.removeMapLayer(layers_list[l])
                    project.addMapLayer(reprojected_layer)

    def export_layers(self, project: QgsProject, outputFolder: str):

        # A new list is created, including the new reprojected layers:
        new_layers_list = {}
        for l in project.mapLayers().values():
            new_layers_list[l.name()] = l            
   

        for l in new_layers_list:
            thisLayer: QgsMapLayer = new_layers_list[l]
       
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
                              "paint": json.loads(self.get_Style(thisLayer)[0]),   
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
                    new_url_parameters['layers'] = layers

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
            
                

    def create_project_directory(self, project_name):

        directory = f'{self.base_directory}/{project_name}_MapComponentizer'

        # If the directory already exists, append a number to the project name
        counter = 1
        while os.path.exists(directory):
            project_name_with_counter = f'{project_name}_MapComponentizer_{counter}'
            directory = f'{self.base_directory}/{project_name_with_counter}'
            counter += 1

        # Create the project directory        
        os.mkdir(directory)
        print(f'Directory "{directory}" created successfully.')
        exportFolder = directory + "/exported"
        os.mkdir(exportFolder)       

        return directory, exportFolder
    
    def is_layer_visible(self, project: QgsProject, layer: QgsMapLayer):
    #Checks if the layer is currently set visible in the layer tree.
        layer_tree_root = project.layerTreeRoot()
        layer_tree_layer = layer_tree_root.findLayer(layer)
        return layer_tree_layer.isVisible()
    
    def getVectorLayerType(self, geojson):
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
    
    def export_project_details(self, project: QgsProject, exportFolder: str):
        order = [layer.name() for layer in QgsLayerTree.layerOrder(project.layerTreeRoot())]
        layers = project.mapLayers().values()

        # Calculate the combined extent of all layers
          

        config = {"order": order, "projectName": project.baseName()}

        with open(f'{exportFolder}/config.json', 'w') as file:
            file.write(json.dumps(config))

    def get_Style(self, layer: QgsMapLayer):
        inputFilePAth = f'{self.temp_directory}/{layer.name()}.qml'
        outputFilePath = f'{self.temp_directory}/{layer.name()}.json' 

        mapbox = layerStyleAsMapbox(layer)


        # document = QDomDocument()
        # layer.exportNamedStyle(document)
        # with open(inputFilePAth, 'w') as file:
        #             file.write(document.toString())
        # subprocess.run(['geostyler', '-s', 'qml', '-t', 'mapbox', inputFilePAth, outputFilePath ] ) 
# TODO: extract the result from the outputFilePath
        return mapbox    

map_componentizer = MapComponentizer()
map_componentizer.main()
