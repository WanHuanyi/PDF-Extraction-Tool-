#!/bin/bash

# PDF Extraction Tool - One Click Start Script
# PDF 提取工具 - 一键启动脚本

echo "🚀 Starting PDF Extraction Tool..."
echo "🚀 正在启动 PDF 提取工具..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python
if ! command_exists python3; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 first."
    echo "❌ 错误: 未安装 Python 3。请先安装 Python 3。"
    exit 1
fi

# Check for Node.js/npm
if ! command_exists npm; then
    echo "❌ Error: Node.js/npm is not installed. Please install Node.js first."
    echo "❌ 错误: 未安装 Node.js/npm。请先安装 Node.js。"
    exit 1
fi

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

if [ ! -d ".venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv .venv
fi

echo "   Installing/Updating Python dependencies..."
source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo "✅ Backend ready."

# Start Backend in background
echo "🔥 Starting Backend Server..."
uvicorn main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
BACKEND_PID=$!

cd ..

# Setup Frontend
echo "📦 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing Node dependencies (this may take a while)..."
    npm install > /dev/null 2>&1
fi

echo "✅ Frontend ready."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    kill $BACKEND_PID
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

echo "🔥 Starting Frontend..."
echo "✨ Application will be available at: http://localhost:5173"
echo "✨ 应用将在 http://localhost:5173 启动"
echo "Press Ctrl+C to stop."

# Open browser after a slight delay to allow server to start
(sleep 3 && open "http://localhost:5173") &

npm run dev

# Cleanup if npm run dev exits
cleanup
