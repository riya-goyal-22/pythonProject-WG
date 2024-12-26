from app.handlers.donor_handler import DonorHandler
from fastapi import APIRouter, Request
from models.login import UserLogin
from models.signup import UserSignup


class DonorRoutes:
    def __init__(self, donor_handler: DonorHandler):
        self.handler = donor_handler
        self.router = APIRouter(tags=["donor"])

    def register_routes(self):
       @self.router.post("/signup")
       async def signup(user: UserSignup):
           return self.handler.create_donor(user)

       @self.router.post("/login")
       async def login(user: UserLogin):
           return self.handler.login(user)

       @self.router.get("/ngo/all")
       async def get_all_ngos():
           return self.handler.get_list_of_ngos()

       @self.router.get("/ngo/{ngo_id}")
       async def get_ngo_by_id(ngo_id: str):
           return self.handler.get_one_ngo(ngo_id)

       @self.router.get("/profile")
       async def get_profile(request:Request):
           return self.handler.get_profile(request)

       return self.router
