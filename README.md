# 📄 Mars_MetaData

**Mars_MetaData** is a lightweight and modular Python project to extract, analyze, and generate semantic metadata from documents like PDFs, DOCX files, and images using OCR. It supports resume/CV analysis, academic papers, and general documents.

---

## 🚀 Features

- 🔍 Extracts text from PDFs, Word docs, and image-based documents (OCR).
- 🧠 Generates structured metadata using LLMs (OpenAI/Gemini-compatible).
- 📊 Supports metadata categories like keywords, sentiment, named entities, document sections, etc.
- 📁 Easily integrable into larger document understanding pipelines.
- ✅ Jupyter notebook friendly.

---

## 🗂️ Project Structure

Mars_MetaData/
│
├── app/
│ └── temp/ # Folder for temporary document uploads
│
├── backend/
│ ├── extractor.py # Text extractor (PDF, DOCX)
│ ├── ocr.py # OCR handler using Tesseract + cv2
│ └── metadata_gen.py # Calls LLM and generates structured metadata
│
├── notebook/
│ └── Mars_Metadata_Notebook.ipynb # Interactive Jupyter notebook interface
│
├── README.md
└── requirements.txt

