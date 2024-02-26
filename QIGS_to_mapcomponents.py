import os
import subprocess
import webbrowser
from qgis.core import QgsProject, QgsVectorFileWriter, QgsVectorLayer, QgsMapLayerType, QgsJsonExporter
from qgis.core import QgsCoordinateReferenceSystem
import json
from urllib.parse import urlparse, parse_qs


class MapComponentizer():

    base_directory = './output'
    temp_directory = './temp'

    def main(self):
        
        # Get the project instance
        project = QgsProject.instance()

        # Print the current project file name (might be empty in case no projects have been loaded)
        #print(project.fileName())
         
        # Load test project
        project.read('testdata/testProject.qgs')
        projectName = project.baseName()

        outputFolder = self.create_project_directory(projectName)

        self.reproject_layers(project)
        self.export_layers(project, outputFolder)

        workingPath = os.path.dirname(os.path.realpath(__file__))
        subprocess.run(['npx', 'degit', 'mapcomponents/template', projectName], cwd=outputFolder)
        subprocess.run(['yarn'], cwd=f'{outputFolder}/{projectName}')
        subprocess.run(['yarn', 'dev'], cwd=f'{outputFolder}/{projectName}')
        webbrowser.open("http://localhost:5173", new=2)

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
                    reprojected_path = f'./tmp/{layers_list[l].name()}_reprojected.gpkg'
                    QgsVectorFileWriter.writeAsVectorFormat(
                        layers_list[l], reprojected_path, 'UTF-8', crs, 'GPKG')

                    # Load the reprojected layer back into the project
                    reprojected_layer = QgsVectorLayer(
                        reprojected_path, f'{layers_list[l].name()}_reprojected', 'ogr')
                    project.addMapLayer(reprojected_layer)

    def export_layers(self, project: QgsProject, outputFolder: str):
        # A new list is created, including the new reprojected layers:
        new_layers_list = {}
        for l in project.mapLayers().values():
            new_layers_list[l.name()] = l

        for l in new_layers_list:
            thisLayer = new_layers_list[l]
        # the new list is looped and the vector layer with supported geomtrie exported as geojson:
            if thisLayer.type() == QgsMapLayerType.VectorLayer:
                if thisLayer.crs().authid() == 'EPSG:4326':

                    exporter = QgsJsonExporter(thisLayer)
                    features = thisLayer.getFeatures()
                    geojson = exporter.exportFeatures(features)
                    name = thisLayer.name()
                    file = open(f'{outputFolder}/{name}.json', 'w')
                    file.write(geojson)

            # read wms layer infos and export them as a json object:
            elif thisLayer.type() == QgsMapLayerType.RasterLayer:

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
                with open(f'{outputFolder}/{name}.json', 'w') as file:
                    file.write(json_string)

    def create_project_directory(self, project_name):

        directory = f'{self.base_directory}/{project_name}'

        # If the directory already exists, append a number to the project name
        counter = 1
        while os.path.exists(directory):
            project_name_with_counter = f'{project_name}_{counter}'
            directory = f'{self.base_directory}/{project_name_with_counter}'
            counter += 1

            # Create the project directory
        os.mkdir(directory)
        print(f'Directory "{directory}" created successfully.')

        return directory


map_componentizer = MapComponentizer()
map_componentizer.main()
