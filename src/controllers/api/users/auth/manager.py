from dataclasses import dataclass
from typing import Any

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi_users import BaseUserManager, models
from fastapi_users.db import BaseUserDatabase

from src.application.users.interfaces.repo import UserRepo
from src.domain.users.entities import UserDM


@dataclass
class UserAuthEntity(models.UserProtocol):
    id: int
    name: str
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserAuthDatabase(BaseUserDatabase):
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    @staticmethod
    def map_domain_model_to_entity(user: UserDM) -> UserAuthEntity:
        return UserAuthEntity(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.password,
            is_active=user.is_active,
            is_superuser=False,
            is_verified=True,
        )

    async def get(self, id: int) -> UserAuthEntity | None:
        user = await self.user_repo.get(id)
        try:
            user = await self.user_repo.get(id)
        except ValueError:
            return None
        return self.map_domain_model_to_entity(user)

    async def get_by_email(self, email: str) -> UserAuthEntity | None:
        try:
            user = await self.user_repo.get_by_email(email)
        except ValueError:
            return None
        return self.map_domain_model_to_entity(user)

    async def create(self, create_dict: dict) -> UserAuthEntity:
        user_id = await self.user_repo.create(
            name=create_dict["name"],
            email=create_dict["email"],
            password=create_dict["hashed_password"],
        )
        user = await self.user_repo.get(user_id)
        return self.map_domain_model_to_entity(user)

    async def update(self, user: UserAuthEntity, update_dict: dict) -> UserAuthEntity:
        await self.user_repo.update(user.id, **update_dict)
        user_dm = await self.user_repo.get(user.id)
        return self.map_domain_model_to_entity(user_dm)

    async def delete(self, user: UserAuthEntity) -> None:
        await self.user_repo.delete(user.id)


class UserAuthManager(BaseUserManager[UserAuthEntity, int]):
    def __init__(self, user_db: UserAuthDatabase):
        super().__init__(user_db)

    def parse_id(self, value: Any) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        raise ValueError("Invalid ID")


@inject
async def get_user_db(user_repo: FromDishka[UserRepo]):
    yield UserAuthDatabase(user_repo)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserAuthManager(user_db)
