from datetime import datetime, timezone
import os
import uuid
from flask import json, jsonify, request

from .controller_v2 import ControllerV2


class UploadFileController(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(UploadFileController, self).__init__(
            "Upload file",
            "upload-file",
            "upload-file",
            "upload-file",
            app,
            handler,
        )

    def upload_file_multiple(self, files):
        pass

    def get_file_multiple(self, ids):
        print(ids)

    def remove_file_multiple(self, ids):
        pass
