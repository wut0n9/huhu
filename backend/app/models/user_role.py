from tortoise import fields
from tortoise.models import Model
from .user import User
from .role import Role

class UserRole(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='user_roles')
    role = fields.ForeignKeyField('models.Role', related_name='role_users')

    class Meta:
        table = "user_roles" 