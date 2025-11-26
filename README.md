# PDF Extraction Tool (PDF 提取工具)

A powerful, web-based tool for extracting text, tables, and images from PDF documents.
这是一个强大的 Web 工具，用于从 PDF 文档中提取文本、表格和图片。

## ✨ Features (功能特性)

- **📄 Text Extraction**: Converts PDF text to clean Markdown format, preserving paragraphs and layout.
  - **文本提取**: 将 PDF 文本转换为清晰的 Markdown 格式，保留段落和布局。
- **📊 Table Extraction**: Automatically detects and converts tables into Markdown tables.
  - **表格提取**: 自动检测并将表格转换为 Markdown 表格。
- **🖼️ Smart Image Extraction**: Extracts images and automatically renames them based on their captions (e.g., `Figure_1.png`).
  - **智能图片提取**: 提取图片并根据标题自动重命名（例如 `Figure_1.png`）。
- **📂 Automatic Organization**: Output folders are named after the paper title for easy management.
  - **自动整理**: 输出文件夹以论文标题命名，便于管理。
- **🎨 Premium UI**: Modern, dark-themed React frontend with drag-and-drop support.
  - **精美界面**: 现代化的暗色主题 React 前端，支持拖拽上传。

## 🛠️ Tech Stack (技术栈)

- **Backend**: Python, FastAPI, PyMuPDF (fitz), pdfplumber, Pandas
- **Frontend**: React, Vite, Vanilla CSS

## 🚀 Quick Start (一键启动)

**For macOS (Double-click / 双击运行):**
Double-click `start.command` in Finder. This will open a terminal window and automatically launch the browser.
在 Finder 中双击 `start.command`。这将打开一个终端窗口并自动启动浏览器。

**For Linux/macOS (Terminal):**
```bash
./start.sh
```
This script will automatically set up environments and start both backend and frontend.
该脚本会自动配置环境并启动后端和前端。

## 🚀 Manual Setup (手动安装)

### Prerequisites (前置要求)
- Python 3.9+
- Node.js & npm

### 1. Backend Setup (后端设置)

```bash
cd backend

# Create virtual environment (创建虚拟环境)
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies (安装依赖)
pip install -r requirements.txt

# Start server (启动服务)
# The server will run at http://localhost:8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup (前端设置)

```bash
cd frontend

# Install dependencies (安装依赖)
npm install

# Start development server (启动开发服务器)
# The app will run at http://localhost:5173
npm run dev
```

## 📖 Usage (使用说明)

1. Open the frontend URL (http://localhost:5173).
2. Drag and drop a PDF file into the upload zone.
3. Wait for the processing to complete.
4. Download the extracted Markdown text or individual images from the results panel.
5. Check the `outputs/` directory in the project root for all extracted files organized by paper title.

## 📁 Project Structure (项目结构)

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── extractor.py      # Core extraction logic (PyMuPDF + pdfplumber)
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/              # React source code
│   └── ...
├── outputs/              # Extracted results (Generated)
├── uploads/              # Uploaded temp files (Generated)
└── README.md
```

## 📄 License

MIT
