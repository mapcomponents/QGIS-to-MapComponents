# -*- coding: utf-8 -*-

"""
/***************************************************************************
 MapComponentizer
                                 A QGIS plugin
 Convert a QGIS project into a React Web Application
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-03-08
        copyright            : (C) 2024 by WhereGroup GmbH
        email                : info@wheregroup.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'WhereGroup GmbH'
__date__ = '2024-03-08'
__copyright__ = '(C) 2024 by WhereGroup GmbH'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import inspect
import os
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFolderDestination,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsProject
)
import subprocess
import shutil
from qgis.core import QgsApplication, QgsProject
from .ProjectUtils import *
from .LayersExporter import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
from qgis.PyQt.QtGui import QIcon



class MapComponentizerAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'
    TEMPLATE = 'TEMPLATE'
    plugin_path = os.path.dirname(os.path.realpath(__file__))
    templatesPath = f'{plugin_path}/templates'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm.
        """
        

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                self.tr('Output folder'),
                self.plugin_path + '/output'
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.TEMPLATE,
                self.tr('Create from template: '),
                options=self.get_folder_names(self.templatesPath),
                defaultValue=0,
                optional=False)
        )

    def processAlgorithm(self, parameters, context, feedback):

        # Send some information to the user
        feedback.pushInfo('Output folder is {}'.format(self.OUTPUT))
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        templateOptions = self.get_folder_names(self.templatesPath)

        BASE_OUTPUT_DIRECTORY = parameters[self.OUTPUT]
        TEMP_DIRECTORY = f'{plugin_path}/tmp'
        TEMPLATE_PATH = f'{plugin_path}/templates/{templateOptions[parameters[self.TEMPLATE]]}'
        #QGIS_PREFIX_PATH = "/usr/lib/qgis"

        # # get Application path
        # qgs = QgsApplication([], False)
        # QgsApplication.setPrefixPath(QGIS_PREFIX_PATH, True)
        # QgsApplication.initQgis()
        # for alg in QgsApplication.processingRegistry().algorithms():
        #     print(alg.id(), "->", alg.displayName())

        # Get the project instance
        project = QgsProject.instance()
        feedback.pushInfo(project.absolutePath())

        # Load test project
        # project.read(f'{plugin_path}/testdata/testProject.qgs')
        projectName = project.baseName()

        projectFolder, exportFolder = ProjectUtils.create_project_directory(
            projectName, BASE_OUTPUT_DIRECTORY)
        # export project details and layers
        ProjectUtils.export_project_details(project, exportFolder)
        LayersExporter.reproject_layers(project, TEMP_DIRECTORY)

        for layer in project.mapLayers().values():
            LayersExporter.export_layer(project, layer, exportFolder, feedback)

        # Create the MapComponents project using the selected template
        shutil.copytree(TEMPLATE_PATH, f'{projectFolder}', dirs_exist_ok=True)
        
        # Start dev Server in the new app
        ## only for stand-alone script
        
        #subprocess.run(['yarn'], cwd=f'{projectFolder}')
      
        # open dev server in the browser
        # url = "http://localhost:5173/"
        # try:
        #     subprocess.run(['xdg-open', url], check=True)
        # except subprocess.CalledProcessError as e:
        #     print(f"Error: {e}")

        # qgs.exitQgis()

        shutil.rmtree(TEMP_DIRECTORY)
        os.mkdir(TEMP_DIRECTORY)

        #subprocess.run(['yarn', 'dev'], cwd=f'{projectFolder}')

        return {self.OUTPUT: projectFolder}

    def name(self):

        return 'QGIS to MapComponents'

    def displayName(self):
        """
        Returns the translated algorithm name.
        """
        return self.tr(self.name())

    # Group Methods create a group inside the Provider folder in the toolbox
    # def group(self):
    #     return self.tr(self.groupId())

    # def groupId(self):
    #     return 'MapComponents'

    def shortHelpString(self):
        return self.tr("Make a React WebApp from your actual project and run it on a dev server")

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'logo.svg')))
        return icon
   
    def get_folder_names(self, directory_path):
        folder_names = [folder for folder in os.listdir(
            directory_path) if os.path.isdir(os.path.join(directory_path, folder))]
        return folder_names

    def createInstance(self):
        return MapComponentizerAlgorithm()
