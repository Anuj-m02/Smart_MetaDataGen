from docx import Document
import fitz  # PyMuPDF
import os
import pytesseract
from PIL import Image
import io

# Optional: Configure path to tesseract.exe (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(path):
    text = ""
    ocr_text = ""
    doc = fitz.open(path)
    for page in doc:
        # Extract visible text
        text += page.get_text()

        # Render page as image
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Run OCR on image
        ocr_text += pytesseract.image_to_string(img, lang='eng')

    return text + "\n\n[OCR-Extracted Text]\n" + ocr_text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(path):
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type.")
