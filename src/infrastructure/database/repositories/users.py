import sqlalchemy as sa

from src.application.common.pagination.constants import Empty
from src.application.users.interfaces.repo import UserRepo
from src.domain.users.entities import UserDM
from src.infrastructure.database.converters import convert_user_mode_to_domain_model
from src.infrastructure.database.models.users import User
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class UserRepoImpl(SQLAlchemyRepo, UserRepo):
    @staticmethod
    def _map_to_domain_model(model: User) -> UserDM:
        return convert_user_mode_to_domain_model(model)

    async def create(
        self, name: str, email: str, password: str, is_active: bool = True
    ) -> int:
        user = User(name=name, email=email, password=password, is_active=is_active)
        self._session.add(user)
        await self._session.commit()
        return user.id

    async def get(self, user_id: int) -> UserDM:
        user = await self._session.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return self._map_to_domain_model(user)

    async def get_by_email(self, email: str) -> UserDM:
        query = sa.select(User).where(User.email == email).limit(1)
        result = await self._session.execute(query)
        user = result.scalars().first()
        if not user:
            raise ValueError(f"User with email {email} not found")
        return self._map_to_domain_model(user)

    async def update(
        self,
        user_id: int,
        name: str | Empty = Empty.UNSET,
        email: str | Empty = Empty.UNSET,
        password: str | Empty = Empty.UNSET,
        is_active: bool | Empty = Empty.UNSET,
    ) -> None:
        query = sa.update(User).where(User.id == user_id)
        if name is not Empty.UNSET:
            query = query.values(name=name)
        if email is not Empty.UNSET:
            query = query.values(email=email)
        if password is not Empty.UNSET:
            query = query.values(password=password)
        if is_active is not Empty.UNSET:
            query = query.values(is_active=is_active)
        await self._session.execute(query)
        await self._session.commit()

    async def delete(self, user_id: int) -> None:
        query = sa.delete(User).where(User.id == user_id)
        await self._session.execute(query)
