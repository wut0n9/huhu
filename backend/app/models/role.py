from tortoise import fields
from tortoise.models import Model

class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, unique=True)
    description = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "roles" 