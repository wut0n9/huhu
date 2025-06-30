# 大模型Agent应用平台

一个基于FastAPI和React的大模型Agent应用平台，集成了知识库RAG问答、数据可视化、ChatBI、MCP工具调用、Text2SQL等核心功能。

## 🚀 功能特性

### 核心功能
- **知识库RAG问答**：支持文档上传、分词、向量化、智能问答
- **数据可视化**：基于ECharts的数据可视化，支持多种图表类型
- **ChatBI**：对话式BI分析，支持多轮对话和SQL生成
- **MCP工具调用**：支持Model Context Protocol工具调用
- **Text2SQL**：自然语言转SQL，支持复杂查询生成
- **用户权限管理**：基于RBAC的用户认证和权限控制

### 技术特性
- **前后端分离**：React + TypeScript + Ant Design前端，FastAPI后端
- **向量数据库**：集成Milvus向量数据库，支持高效相似性检索
- **对象存储**：集成MinIO对象存储，支持文件管理
- **容器化部署**：支持Docker容器化部署
- **API文档**：自动生成Swagger/OpenAPI文档

## 🛠️ 技术栈

### 后端
- **框架**：FastAPI
- **数据库**：MySQL + Milvus
- **ORM**：Tortoise ORM
- **对象存储**：MinIO
- **认证**：JWT
- **向量检索**：Milvus
- **大模型API**：OpenAI兼容协议

### 前端
- **框架**：React + TypeScript
- **UI组件**：Ant Design
- **图表库**：ECharts
- **状态管理**：React Hooks
- **路由**：React Router
- **HTTP客户端**：Axios

## 📦 项目结构

```
huhu/
├── backend/                # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React前端
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── pages/          # 页面
│   │   ├── api/            # API请求
│   │   └── router/         # 路由配置
│   ├── package.json
│   └── Dockerfile
├── deploy/                 # 部署配置
│   ├── docker-compose.yml
│   └── env.example
└── README.md
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- MySQL 8.0+
- MinIO

### 1. 克隆项目
```bash
git clone <repository-url>
cd huhu
```

### 2. 配置环境变量
```bash
cd deploy
cp env.example .env
# 编辑.env文件，配置数据库密码、JWT密钥、OpenAI API Key等
```

### 3. Docker部署（推荐）
```bash
cd deploy
docker-compose up -d
```

### 4. 访问应用
- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs
- MinIO控制台：http://localhost:9001

### 5. 开发环境启动

#### 后端启动
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### 前端启动
```bash
cd frontend
npm install
npm start
```

## 📚 功能使用

### 用户认证
1. 访问 `/register` 注册新用户
2. 访问 `/login` 登录系统
3. 访问 `/profile` 查看个人信息

### 知识库管理
1. 访问 `/knowledge` 查看知识库列表
2. 点击"新建知识库"上传文档或输入文本
3. 系统自动进行分词、向量化处理
4. 查看知识库详情和分片信息

### RAG问答
1. 在知识库详情页进行智能问答
2. 系统基于向量检索和大模型生成答案

### 数据可视化
1. 访问 `/visualization` 配置数据源
2. 输入SQL查询语句
3. 选择图表类型
4. 查看可视化结果

### ChatBI
1. 访问 `/chatbi` 进入对话界面
2. 配置数据库连接
3. 用自然语言描述分析需求
4. 系统自动生成SQL并执行
5. 查看表格和图表结果

### Text2SQL
1. 访问 `/text2sql` 进入查询界面
2. 配置数据库连接
3. 输入自然语言问题
4. 系统生成SQL并执行
5. 查看查询结果

### MCP工具调用
1. 访问 `/mcp` 进入工具调用界面
2. 选择MCP Server
3. 查看可用工具列表
4. 配置工具参数
5. 执行工具调用

## 🔧 配置说明

### 环境变量
```bash
# 数据库配置
MYSQL_ROOT_PASSWORD=your-mysql-root-password
MYSQL_DATABASE=huhu
MYSQL_USER=huhu
MYSQL_PASSWORD=huhu123

# JWT配置
JWT_SECRET=your-jwt-secret-key

# OpenAI配置
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1

# MinIO配置
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

## 🐳 Docker部署

### 使用Docker Compose
```bash
cd deploy
docker-compose up -d
```

### 查看服务状态
```bash
docker-compose ps
```

### 查看日志
```bash
docker-compose logs -f backend
```

## 📖 API文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的API文档。

## 🔧 开发说明

### 最近修复的问题
- ✅ 完善了用户认证和权限管理
- ✅ 实现了完整的RAG问答功能
- ✅ 修复了知识库CRUD操作
- ✅ 完善了Text2SQL和ChatBI功能
- ✅ 添加了数据可视化页面
- ✅ 完善了异常处理和日志记录
- ✅ 修复了前端配置和路由
- ✅ 完善了Docker部署配置

### 开发注意事项
1. 确保配置了正确的OpenAI API Key
2. 数据库会自动初始化并创建默认角色
3. 前端代理配置指向后端API
4. 所有API都需要JWT认证（除了登录注册）

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

如有问题或建议，请提交 Issue 或联系开发团队。
