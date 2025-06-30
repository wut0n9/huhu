# 开发文档

## 开发环境搭建

### 1. 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- MinIO
- Milvus

### 2. 后端开发环境

#### 安装依赖
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 数据库配置
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE huhu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 启动MinIO
docker run -d -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"

# 启动Milvus
docker run -d -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest
```

#### 启动开发服务器
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端开发环境

#### 安装依赖
```bash
cd frontend
npm install
```

#### 启动开发服务器
```bash
npm start
```

## API开发指南

### 1. 路由结构
```
/api/v1/
├── auth/           # 用户认证
├── users/          # 用户管理
├── roles/          # 角色管理
├── knowledge/      # 知识库管理
├── rag/            # RAG问答
├── mcp/            # MCP工具调用
├── text2sql/       # Text2SQL
├── chatbi/         # ChatBI
└── visualization/  # 数据可视化
```

### 2. 认证机制
所有需要认证的接口都需要在请求头中包含JWT Token：
```
Authorization: Bearer <your-jwt-token>
```

### 3. 错误处理
API统一返回格式：
```json
{
  "detail": "错误信息"
}
```

### 4. 分页处理
支持分页的接口使用以下参数：
- `page`: 页码（从1开始）
- `size`: 每页大小
- `total`: 总记录数

## 代码规范

### 1. Python代码规范
- 遵循PEP 8规范
- 使用类型注解
- 函数和类添加文档字符串
- 异常处理要具体明确

### 2. TypeScript代码规范
- 使用ESLint和Prettier
- 组件使用函数式组件
- 使用TypeScript严格模式
- 接口和类型定义清晰

### 3. 数据库规范
- 表名使用小写字母和下划线
- 字段名使用小写字母和下划线
- 主键统一使用id
- 时间字段使用created_at、updated_at

### 4. API设计规范
- RESTful API设计
- 使用HTTP状态码
- 请求和响应使用JSON格式
- 版本控制使用URL路径

## 测试指南

### 1. 后端测试
```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行测试
pytest tests/
```

### 2. 前端测试
```bash
# 运行测试
npm test

# 运行测试覆盖率
npm run test:coverage
```

## 部署指南

### 1. 生产环境配置
```bash
# 环境变量配置
export MYSQL_URL=mysql://user:password@host:3306/huhu
export MILVUS_HOST=milvus
export MINIO_ENDPOINT=minio:9000
export JWT_SECRET=your-production-secret
```

### 2. Docker部署
```bash
# 构建镜像
docker build -t huhu-backend ./backend
docker build -t huhu-frontend ./frontend

# 使用docker-compose启动
cd deploy
docker-compose up -d
```

## 常见问题

### 1. 数据库连接问题
- 检查MySQL服务是否启动
- 验证数据库连接字符串
- 确认数据库用户权限

### 2. Milvus连接问题
- 检查Milvus服务状态
- 验证网络连接
- 查看Milvus日志

### 3. MinIO连接问题
- 检查MinIO服务状态
- 验证访问密钥
- 确认存储桶权限

### 4. 前端构建问题
- 清理node_modules重新安装
- 检查Node.js版本
- 查看构建日志

## 性能优化

### 1. 数据库优化
- 添加适当的索引
- 优化查询语句
- 使用连接池

### 2. 缓存策略
- Redis缓存热点数据
- 前端缓存静态资源
- API响应缓存

### 3. 前端优化
- 代码分割
- 懒加载组件
- 图片压缩

## 监控和日志

### 1. 日志配置
- 使用loguru进行日志记录
- 配置日志级别和格式
- 日志文件轮转

### 2. 性能监控
- 接口响应时间监控
- 数据库查询性能监控
- 系统资源使用监控

## 安全考虑

### 1. 认证安全
- JWT Token过期时间设置
- 密码加密存储
- 接口权限控制

### 2. 数据安全
- SQL注入防护
- XSS攻击防护
- CSRF攻击防护

### 3. 网络安全
- HTTPS配置
- 防火墙设置
- 访问控制 