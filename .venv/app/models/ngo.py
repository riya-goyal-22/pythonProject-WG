import uuid


class NGO:
    def __init__(self, name: str, email: str, details: str, phone_no: str, address: str, id: str = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.address = address
        self.details = details

    def to_dict(self):
        """Convert NGO instance to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_no": self.phone_no,
            "address": self.address,
            "details": self.details
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)