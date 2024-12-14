from dataclasses import dataclass


@dataclass
class NewNGO:
    name: str
    address: str
    phone_no: str
    email: str
    details: str

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'details': self.details,
            'address': self.address,
            'phone_no': self.phone_no
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
