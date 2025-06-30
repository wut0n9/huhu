# 部署文档

## 部署概述

本文档介绍如何部署大模型Agent应用平台，支持Docker容器化部署和传统部署方式。

## 环境要求

### 系统要求
- Linux/Windows/macOS
- Docker 20.10+
- Docker Compose 2.0+
- 至少4GB内存
- 至少20GB磁盘空间

### 网络要求
- 端口8000（后端API）
- 端口3000（前端应用）
- 端口3306（MySQL）
- 端口9000（MinIO）
- 端口19530（Milvus）

## Docker部署

### 1. 快速部署

#### 使用Docker Compose
```bash
# 克隆项目
git clone <repository-url>
cd huhu

# 配置环境变量
cp deploy/.env.example deploy/.env
# 编辑.env文件，配置数据库密码、JWT密钥等

# 启动服务
cd deploy
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 访问服务
- 前端应用：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs
- MinIO控制台：http://localhost:9001
- Milvus控制台：http://localhost:9091

### 2. 生产环境部署

#### 环境变量配置
创建`.env`文件：
```bash
# 数据库配置
MYSQL_ROOT_PASSWORD=your-mysql-password
MYSQL_DATABASE=huhu
MYSQL_USER=huhu
MYSQL_PASSWORD=huhu-password

# 后端配置
JWT_SECRET=your-jwt-secret-key
OPENAI_API_KEY=your-openai-api-key

# MinIO配置
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# 网络配置
BACKEND_PORT=8000
FRONTEND_PORT=3000
MYSQL_PORT=3306
MINIO_PORT=9000
MILVUS_PORT=19530
```

#### 启动服务
```bash
# 启动所有服务
docker-compose -f docker-compose.prod.yml up -d

# 初始化数据库
docker-compose exec backend python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"

# 创建管理员用户
docker-compose exec backend python -c "from app.services.user import register_user; import asyncio; asyncio.run(register_user('admin', 'admin123'))"
```

### 3. 服务配置

#### 后端服务配置
```yaml
backend:
  build: ../backend
  environment:
    - MYSQL_URL=mysql://huhu:huhu-password@mysql:3306/huhu
    - MILVUS_HOST=milvus
    - MILVUS_PORT=19530
    - MINIO_ENDPOINT=minio:9000
    - MINIO_ACCESS_KEY=minioadmin
    - MINIO_SECRET_KEY=minioadmin
    - JWT_SECRET=${JWT_SECRET}
  ports:
    - "8000:8000"
  depends_on:
    - mysql
    - milvus
    - minio
```

#### 前端服务配置
```yaml
frontend:
  build: ../frontend
  environment:
    - REACT_APP_API_URL=http://localhost:8000
  ports:
    - "3000:3000"
  depends_on:
    - backend
```

#### 数据库服务配置
```yaml
mysql:
  image: mysql:8.0
  environment:
    - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
    - MYSQL_DATABASE=${MYSQL_DATABASE}
    - MYSQL_USER=${MYSQL_USER}
    - MYSQL_PASSWORD=${MYSQL_PASSWORD}
  ports:
    - "3306:3306"
  volumes:
    - mysql_data:/var/lib/mysql
```

#### MinIO服务配置
```yaml
minio:
  image: minio/minio
  environment:
    - MINIO_ROOT_USER=${MINIO_ROOT_USER}
    - MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
  ports:
    - "9000:9000"
    - "9001:9001"
  volumes:
    - minio_data:/data
  command: server /data --console-address ":9001"
```

#### Milvus服务配置
```yaml
milvus:
  image: milvusdb/milvus:latest
  environment:
    - ETCD_USE_EMBED=true
    - ETCD_DATA_DIR=/var/lib/milvus/etcd
    - ETCD_CONFIG_PATH=/milvus/configs/etcd.yaml
  ports:
    - "19530:19530"
    - "9091:9091"
  volumes:
    - milvus_data:/var/lib/milvus
```

## 传统部署

### 1. 后端部署

#### 安装依赖
```bash
# 安装Python依赖
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 安装系统依赖
sudo apt-get update
sudo apt-get install -y mysql-client
```

#### 配置环境
```bash
# 设置环境变量
export MYSQL_URL=mysql://user:password@localhost:3306/huhu
export MILVUS_HOST=localhost
export MILVUS_PORT=19530
export MINIO_ENDPOINT=localhost:9000
export JWT_SECRET=your-secret-key
```

#### 启动服务
```bash
# 开发环境
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产环境
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. 前端部署

#### 安装依赖
```bash
cd frontend
npm install
```

#### 构建生产版本
```bash
npm run build
```

#### 部署到Web服务器
```bash
# 使用Nginx
sudo cp -r build/* /var/www/html/
sudo systemctl restart nginx

# 使用Apache
sudo cp -r build/* /var/www/html/
sudo systemctl restart apache2
```

## 运维指南

### 1. 服务管理

#### 启动服务
```bash
# 启动所有服务
docker-compose up -d

# 启动特定服务
docker-compose up -d backend
docker-compose up -d frontend
```

#### 停止服务
```bash
# 停止所有服务
docker-compose down

# 停止特定服务
docker-compose stop backend
```

#### 重启服务
```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 2. 日志管理

#### 查看日志
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend

# 实时查看日志
docker-compose logs -f backend
```

#### 日志轮转
```bash
# 配置logrotate
sudo nano /etc/logrotate.d/huhu

# 配置内容
/var/log/huhu/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 root root
}
```

### 3. 数据备份

#### 数据库备份
```bash
# 备份MySQL数据
docker-compose exec mysql mysqldump -u root -p huhu > backup.sql

# 恢复MySQL数据
docker-compose exec -T mysql mysql -u root -p huhu < backup.sql
```

#### 文件备份
```bash
# 备份MinIO数据
docker-compose exec minio mc mirror /data /backup

# 备份Milvus数据
docker-compose exec milvus cp -r /var/lib/milvus /backup
```

### 4. 监控告警

#### 健康检查
```bash
# 检查服务状态
curl http://localhost:8000/ping

# 检查数据库连接
docker-compose exec backend python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

#### 性能监控
```bash
# 查看资源使用情况
docker stats

# 查看磁盘使用情况
df -h

# 查看内存使用情况
free -h
```

### 5. 故障排查

#### 常见问题
1. **服务启动失败**
   - 检查端口是否被占用
   - 检查环境变量配置
   - 查看服务日志

2. **数据库连接失败**
   - 检查MySQL服务状态
   - 验证连接字符串
   - 检查网络连接

3. **文件上传失败**
   - 检查MinIO服务状态
   - 验证存储桶权限
   - 检查磁盘空间

4. **向量检索失败**
   - 检查Milvus服务状态
   - 验证集合配置
   - 查看Milvus日志

#### 调试命令
```bash
# 进入容器调试
docker-compose exec backend bash
docker-compose exec frontend bash

# 查看网络连接
docker network ls
docker network inspect huhu_default

# 查看容器配置
docker-compose config
```

## 安全配置

### 1. 网络安全
- 配置防火墙规则
- 使用HTTPS协议
- 限制端口访问

### 2. 数据安全
- 定期备份数据
- 加密敏感信息
- 配置访问控制

### 3. 应用安全
- 更新依赖包
- 配置安全头
- 启用日志审计

## 扩展部署

### 1. 负载均衡
```bash
# 使用Nginx负载均衡
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### 2. 高可用部署
- 使用多个后端实例
- 配置数据库主从复制
- 使用Redis缓存

### 3. 微服务部署
- 拆分服务模块
- 使用服务网格
- 配置API网关
