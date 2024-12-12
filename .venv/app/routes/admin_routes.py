from flask import Blueprint
from app.handlers.admin_handler import AdminHandler

class AdminRoutes:
    def __init__(self,admin_handler: AdminHandler):
        self.handler = admin_handler
        self.blueprint = Blueprint('admin',__name__)

    def register_routes(self):
        self.blueprint.add_url_rule(
            '/ngo',
            'create_ngo',
            self.handler.create_ngo,
            methods=['POST']
        )
        self.blueprint.add_url_rule(
            '/ngo/<ngo_id>',
            'update_ngo',
            self.handler.update_ngo,
            methods=['PUT']
        )
        self.blueprint.add_url_rule(
            '/ngo/<ngo_id>',
            'delete_ngo',
            self.handler.delete_ngo,
            methods=['DELETE']
        )
        return self.blueprint