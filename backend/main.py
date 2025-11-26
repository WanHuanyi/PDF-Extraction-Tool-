from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from pathlib import Path
from .extractor import extract_content

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    session_id = str(uuid.uuid4())
    session_upload_dir = UPLOAD_DIR / session_id
    session_output_dir = OUTPUT_DIR / session_id
    session_upload_dir.mkdir(exist_ok=True)
    session_output_dir.mkdir(exist_ok=True)
    
    file_path = session_upload_dir / file.filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        result_files, title = extract_content(str(file_path), str(session_output_dir))
        
        # Sanitize title for folder name
        safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip()
        safe_title = safe_title.replace(' ', '_')
        if not safe_title:
            safe_title = "Untitled"
            
        # Create new session ID based on title (and UUID to ensure uniqueness if needed, 
        # but user wants readable names. Let's try Title first, append UUID if exists)
        new_session_id = safe_title
        new_output_dir = OUTPUT_DIR / new_session_id
        
        # Handle collision
        counter = 1
        while new_output_dir.exists():
            new_session_id = f"{safe_title}_{counter}"
            new_output_dir = OUTPUT_DIR / new_session_id
            counter += 1
            
        # Rename output directory
        # Note: We are not renaming the upload directory, that stays as UUID or we can rename it too.
        # For simplicity, let's just rename the output directory which is what the user sees/downloads from.
        os.rename(session_output_dir, new_output_dir)
        
        return {"status": "success", "session_id": new_session_id, "files": result_files}
    except Exception as e:
        # Cleanup on failure could be added here
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{session_id}/{filename}")
async def download_file(session_id: str, filename: str):
    file_path = OUTPUT_DIR / session_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
