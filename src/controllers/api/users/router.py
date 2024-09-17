from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from src.application.users.dto import UpdateUserDTO
from src.application.users.interactors import UpdateUserInteractor
from src.controllers.api.users.auth.manager import UserAuthEntity
from src.controllers.api.users.auth.router import router as auth_router
from src.controllers.api.users.auth.users import current_active_user
from src.controllers.api.users.schemas import UserAuthUpdateSchema, UserSchema

router = APIRouter()
router.include_router(auth_router)


@router.get("/me/")
async def get_me(
    current_user: UserAuthEntity = Depends(current_active_user),
) -> UserSchema:
    return UserSchema(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        is_active=current_user.is_active,
    )


@router.patch("/me/", status_code=204)
@inject
async def update_me(
    user: UserAuthUpdateSchema,
    interactor: FromDishka[UpdateUserInteractor],
    current_user: UserAuthEntity = Depends(current_active_user),
) -> None:
    dto = UpdateUserDTO(
        user_id=current_user.id,
        email=user.email,
        name=user.name,
        password=user.password,
    )
    await interactor(dto)
