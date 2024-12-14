import uuid
from app.utils.enums.role import Role


class User:
    def __init__(self, name: str, email: str, password: str, phone_no: str, address: str, id: str = None,
                 role: str = Role.DONOR.value):
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.address = address
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone_no": self.phone_no,
            "address": self.address,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
