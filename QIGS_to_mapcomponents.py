import os
import subprocess
import shutil
from qgis.core import QgsApplication, QgsProject

from ProjectUtils import *
from LayersExporter import *



class MapComponentizer:

    BASE_OUTPUT_DIRECTORY = './output'
    TEMP_DIRECTORY = './tmp'
    TEMPLATE_PATH = './templates/MapComponentizer'
    QGIS_PREFIX_PATH = "/usr/lib/qgis"
    
    def main(self):

        # get Application path
        qgs = QgsApplication([], False)
        QgsApplication.setPrefixPath(self.QGIS_PREFIX_PATH, True)
        QgsApplication.initQgis()
        for alg in QgsApplication.processingRegistry().algorithms():
            print(alg.id(), "->", alg.displayName())
    
        # Get the project instance
        project = QgsProject.instance()
        
        # Print the current project file name (might be empty in case no projects have been loaded)
        print(project.fileName())

        # Load test project
        project.read('testdata/testProject.qgs')
        projectName = project.baseName()

        projectFolder, exportFolder = ProjectUtils.create_project_directory(projectName, self.BASE_OUTPUT_DIRECTORY)

        #export project details and layers
        ProjectUtils.export_project_details(project, exportFolder)
        LayersExporter.reproject_layers(self, project)
        LayersExporter.export_layers(project, exportFolder)
        
        
        #Create the MapComponents project using the selected template
        shutil.copytree(self.TEMPLATE_PATH, f'{projectFolder}', dirs_exist_ok=True)
        subprocess.run(["mv", "exported", "public" ], cwd=f'{projectFolder}')
               
        #Start dev Server in the new app 
        subprocess.run(['yarn'], cwd=f'{projectFolder}')
        
        # open dev server in the browser
        url = "http://localhost:5173/"        
        try:
            subprocess.run(['xdg-open', url], check=True)            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        # clear project and temp directory
        project.clear()
        qgs.exitQgis()

        shutil.rmtree(self.TEMP_DIRECTORY)
        os.mkdir(self.TEMP_DIRECTORY)

        subprocess.run(['yarn', 'dev'], cwd=f'{projectFolder}')     
    
map_componentizer = MapComponentizer()
map_componentizer.main()
