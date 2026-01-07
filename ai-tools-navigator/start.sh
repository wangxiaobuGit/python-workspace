#!/bin/bash

# AI导航工具网站启动脚本

echo "🚀 启动AI导航工具网站..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
pip install -r requirements.txt

# 初始化GitHub热榜数据
echo "🔄 初始化GitHub热榜数据..."
python3 github_trending.py

# 启动Flask应用
echo "🌐 启动Web服务器..."
echo "访问地址: http://localhost:12001"
echo "管理后台: http://localhost:12001/admin"
echo "按 Ctrl+C 停止服务器"

python3 app.py