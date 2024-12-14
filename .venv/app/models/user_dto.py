from dataclasses import dataclass


@dataclass
class User_DTO:
    id: str
    name: str
    address: str
    email: str
    phone_no: str
    role: str

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'email': self.email,
            'phone_no': self.phone_no,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)