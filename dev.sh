#!/bin/bash

echo "🔧 启动开发环境 (使用uv)..."

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ uv 未安装，请先安装uv"
    echo "👉 运行: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js"
    exit 1
fi

# 检查MySQL是否运行
if ! mysqladmin ping -h localhost -u root -p "" &>/dev/null; then
    echo "⚠️  MySQL未运行，请先启动MySQL服务"
    echo "   或者使用Docker启动: docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 mysql:8.0"
fi

# 检查Redis是否运行
if ! redis-cli ping &>/dev/null; then
    echo "⚠️  Redis未运行，请先启动Redis服务"
    echo "   或者使用Docker启动: docker run -d --name redis -p 6379:6379 redis:7-alpine"
fi

# 创建必要的目录
mkdir -p logs uploads

# 复制环境变量文件
if [ ! -f backend/.env ]; then
    echo "📝 创建后端环境变量文件..."
    cp backend/env.example backend/.env
    echo "⚠️  请编辑 backend/.env 文件配置数据库连接等信息"
fi

# 安装后端依赖
echo "📦 安装后端依赖 (使用uv)..."
cd backend
if [ ! -d ".venv" ]; then
    echo "🐍 创建Python虚拟环境 (使用uv)..."
    uv venv
fi
uv pip install -r requirements.txt
cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "🚀 启动服务:"
echo "1. 启动后端: cd backend && uv run uvicorn app.main:app --reload"
echo "2. 启动前端: cd frontend && npm run dev"
echo ""
echo "🌐 访问地址:"
echo "   前端: http://localhost:5173"
echo "   后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs" 