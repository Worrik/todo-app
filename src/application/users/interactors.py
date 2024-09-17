from src.application.users.dto import UpdateUserDTO
from src.application.users.interfaces.repo import UserRepo


class UpdateUserInteractor:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def __call__(self, dto: UpdateUserDTO) -> None:
        await self.user_repo.update(
            user_id=dto.user_id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
        )
