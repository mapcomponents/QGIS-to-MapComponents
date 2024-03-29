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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'WhereGroup GmbH'
__date__ = '2024-03-08'
__copyright__ = '(C) 2024 by WhereGroup GmbH'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MapComponentizer class from file MapComponentizer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mapcomponentizer import MapComponentizerPlugin    
    return MapComponentizerPlugin()
