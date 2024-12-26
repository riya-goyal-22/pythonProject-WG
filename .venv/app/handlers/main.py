from app.handlers.admin_handler import AdminHandler
from app.handlers.donor_handler import DonorHandler
from app.repositories.ngo_repository import NGORepository
from app.repositories.user_repository import UserRepository
from app.routes.donor_routes import DonorRoutes
from app.routes.admin_routes import AdminRoutes
from app.services.admin_service import AdminService
from app.services.donor_service import DonorService
from app.utils.db.db import DB_Instance
from app.utils.logger.logger import Logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import http_exception_handler
from middlewares.auth_middleware import AuthMiddleware
from middlewares.logger_middleware import LogMiddleware
from utils.errors.custom_errors import CustomHTTPException, custom_http_exception_handler


def create_app():
    logger = Logger()
    app = FastAPI(title='NGO Management')

    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)

    # Add logging middlewares
    app.add_middleware(AuthMiddleware)
    app.add_middleware(LogMiddleware,logger=logger)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    db = DB_Instance.get_connection()

    user_repo = UserRepository(db)
    ngo_repo = NGORepository(db)

    donor_service = DonorService(user_repo, ngo_repo)
    admin_service = AdminService(user_repo, ngo_repo)

    donor_handler = DonorHandler(donor_service)
    admin_handler = AdminHandler(admin_service)

    # include routers
    app.include_router(DonorRoutes(donor_handler).register_routes())
    app.include_router(AdminRoutes(admin_handler).register_routes())

    return app


if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=5000)
