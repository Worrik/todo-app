from dataclasses import dataclass


@dataclass
class UserDM:
    id: int
    name: str
    email: str
    password: str
    is_active: bool
