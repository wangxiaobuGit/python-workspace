#!/bin/bash

# AI 工具导航网站部署脚本

set -e

echo "🚀 开始部署 AI 工具导航网站..."

# 检查 Python 版本
echo "📋 检查 Python 版本..."
python3 --version

# 安装依赖
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 检查数据文件
echo "📄 检查数据文件..."
if [ ! -f "data/ai_tools.json" ]; then
    echo "❌ 数据文件不存在！"
    exit 1
fi

# 创建必要的目录
echo "📁 创建目录..."
mkdir -p logs
mkdir -p static/images

# 设置权限
echo "🔐 设置权限..."
chmod +x app.py

# 检查端口是否被占用
echo "🔍 检查端口 12000..."
if lsof -Pi :12000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 12000 已被占用，正在停止现有进程..."
    pkill -f "python.*app.py" || true
    sleep 2
fi

# 启动应用
echo "🌟 启动应用..."
if [ "$1" = "production" ]; then
    echo "🏭 生产环境模式"
    export FLASK_ENV=production
    nohup python3 app.py > logs/app.log 2>&1 &
else
    echo "🔧 开发环境模式"
    export FLASK_ENV=development
    python3 app.py
fi

# 等待应用启动
sleep 3

# 健康检查
echo "🏥 健康检查..."
if curl -f http://localhost:12000/ > /dev/null 2>&1; then
    echo "✅ 应用启动成功！"
    echo "🌐 访问地址: http://localhost:12000"
    echo "🔧 管理后台: http://localhost:12000/admin"
else
    echo "❌ 应用启动失败！"
    echo "📋 查看日志: tail -f logs/app.log"
    exit 1
fi

echo "🎉 部署完成！"