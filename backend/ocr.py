import os
import cv2
import pytesseract
from pdf2image import convert_from_path
import tempfile
from PIL import Image

# Tesseract path (Windows only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.adaptiveThreshold(gray, 255,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 31, 2)
    return gray

def ocr_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unreadable.")
    processed = preprocess_image(image)
    text = pytesseract.image_to_string(processed, lang='eng')
    return text

def ocr_scanned_pdf(pdf_path):
    text = ""
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(
            pdf_path, 
            dpi=300, 
            output_folder=path,
            poppler_path=r"C:\poppler-24.08.0\Library\bin"
        )
        for i, img in enumerate(images):
            img_path = os.path.join(path, f"page_{i}.png")
            img.save(img_path, "PNG")
            text += ocr_image(img_path) + "\n\n"
    return text

def extract_text_from_image(path):
    ext = os.path.splitext(path)[-1].lower()
    if ext in [".png", ".jpg", ".jpeg"]:
        return ocr_image(path)
    elif ext == ".pdf":
        return ocr_scanned_pdf(path)
    else:
        raise ValueError("Unsupported image file type.")
