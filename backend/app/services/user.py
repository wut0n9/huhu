from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.security import hash_password, verify_password, create_access_token
from tortoise.exceptions import DoesNotExist

async def register_user(username: str, password: str):
    exists = await User.filter(username=username).first()
    if exists:
        raise ValueError("用户名已存在")
    user = await User.create(username=username, password_hash=hash_password(password))
    # 默认分配user角色
    role = await Role.get_or_create(name="user", defaults={"description": "普通用户"})
    await UserRole.create(user=user, role=role[0])
    return user

async def authenticate_user(username: str, password: str):
    user = await User.filter(username=username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

async def get_user_roles(user_id: int):
    roles = await Role.filter(role_users__user_id=user_id).all()
    return [r.name for r in roles]

async def get_user_by_id(user_id: int):
    return await User.get(id=user_id)

async def create_jwt_for_user(user: User):
    roles = await get_user_roles(user.id)
    token = create_access_token({"sub": str(user.id), "roles": roles})
    return token 