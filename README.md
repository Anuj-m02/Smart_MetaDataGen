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
```
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

```

---

## 🧠 Modules Explained

### 📄 extractor.py
- Handles reading text from:
  - `.pdf` files (using PyMuPDF)
  - `.docx` files (using python-docx)
- Automatically detects format and delegates extraction accordingly.

### 🧾 ocr.py
- Uses `cv2`, `pytesseract`, and `pdf2image` to:
  - Convert scanned images to text.
  - OCR PDFs with non-searchable content.

### 🧠 metadata_gen.py
- Takes extracted text and queries an LLM (Llama) to:
  - Generate metadata in JSON format.
  - Extract structured information: title, author, keywords, sections, sentiment, etc.

---

## 🧪 How to Use (Jupyter Notebook)

1. Open the notebook at: `notebook/Mars_Metadata_Notebook.ipynb`
2. Upload your file to `app/temp/`
3. Modify `file_path` in the notebook to point to your document.
4. Run each cell:
   - Extracts text (PDF/DOCX/Image)
   - Generates metadata
   - Displays JSON output and table view

---

## 📦 Installation

```bash
# Clone this repo
git clone https://github.com/Anuj-m02/Smart_MetaDataGen.git
cd Smart_MetaDataGen

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
🔧 Requirements
Install via `pip install -r requirements.txt`
```
python-docx
pytesseract
opencv-python
pdf2image
PyMuPDF
openai
ipython
```
📌 Note
Ensure Tesseract OCR is installed on your machine.

Windows: https://github.com/tesseract-ocr/tesseract/wiki

Linux/macOS: `sudo apt install tesseract-ocr`

Configure the path in `ocr.py` if needed:
```
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
