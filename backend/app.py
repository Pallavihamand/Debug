

from typing import Optional
import os
import shutil

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.ocr_service import extract_text
from services.prompt_builder import build_debug_prompt
from models.llava_engine import run_llava
from utils.memory_guard import has_enough_memory
from services.db_service import save_upload_record

app = FastAPI()

# Allow the DebugAI frontend on ports 3000 and 5173.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/analyze")
async def analyze(
    file: Optional[UploadFile] = File(None),
    code: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
):
    if not has_enough_memory():
        raise HTTPException(
            status_code=503,
            detail="Low system memory. Close other apps and retry.",
        )

    # Require at least source code or an uploaded image.
    if not (code and code.strip()) and file is None:
        raise HTTPException(
            status_code=400,
            detail="Please provide source code, an image, or both.",
        )

    ocr_text = ""
    file_path = None
    filename = None

    # Extract text if an image was uploaded.
    if file is not None:
        filename = os.path.basename(file.filename or "upload.png")
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ocr_text = extract_text(file_path)

    # Combine source code and OCR text into the analysis input.
    analysis_parts = []

    if language:
        analysis_parts.append(f"Programming language: {language}")

    if code and code.strip():
        analysis_parts.append(f"Source code:\n{code}")

    if ocr_text.strip():
        analysis_parts.append(f"Text extracted from screenshot:\n{ocr_text}")

    analysis_input = "\n\n".join(analysis_parts)
    prompt = build_debug_prompt(analysis_input)

    # The current engine provides rule-based preliminary analysis.
    if file_path:
        result = run_llava(file_path, prompt)
    else:
        result = run_llava("", prompt)

    # Save an upload record only when an image was provided.
    record_id = None

    if file_path is not None:
        try:
            record_id = save_upload_record(
                filename,
                file_path,
                ocr_text,
                result,
            )
        except Exception as exc:
            print(f"MongoDB save failed: {exc}")

    return {
        "analysis": result,
        "record_id": record_id,
    }
