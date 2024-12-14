from dataclasses import dataclass


@dataclass
class UserSignup:
    name: str
    address: str
    phone_no: str
    email: str
    password: str

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'phone_no': self.phone_no
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
