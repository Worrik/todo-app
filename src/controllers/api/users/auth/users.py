from fastapi_users import FastAPIUsers

from src.controllers.api.users.auth.backend import get_auth_backend
from src.controllers.api.users.auth.manager import UserAuthEntity, get_user_manager

auth_backend = get_auth_backend()
fastapi_users = FastAPIUsers[UserAuthEntity, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
