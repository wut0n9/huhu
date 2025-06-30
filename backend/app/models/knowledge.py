from tortoise import fields
from tortoise.models import Model

class Knowledge(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=128)
    content = fields.TextField()
    owner_id = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "knowledge"

class KnowledgeChunk(Model):
    id = fields.IntField(pk=True)
    knowledge = fields.ForeignKeyField('models.Knowledge', related_name='chunks')
    chunk_index = fields.IntField()
    content = fields.TextField()
    vector_id = fields.CharField(max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "knowledge_chunk" 