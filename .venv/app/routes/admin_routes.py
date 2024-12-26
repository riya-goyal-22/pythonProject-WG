from app.models.new_ngo import NewNGO
from fastapi import APIRouter, Request
from app.handlers.admin_handler import AdminHandler


class AdminRoutes:
    def __init__(self, admin_handler: AdminHandler):
        self.handler = admin_handler
        self.router = APIRouter(tags=["admin"])

    def register_routes(self):
        @self.router.post("/admin/ngo")
        async def create_NGO(ngo: NewNGO,request: Request):
            return self.handler.create_ngo(request=request, data=ngo)

        @self.router.put("/admin/ngo/{ngo_id}")
        async def update_NGO(ngo: NewNGO,ngo_id: str,request: Request):
            return self.handler.update_ngo(request=request, ngo_id=ngo_id, data=ngo)

        @self.router.delete("/admin/ngo/{ngo_id}")
        async def delete_NGO(ngo_id: str,request: Request):
            return self.handler.delete_ngo(request=request,ngo_id=ngo_id)

        return self.router
