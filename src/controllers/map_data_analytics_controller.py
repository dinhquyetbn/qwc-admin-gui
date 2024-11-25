import os

from flask import json

from .controller import Controller


class MapDataAnalyticsController(Controller):
    """Controller for user model"""

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(MapDataAnalyticsController, self).__init__(
            "Phân tích dữ liệu bản đồ",
            "map-data-analytics",
            "map-data-analytics",
            "map-data-analytics",
            app,
            handler,
        )

    def resources_for_index_query(self, search_text, session):
        """Return query for users list.

        :param str search_text: Search string for filtering
        :param Session session: DB session
        """
        query = session.query(self.User).order_by(self.User.name)
        if search_text:
            query = query.filter(self.User.name.ilike("%%%s%%" % search_text))

        return query