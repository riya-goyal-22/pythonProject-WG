from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.ngo_repository import NGORepository
from app.utils.errors.custom_errors import UserExistsError
import app.utils.utilities.encrypter as encrypter
from app.services.user_service import UserService


class DonorService(UserService):
    def __init__(self, user_repo: UserRepository, ngo_repo: NGORepository):
        super().__init__(user_repo, ngo_repo)

    def signup(self, user: User):
        if self.user_repo.get_user_by_email(user.email) is not None:
            raise UserExistsError(user.email)

        user.password = encrypter.hash_password(user.password)
        self.user_repo.create_user(user)
        return user
