@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🚀 Starting PDF Extraction Tool...
echo 🚀 正在启动 PDF 提取工具...
echo.

REM Check for Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed. Please install Python first.
    echo ❌ 错误: 未安装 Python。请先安装 Python。
    pause
    exit /b 1
)

REM Check for Node.js/npm
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Node.js/npm is not installed. Please install Node.js first.
    echo ❌ 错误: 未安装 Node.js/npm。请先安装 Node.js。
    pause
    exit /b 1
)

REM Setup Backend
echo 📦 Setting up Backend...
cd backend

if not exist ".venv" (
    echo    Creating virtual environment...
    python -m venv .venv
)

echo    Installing/Updating Python dependencies (This may take a few minutes)...
echo    正在安装/更新 Python 依赖（首次运行可能需要几分钟）...
call .venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

echo ✅ Backend ready.

REM Start Backend in a new minimized window
echo 🔥 Starting Backend Server...
start /min "PDF-Tool-Backend" cmd /c "call .venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000"

cd ..

REM Setup Frontend
echo 📦 Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo    Installing Node dependencies (This may take a few minutes)...
    echo    正在安装前端依赖...
    call npm install
)

echo ✅ Frontend ready.
echo.
echo 🔥 Starting Frontend...
echo ✨ Application will be available at: http://localhost:5173
echo ✨ 应用将在 http://localhost:5173 启动
echo Press Ctrl+C to stop.
echo.

REM Open browser after a slight delay
start "" timeout /t 3 /nobreak >nul && start http://localhost:5173

REM Start Frontend (this will block)
call npm run dev

REM Cleanup
cd ..
taskkill /FI "WindowTitle eq PDF-Tool-Backend*" /T /F >nul 2>&1
