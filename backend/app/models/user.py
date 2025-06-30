from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, unique=True)
    password_hash = fields.CharField(max_length=128)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
        
    async def get_roles(self):
        """获取用户角色列表"""
        from app.models.user_role import UserRole
        user_roles = await UserRole.filter(user=self).prefetch_related('role')
        return [ur.role.name for ur in user_roles] 