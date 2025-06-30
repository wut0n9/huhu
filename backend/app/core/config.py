import os

class Settings:
    PROJECT_NAME: str = "大模型Agent应用平台"
    VERSION: str = "0.1.0"
    
    # 数据库配置
    MYSQL_URL: str = os.getenv("MYSQL_URL", "mysql://root:password@mysql:3306/huhu")
    
    # Milvus配置
    MILVUS_HOST: str = os.getenv("MILVUS_HOST", "milvus")
    MILVUS_PORT: int = int(os.getenv("MILVUS_PORT", 19530))
    
    # JWT配置
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))
    
    # MinIO配置
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "knowledge")
    
    # LLM配置
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    LLM_EMBEDDING_MODEL: str = os.getenv("LLM_EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # OpenAI配置（兼容性）
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_EMBEDDING_MODEL: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
    
    # MCP配置
    MCP_MAX_TOOL_ROUNDS: int = int(os.getenv("MCP_MAX_TOOL_ROUNDS", "5"))
    MCP_TEMPERATURE: float = float(os.getenv("MCP_TEMPERATURE", "0.1"))
    
    # Agent配置
    AGENT_MAX_HISTORY: int = int(os.getenv("AGENT_MAX_HISTORY", "10"))
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "30"))
    
    # 应用配置
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings() 