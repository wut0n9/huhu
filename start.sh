#!/bin/bash

echo "🚀 启动大模型Agent应用平台..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
mkdir -p logs uploads

# 复制环境变量文件
if [ ! -f backend/.env ]; then
    echo "📝 创建后端环境变量文件..."
    cp backend/env.example backend/.env
    echo "⚠️  请编辑 backend/.env 文件配置数据库连接等信息"
fi

# 启动服务
echo "🐳 启动Docker服务..."
docker-compose up -d

echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 服务状态检查..."
docker-compose ps

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "🌐 前端地址: http://localhost:5173"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "📝 使用说明:"
echo "1. 访问 http://localhost:5173 进入前端"
echo "2. 首次使用请先注册账户"
echo "3. 创建Agent并开始对话"
echo ""
echo "🛑 停止服务: docker-compose down"
echo "📋 查看日志: docker-compose logs -f" 