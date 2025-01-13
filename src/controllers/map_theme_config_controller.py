# import sys
# import os

# # Path to the QGIS installation
# # qgis_path = '/usr/share/qgis/python'
# qgis_path = '/usr/lib/python3/dist-packages'

# # Append QGIS Python directory to the system path
# sys.path.append(qgis_path)

# # Set environment variables if needed
# os.environ['QGIS_PREFIX_PATH'] = '/usr'
# os.environ['QGIS_PATH'] = '/usr'
# # Add the QGIS Python bindings path
# os.environ['PYTHONPATH'] = qgis_path + ':' + os.environ.get('PYTHONPATH', '')

# from qgis.core import (
#     QgsProject,
#     QgsVectorLayer,
#     QgsRasterLayer,
#     QgsApplication
# )

import uuid
from datetime import datetime, timezone
from flask import json, jsonify, request
from .controller_v2 import ControllerV2

class MapThemeConfigController(ControllerV2):
    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(MapThemeConfigController, self).__init__(
            "Thiết lập giao diện",
            "theme-config",
            "theme-config",
            "map_theme_config",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        pass