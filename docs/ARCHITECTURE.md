# 架构设计文档

## 系统概述

大模型Agent应用平台是一个基于微服务架构的智能应用平台，集成了多种AI功能，包括知识库管理、智能问答、数据分析、可视化等。系统采用前后端分离架构，支持容器化部署和水平扩展。

## 整体架构

### 架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端应用      │    │   负载均衡      │    │   监控告警      │
│   (React)       │    │   (Nginx)       │    │   (Prometheus)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API网关       │
                    │  (FastAPI)      │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   认证服务      │    │   业务服务      │    │   工具服务      │
│   (Auth)        │    │   (Business)    │    │   (Tools)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   数据存储      │    │   向量数据库    │    │   对象存储      │
│   (MySQL)       │    │   (Milvus)      │    │   (MinIO)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 核心组件

1. **前端层**：React + TypeScript + Ant Design
2. **API网关层**：FastAPI + 中间件
3. **业务服务层**：模块化业务逻辑
4. **数据存储层**：MySQL + Milvus + MinIO
5. **基础设施层**：Docker + Docker Compose

## 技术选型

### 前端技术栈

| 技术 | 版本 | 用途 | 优势 |
|------|------|------|------|
| React | 18.x | UI框架 | 组件化、生态丰富 |
| TypeScript | 5.x | 类型系统 | 类型安全、开发体验好 |
| Ant Design | 5.x | UI组件库 | 企业级、设计规范 |
| ECharts | 5.x | 图表库 | 功能强大、性能优秀 |
| Axios | 1.x | HTTP客户端 | 易用、功能完整 |
| React Router | 6.x | 路由管理 | 声明式、功能丰富 |

### 后端技术栈

| 技术 | 版本 | 用途 | 优势 |
|------|------|------|------|
| FastAPI | 0.104.x | Web框架 | 高性能、自动文档 |
| Tortoise ORM | 0.20.x | ORM框架 | 异步、类型安全 |
| Pydantic | 2.x | 数据验证 | 类型验证、序列化 |
| JWT | 1.3.x | 认证 | 无状态、标准化 |
| Uvicorn | 0.24.x | ASGI服务器 | 高性能、异步 |

### 数据存储

| 技术 | 版本 | 用途 | 优势 |
|------|------|------|------|
| MySQL | 8.0 | 关系数据库 | 成熟稳定、生态丰富 |
| Milvus | 2.3.x | 向量数据库 | 高性能、易扩展 |
| MinIO | 8.x | 对象存储 | S3兼容、轻量级 |

### 部署运维

| 技术 | 版本 | 用途 | 优势 |
|------|------|------|------|
| Docker | 20.10+ | 容器化 | 标准化、可移植 |
| Docker Compose | 2.0+ | 编排工具 | 简单易用、开发友好 |
| Nginx | 1.24+ | 反向代理 | 高性能、功能丰富 |

## 模块设计

### 1. 用户认证模块

#### 功能职责
- 用户注册和登录
- JWT Token管理
- 权限验证
- 用户信息管理

#### 核心组件
```python
# 认证服务
class AuthService:
    async def authenticate_user(username: str, password: str) -> User
    async def create_access_token(user: User) -> str
    async def verify_token(token: str) -> User

# 权限中间件
class PermissionMiddleware:
    async def check_permission(user: User, resource: str, action: str) -> bool
```

#### 数据模型
```python
class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=255)
    role = fields.ForeignKeyField('models.Role', related_name='users')
    created_at = fields.DatetimeField(auto_now_add=True)

class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    permissions = fields.JSONField()
```

### 2. 知识库管理模块

#### 功能职责
- 文档上传和存储
- 文本分词和向量化
- 向量数据库管理
- 知识库元数据管理

#### 核心组件
```python
# 知识库服务
class KnowledgeService:
    async def create_knowledge(title: str, content: str) -> Knowledge
    async def process_document(file: UploadFile) -> List[Chunk]
    async def vectorize_chunks(chunks: List[Chunk]) -> List[str]
    async def store_vectors(vectors: List[str]) -> List[str]

# 文档处理器
class DocumentProcessor:
    async def extract_text(file: UploadFile) -> str
    async def split_text(text: str) -> List[str]
    async def clean_text(text: str) -> str
```

#### 数据模型
```python
class Knowledge(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    user = fields.ForeignKeyField('models.User', related_name='knowledge_bases')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Chunk(Model):
    id = fields.IntField(pk=True)
    knowledge = fields.ForeignKeyField('models.Knowledge', related_name='chunks')
    chunk_index = fields.IntField()
    content = fields.TextField()
    vector_id = fields.CharField(max_length=100)
```

### 3. RAG问答模块

#### 功能职责
- 向量检索
- 大模型调用
- 答案生成
- 来源追踪

#### 核心组件
```python
# RAG服务
class RAGService:
    async def search_similar_chunks(question: str, knowledge_id: int) -> List[Chunk]
    async def generate_answer(question: str, chunks: List[Chunk]) -> str
    async def rank_results(chunks: List[Chunk], scores: List[float]) -> List[Chunk]

# 向量检索器
class VectorRetriever:
    async def search(embedding: List[float], top_k: int = 5) -> List[SearchResult]
    async def get_embedding(text: str) -> List[float]
```

### 4. MCP工具调用模块

#### 功能职责
- MCP Server管理
- 工具发现和注册
- 工具调用执行
- 结果处理

#### 核心组件
```python
# MCP客户端
class MCPClient:
    async def connect(server_path: str) -> bool
    async def list_tools() -> List[Tool]
    async def call_tool(tool_name: str, arguments: dict) -> ToolResult
    async def disconnect()

# 工具管理器
class ToolManager:
    async def register_server(server_path: str) -> bool
    async def get_tools(server_path: str) -> List[Tool]
    async def execute_tool(server_path: str, tool_name: str, args: dict) -> ToolResult
```

### 5. Text2SQL模块

#### 功能职责
- 自然语言理解
- SQL生成
- 数据库连接管理
- 查询执行

#### 核心组件
```python
# Text2SQL服务
class Text2SQLService:
    async def convert_to_sql(question: str, database_url: str) -> str
    async def execute_sql(sql: str, database_url: str) -> QueryResult
    async def validate_sql(sql: str) -> bool

# 数据库连接器
class DatabaseConnector:
    async def connect(database_url: str) -> Connection
    async def execute_query(connection: Connection, sql: str) -> QueryResult
    async def get_schema(connection: Connection) -> Schema
```

### 6. ChatBI模块

#### 功能职责
- 多轮对话管理
- 上下文记忆
- SQL生成和执行
- 结果可视化

#### 核心组件
```python
# ChatBI服务
class ChatBIService:
    async def process_message(message: str, session_id: str) -> ChatResponse
    async def generate_sql(context: List[Message], database_url: str) -> str
    async def create_chart(data: QueryResult, chart_type: str) -> Chart

# 会话管理器
class SessionManager:
    async def create_session() -> str
    async def add_message(session_id: str, message: Message)
    async def get_context(session_id: str) -> List[Message]
```

## 数据流设计

### 1. 知识库创建流程

```
用户上传文档 → 文档解析 → 文本提取 → 文本清洗 → 分词分块 → 
向量化 → 存储到Milvus → 元数据存储到MySQL → 返回结果
```

### 2. RAG问答流程

```
用户提问 → 问题向量化 → 向量检索 → 获取相关文档 → 
构建提示词 → 调用大模型 → 生成答案 → 返回结果
```

### 3. MCP工具调用流程

```
用户选择工具 → 获取工具Schema → 用户填写参数 → 
验证参数 → 调用MCP Server → 执行工具 → 返回结果
```

### 4. Text2SQL流程

```
用户输入问题 → 获取数据库Schema → 构建提示词 → 
调用大模型 → 生成SQL → 验证SQL → 执行查询 → 返回结果
```

## 安全设计

### 1. 认证安全
- JWT Token过期机制
- 密码加密存储（bcrypt）
- 接口权限控制
- 会话管理

### 2. 数据安全
- SQL注入防护
- XSS攻击防护
- CSRF攻击防护
- 输入验证和过滤

### 3. 网络安全
- HTTPS协议
- 防火墙配置
- 访问控制
- 日志审计

### 4. 应用安全
- 依赖包安全扫描
- 代码安全审查
- 安全配置管理
- 漏洞修复流程

## 性能设计

### 1. 缓存策略
- Redis缓存热点数据
- 前端静态资源缓存
- API响应缓存
- 数据库查询缓存

### 2. 异步处理
- 异步数据库操作
- 异步文件处理
- 异步向量化处理
- 异步大模型调用

### 3. 连接池
- 数据库连接池
- HTTP连接池
- 向量数据库连接池

### 4. 负载均衡
- 多实例部署
- 负载均衡器
- 健康检查
- 故障转移

## 监控设计

### 1. 应用监控
- 接口响应时间
- 错误率统计
- 并发用户数
- 系统资源使用

### 2. 业务监控
- 用户活跃度
- 功能使用率
- 数据增长趋势
- 性能指标

### 3. 基础设施监控
- 服务器状态
- 数据库性能
- 网络连接
- 存储使用

### 4. 告警机制
- 阈值告警
- 异常告警
- 趋势告警
- 多渠道通知

## 扩展性设计

### 1. 水平扩展
- 无状态服务设计
- 负载均衡支持
- 数据分片策略
- 服务发现机制

### 2. 垂直扩展
- 模块化设计
- 插件化架构
- 配置化管理
- 热更新支持

### 3. 功能扩展
- API版本控制
- 向后兼容性
- 插件接口
- 自定义扩展

## 部署架构

### 1. 开发环境
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  前端开发   │    │  后端开发   │    │  数据库     │
│  (3000)     │    │  (8000)     │    │  (3306)     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 2. 测试环境
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  负载均衡   │    │  应用集群   │    │  数据集群   │
│  (Nginx)    │    │  (FastAPI)  │    │  (MySQL)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 3. 生产环境
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  CDN/缓存   │    │  应用集群   │    │  数据集群   │
│  (CloudFlare)│   │  (K8s)      │    │  (RDS)      │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 技术债务

### 1. 当前问题
- 异常处理不够完善
- 测试覆盖率较低
- 性能优化空间大
- 安全防护需要加强

### 2. 改进计划
- 完善异常处理机制
- 提高测试覆盖率
- 优化性能瓶颈
- 加强安全防护

### 3. 技术升级
- 升级依赖包版本
 