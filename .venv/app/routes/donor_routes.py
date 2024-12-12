from app.handlers.donor_handler import DonorHandler
from flask import Blueprint


class DonorRoutes:
    def __init__(self,donor_handler: DonorHandler):
        self.handler = donor_handler

    def register_routes(self):
        self.blueprint = Blueprint('donor_routes', __name__)
        self.blueprint.add_url_rule(
            '/signup',
            'signup',
            self.handler.create_donor,
            methods=['POST']
        )
        self.blueprint.add_url_rule(
            '/login',
            'login',
            self.handler.login,
            methods=['POST']
        )
        self.blueprint.add_url_rule(
            '/ngo/all',
            'all_ngos',
            self.handler.get_list_of_ngos,
            methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/ngo/<ngo_id>',
            'ngo_by_id',
            self.handler.get_one_ngo,
            methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/profile',
            'profile',
            self.handler.get_profile,
            methods=['GET']
        )
        return self.blueprint