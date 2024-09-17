from dataclasses import dataclass

from src.application.common.pagination.constants import Empty


@dataclass
class UpdateUserDTO:
    user_id: int
    name: str | Empty = Empty.UNSET
    email: str | Empty = Empty.UNSET
    password: str | Empty = Empty.UNSET
