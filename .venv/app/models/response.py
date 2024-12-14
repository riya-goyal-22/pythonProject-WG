from dataclasses import dataclass


@dataclass
class CustomResponse:
    status_code: int
    message: str
    data: any

    def to_dict(self):
        return {
            'status_code': self.status_code,
            'message': self.message,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)