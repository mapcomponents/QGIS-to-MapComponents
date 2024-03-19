import os
import json
from qgis.core import QgsProject, QgsLayerTree

class ProjectUtils:
    @classmethod
    def create_project_directory(self, project_name, outputFolder):
        """
            Create a project directory with a unique name based on the project name.
        """

        directory = f'{outputFolder}/{project_name}_MapComponentizer'

        # If the directory already exists, append a number to the project name
        counter = 1
        while os.path.exists(directory):
            project_name_with_counter = f'{project_name}_MapComponentizer_{counter}'
            directory = f'{outputFolder}/{project_name_with_counter}'
            counter += 1

        # Create the project directory        
        os.makedirs(directory, exist_ok=True)
        print(f'Directory "{directory}" created successfully.')
        os.mkdir(directory + "/public")
        exportFolder = directory + "/public/exported"
        os.mkdir(exportFolder)       

        return directory, exportFolder
    
    @classmethod
    def export_project_details(self, project: QgsProject, exportFolder: str):
        order = [layer.name() for layer in QgsLayerTree.layerOrder(project.layerTreeRoot())]        

        # Calculate the combined extent of all layers  
        config = {"order": order, "projectName": project.baseName()}
        with open(f'{exportFolder}/config.json', 'w') as file:
            file.write(json.dumps(config))