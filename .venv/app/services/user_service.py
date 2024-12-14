from app.repositories.user_repository import UserRepository
from app.repositories.ngo_repository import NGORepository
from app.utils.errors.custom_errors import InvalidCredentialsError
import app.utils.utilities.encrypter as encrypter
import app.utils.utilities.token as token


class UserService:
    def __init__(self, user_repo: UserRepository, ngo_repo: NGORepository):
        self.user_repo = user_repo
        self.ngo_repo = ngo_repo

    def login(self, email: str, password: str):
        user = self.user_repo.get_user_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Invalid Email Id")
        else:
            if not encrypter.check_password(user.password, password):
                raise InvalidCredentialsError("Invalid password")
            else:
                return token.generate_token(user.id, user.email, user.role)

    def get_all_ngos(self):
        ngos = self.ngo_repo.get_all_ngos()
        return ngos

    def get_ngo_by_id(self, id: str):
        ngo = self.ngo_repo.get_ngo_by_id(id)
        return ngo

    def get_profile(self, id: str):
        user = self.user_repo.get_user_by_id(id)
        return user
