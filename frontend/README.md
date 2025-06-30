# Huhu 前端应用

基于 React + TypeScript + Ant Design X 的聊天应用前端。

## 功能特性

- 🎨 基于 Ant Design X 的现代化 UI 设计
- 💬 实时聊天对话功能
- 📁 文件上传和管理
- 🔧 MCP 工具选择和调用
- 📱 响应式设计，支持移动端
- 🔄 流式消息响应
- 👤 用户认证和权限管理
- 📚 对话历史管理

## 技术栈

- **框架**: React 18 + TypeScript
- **UI 组件**: Ant Design X
- **路由**: React Router v6
- **HTTP 客户端**: Axios
- **构建工具**: Vite
- **状态管理**: React Hooks + Context API

## 项目结构

```
src/
├── components/          # 组件目录
│   ├── ChatPage/       # 聊天页面组件
│   │   ├── index.tsx   # 主聊天页面
│   │   ├── ChatHistory.tsx    # 对话历史
│   │   ├── ChatInput.tsx      # 输入框
│   │   ├── MessageItem.tsx    # 消息项
│   │   ├── FileUpload.tsx     # 文件上传
│   │   ├── MCPToolSelector.tsx # MCP工具选择
│   │   └── UserInfo.tsx       # 用户信息
│   └── common/         # 通用组件
├── hooks/              # 自定义 Hooks
├── services/           # API 服务
├── types/              # TypeScript 类型定义
├── utils/              # 工具函数
├── styles/             # 样式文件
└── pages/              # 页面组件
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发环境启动

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 环境配置

### 开发环境

创建 `.env.local` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 生产环境

创建 `.env.production` 文件：

```env
VITE_API_BASE_URL=https://your-api-domain.com
```

## 主要功能

### 聊天功能

- 实时消息发送和接收
- 流式响应显示
- 消息历史记录
- 对话管理

### 文件上传

- 支持多种文件格式
- 拖拽上传
- 上传进度显示
- 文件大小限制

### MCP 工具

- 工具列表展示
- 工具搜索和筛选
- 工具选择和配置
- 工具调用状态显示

### 用户管理

- 用户登录/登出
- 用户信息显示
- 权限控制

## API 接口

### 聊天相关

- `POST /api/v1/agent/chat` - 发送消息
- `GET /api/v1/agent/conversations` - 获取对话列表
- `GET /api/v1/agent/conversations/{id}/history` - 获取对话历史
- `DELETE /api/v1/agent/conversations/{id}` - 清除对话

### 文件上传

- `POST /api/v1/knowledge/upload` - 上传文件

### MCP 工具

- `GET /api/v1/mcp/tools` - 获取工具列表

### 用户认证

- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户登出
- `GET /api/v1/auth/me` - 获取当前用户信息

## 开发指南

### 添加新组件

1. 在 `src/components` 目录下创建组件文件
2. 使用 TypeScript 定义组件接口
3. 添加相应的样式文件
4. 在需要的地方导入使用

### 添加新 API

1. 在 `src/services` 目录下添加 API 函数
2. 在 `src/types` 目录下定义相关类型
3. 在组件中调用 API 函数

### 样式规范

- 使用 CSS Modules 或内联样式
- 遵循 Ant Design 设计规范
- 支持响应式设计
- 使用 CSS 变量管理主题

## 部署

### Docker 部署

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 80

CMD ["npm", "run", "preview"]
```

### 静态文件部署

构建完成后，将 `dist` 目录部署到 Web 服务器即可。

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
