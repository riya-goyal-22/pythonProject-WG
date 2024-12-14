from app.handlers.admin_handler import AdminHandler
from app.handlers.donor_handler import DonorHandler
from app.middlewares.auth_middleware import auth_middleware
from app.middlewares.logger_middleware import log_request_middleware, log_response_middleware, log_exceptions
from app.repositories.ngo_repository import NGORepository
from app.repositories.user_repository import UserRepository
from app.routes.donor_routes import DonorRoutes
from app.routes.admin_routes import AdminRoutes
from app.services.admin_service import AdminService
from app.services.donor_service import DonorService
from app.utils.db.db import DB_Instance
from app.utils.logger.logger import Logger
from flask import Flask


def create_app():
    logger = Logger()
    app = Flask(__name__)
    app.before_request(auth_middleware)

    @app.before_request
    def before_request():
        log_request_middleware(logger)

    @app.after_request
    def after_request(response):
        return log_response_middleware(logger, response)

    @app.errorhandler(Exception)
    def handle_exceptions(e: Exception):
        return log_exceptions(logger, e)

    db = DB_Instance.get_connection()

    user_repo = UserRepository(db)
    ngo_repo = NGORepository(db)

    donor_service = DonorService(user_repo, ngo_repo)
    admin_service = AdminService(user_repo, ngo_repo)

    donor_handler = DonorHandler(donor_service)
    admin_handler = AdminHandler(admin_service)

    # Register blueprints
    app.register_blueprint(
        DonorRoutes(donor_handler).register_routes(),
        url_prefix='/user'
    )

    app.register_blueprint(
        AdminRoutes(admin_handler).register_routes(),
        url_prefix='/admin'
    )

    @app.route('/')
    def index():
        return "Everything's working great"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
