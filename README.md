# 大模型Agent应用平台

基于FastAPI + Vue 3 + TypeScript的现代化大模型Agent应用平台。

## 技术栈

### 后端
- **框架**: FastAPI
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据库**: MySQL 8.0+
- **缓存/消息队列**: Redis
- **认证**: JWT
- **任务队列**: Celery
- **文档**: 自动生成API文档

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **UI组件**: Element Plus
- **HTTP客户端**: Axios

## 项目结构

```
huhu/
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python依赖
├── frontend/               # Vue前端
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia状态管理
│   │   ├── router/         # Vue Router
│   │   ├── types/          # TypeScript类型
│   │   └── utils/          # 工具函数
│   ├── public/             # 静态资源
│   └── package.json        # Node.js依赖
├── docker/                 # Docker配置
├── docs/                   # 项目文档
└── README.md              # 项目说明
```

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 功能特性

- 🤖 Agent管理：创建、配置、监控Agent实例
- 📋 任务调度：任务分配、执行和状态跟踪
- 💬 对话管理：与Agent的实时交互界面
- 🔧 模型集成：支持多种大模型API
- 👥 用户管理：JWT认证和RBAC权限控制
- 📊 监控面板：实时状态、性能指标和日志
- ⚙️ 配置管理：Agent参数和系统配置

## 开发环境

- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Redis 6.0+ 