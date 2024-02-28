###TODO:
## create an index.json for each export folder (containing the nameof the files)


import os
import subprocess
from subprocess import PIPE, Popen
import shutil
   
import json
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter, QgsMapLayer
from qgis.core import QgsCoordinateReferenceSystem
import json
from urllib.parse import urlparse, parse_qs


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

        self.reproject_layers(project)
        self.export_layers(project, exportFolder)

        webAppName = projectName + '_mapComponents'
        #subprocess.run(['npx', 'degit', 'mapcomponents/template', webAppName], cwd=projectFolder)
    
        shutil.copytree(self.templatePath, f'{projectFolder}', dirs_exist_ok=True)
        #subprocess.run(['mv', 'exported'], cwd=f'{projectFolder}')

        #Start dev Server in the new app       
        
        subprocess.run(['yarn'], cwd=f'{projectFolder}')
        #install.wait() 
        
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
                    reprojected_path = f'./tmp/{layers_list[l].name()}(4326).gpkg'
                    QgsVectorFileWriter.writeAsVectorFormat(
                        layers_list[l], reprojected_path, 'UTF-8', crs, 'GPKG')

                    # Load the reprojected layer back into the project
                    reprojected_layer = QgsVectorLayer(
                        reprojected_path, f'{layers_list[l].name()}(4326)', 'ogr')
                    project.addMapLayer(reprojected_layer)

    def export_layers(self, project: QgsProject, outputFolder: str):
        # A new list is created, including the new reprojected layers:
        new_layers_list = {}
        for l in project.mapLayers().values():
            new_layers_list[l.name()] = l              
        vectorIndex = []
        wmsIndex = []
        wmsFolder = f'{outputFolder}/wms'
        geosjonFolder = f'{outputFolder}/geojson'

        for l in new_layers_list:
            thisLayer: QgsMapLayer = new_layers_list[l]
       
            if thisLayer.type() == QgsMapLayerType.VectorLayer:
        # the new list is looped and the vector layer with supported geomtrie exported as geojson:
                if thisLayer.crs().authid() == 'EPSG:4326':
                    if not os.path.isdir(geosjonFolder):
                        os.mkdir(geosjonFolder)
                    
                    exporter = QgsJsonExporter(thisLayer)
                    features = thisLayer.getFeatures()
                    geojson = exporter.exportFeatures(features)
                    name = thisLayer.name()
                    config = {"name": name,
                              "visible": self.is_layer_visible(project, thisLayer),
                              "type": self.getVectorLayerType(geojson),
                              "geojson": json.loads(geojson)                                                    
                              }
                    
                    file = open(f'{geosjonFolder}/{name}.json', 'w')
                    file.write(json.dumps(config))
                    vectorIndex.append(f'{name}.json')
         
       
            elif thisLayer.type() == QgsMapLayerType.RasterLayer:
         # read wms layer infos and export them as a json object:        
                if not os.path.isdir(wmsFolder):
                        os.mkdir(wmsFolder)
                source = thisLayer.source()
                parsedUrl = urlparse('http://domain.de/?' + source)
                url_parameters = parse_qs(parsedUrl.query)

                new_url_parameters = {key: value[0]
                                      for key, value in url_parameters.items()}

                name = thisLayer.name()
                layers = []

                # recover the original layers list from th url:
                if 'layers' in url_parameters:
                    for layer in url_parameters['layers']:
                        layers.append({'visible': True, name: layer})
                    new_url_parameters['layers'] = layers

                json_string = json.dumps(new_url_parameters)
                with open(f'{wmsFolder}/{name}.json', 'w') as file:
                    file.write(json_string)
                wmsIndex.append(f'{name}.json')

        # export the index lists for each type of layer:
        
        with open(f'{wmsFolder}/index.json', 'w') as file:
            file.write(json.dumps(wmsIndex))
        with open(f'{geosjonFolder}/index.json', 'w') as file:
            file.write(json.dumps(vectorIndex))


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

map_componentizer = MapComponentizer()
map_componentizer.main()
