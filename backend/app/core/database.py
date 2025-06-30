from tortoise import Tortoise
from app.core.config import settings
from loguru import logger

async def init_db():
    """初始化数据库"""
    await Tortoise.init(
        db_url=settings.MYSQL_URL,
        modules={"models": [
            "app.models.user", 
            "app.models.role", 
            "app.models.user_role",
            "app.models.knowledge"
        ]}
    )
    await Tortoise.generate_schemas()
    
    # 创建默认角色
    await create_default_roles()
    
    logger.info("数据库初始化完成")

async def create_default_roles():
    """创建默认角色"""
    from app.models.role import Role
    
    default_roles = [
        {"name": "admin", "description": "管理员"},
        {"name": "user", "description": "普通用户"},
        {"name": "guest", "description": "访客"}
    ]
    
    for role_data in default_roles:
        await Role.get_or_create(
            name=role_data["name"],
            defaults={"description": role_data["description"]}
        )
    
    logger.info("默认角色创建完成")

async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()
    logger.info("数据库连接已关闭") 