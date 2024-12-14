from dataclasses import dataclass


@dataclass
class UserLogin:
    email: str
    password: str

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
