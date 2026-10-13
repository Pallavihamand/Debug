# DebugAI — Intelligent Bug Detection and Root-Cause Analysis

**Python · FastAPI · React · TypeScript · OCR**

DebugAI is a debugging assistant designed to help developers understand programming errors. It analyzes error screenshots, extracts visible error messages using Optical Character Recognition (OCR), and provides debugging guidance through a Python-based backend.

The project provides a foundation for building a more advanced debugging system with root-cause analysis, source-code inspection, and automated fix recommendations.

## Overview

DebugAI aims to simplify debugging by helping developers identify common programming errors and understand their possible causes.

### Key Features

- Upload screenshots containing programming errors.
- Extract error messages from screenshots using Tesseract OCR.
- Process extracted error text through a backend analysis pipeline.
- Detect selected common error types using predefined rules.
- Display analysis results through a React-based user interface.
- Provide a modular backend that can be extended with additional debugging capabilities.

**Current implementation:** The fallback analyzer uses predefined rules to identify selected error patterns. It does not currently provide active LLM-based analysis. Results should be treated as debugging guidance rather than guaranteed fixes.

## Architecture Overview

```text
React Frontend
      |
      | HTTP multipart/form-data
      v
FastAPI Backend
      |
      v
Image Upload and Processing
      |
      v
Tesseract OCR
      |
      v
Prompt Builder
      |
      v
Rule-Based Error Analysis
      |
      v
Analysis Response
      |
      v
React Results Interface
```

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend | Python, FastAPI, Uvicorn |
| Text Extraction | Tesseract OCR, pytesseract |
| Analysis | Python-based rules and debugging heuristics |
| Development Tools | Git, npm, Python virtual environment |

## Project Structure

```text
DebugAI/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models/
│   │   └── llava_engine.py
│   ├── services/
│   │   ├── db_service.py
│   │   ├── image_service.py
│   │   ├── ocr_service.py
│   │   ├── prompt_builder.py
│   │   └── db_service.py
│   └── utils/
│       └── memory_guard.py
├── docs/
│   └── screenshots/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

## Prerequisites

Install the following software before running DebugAI:

- Python 3.10 or a compatible version supported by the dependencies.
- Node.js and npm.
- Tesseract OCR.
- Git.

Python dependencies are listed in `backend/requirements.txt`.

### Installing Tesseract OCR

Install Tesseract OCR on your operating system.

On Windows, ensure that the Tesseract executable is available through your system PATH. If it is installed in a non-standard location, configure the executable path in the OCR service.

## Backend Setup

Open PowerShell and navigate to the backend directory:

```powershell
cd C:\Users\PUNAM\DebugAI\backend
```

Create a virtual environment if one does not already exist:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the FastAPI development server:

```powershell
python -m uvicorn app:app --reload
```

The backend should be accessible at:

- **API:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs

Keep this terminal open while using the frontend.

## Frontend Setup

Open a second PowerShell terminal and navigate to the frontend directory:

```powershell
cd C:\Users\PUNAM\DebugAI\frontend
```

Install the frontend dependencies:

```powershell
npm install
```

Start the Vite development server:

```powershell
npm run dev
```

Open the URL displayed in the terminal, usually:

http://localhost:5173

The frontend provides an interface for uploading error screenshots and viewing analysis results.

## How It Works

1. The user uploads a screenshot containing a programming error.
2. The frontend sends the image and optional source-code and programming-language fields to the FastAPI `/analyze` endpoint.
3. The backend processes the uploaded image.
4. Tesseract OCR extracts visible text from the screenshot.
5. The prompt-building service prepares the extracted information for analysis.
6. The fallback analyzer checks the available text against selected error patterns.
7. The backend returns the analysis response to the frontend.
8. The frontend displays the result to the user.

OCR quality depends on screenshot clarity, text size, and image quality. Unrecognized errors may receive generic debugging guidance.

## API Endpoint

### `POST /analyze`

The `/analyze` endpoint accepts a multipart form request containing an image file and optional source-code and programming-language fields.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "file=@error_screenshot.png" \
  -F "code=print(unknown_variable)" \
  -F "language=python"
```

You can inspect the endpoint's required fields and test requests through the interactive API documentation:

http://127.0.0.1:8000/docs

**Current limitation:** Although the request may contain source code and a programming language, the current analysis flow primarily uses text extracted from the uploaded screenshot. Full source-code-aware debugging requires further implementation.

## Current Limitations

- The fallback analyzer uses predefined rules instead of an active LLM.
- Only selected error patterns are recognized.
- OCR errors can affect the quality of the analysis.
- Unfamiliar errors may produce generic suggestions.
- Source-code-aware analysis is not yet fully integrated.
- Automated code correction and test-case generation are future enhancements.
- Database persistence should be treated as optional until its configuration and behavior have been verified.

## Future Enhancements

- Integrate an LLM for more detailed root-cause analysis.
- Improve source-code analysis alongside screenshot text extraction.
- Return structured results containing error type, root cause, severity, and recommended fixes.
- Add automated fix recommendations.
- Generate test cases for identified errors.
- Expand error detection to support Python, Java, and additional programming languages.
- Add persistent debugging history.
- Improve automated testing and frontend-backend integration tests.

## Testing the Application

Before demonstrating DebugAI:

1. Start the backend server.
2. Open `http://127.0.0.1:8000/docs`.
3. Upload a test screenshot containing a recognizable programming error.
4. Verify that OCR extracts the expected text.
5. Review the returned analysis.
6. Start the frontend and repeat the test through the user interface.

## License

This project is intended for **educational and portfolio purposes**.

