from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.ngo_repository import NGORepository
import app.utils.utilities.encrypter as encrypter
from app.services.user_service import UserService
from app.models.ngo import NGO
from app.utils.errors.custom_errors import NGOExistsError


class AdminService(UserService):
    def __init__(self,user_repo:UserRepository,ngo_repo:NGORepository):
        super().__init__(user_repo,ngo_repo)

    def add_ngo(self,ngo:NGO):
        if self.ngo_repo.get_ngo_by_email(ngo.email) is not None:
            raise NGOExistsError("ngo already registered with this email id")
        self.ngo_repo.create_ngo(ngo)

    def update_ngo(self,ngo:NGO):
        self.ngo_repo.update_ngo_by_id(ngo)

    def delete_ngo(self,id: str):
        self.ngo_repo.delete_ngo_by_id(id)
