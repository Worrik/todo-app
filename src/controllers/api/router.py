from fastapi import APIRouter

from src.controllers.api.tasks.router import router as tasks_router
from src.controllers.api.users.router import router as users_router

router = APIRouter()
router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
router.include_router(users_router, prefix="/users", tags=["users"])
