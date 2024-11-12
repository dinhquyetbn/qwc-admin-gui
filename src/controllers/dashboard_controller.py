import os

from flask import json

from .controller import Controller

class DashboardController(Controller):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(DashboardController, self).__init__(
            "Dashboard", 'dashboard', 'dashboard', 'dashboard', app, handler
        )