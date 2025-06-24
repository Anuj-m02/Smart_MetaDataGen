import os
import cv2
import pytesseract
from pdf2image import convert_from_path
import tempfile
from PIL import Image
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tesseract path configuration (adjust for your system)
# Windows users: Uncomment and adjust path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler path for pdf2image (Windows users: adjust path)
POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
#POPPLER_PATH = None  # Set to None for Linux/Mac, or specify path for Windows

def preprocess_image(image):
    """
    Preprocess image for better OCR results
    """
    try:
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Resize image for better OCR (increase resolution)
        height, width = gray.shape
        if width < 1000:
            scale_factor = 1000 / width
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Apply Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Apply adaptive thresholding
        gray = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
        )
        
        # Morphological operations to clean up the image
        kernel = np.ones((1, 1), np.uint8)
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        
        return gray
        
    except Exception as e:
        logger.error(f"Error in image preprocessing: {str(e)}")
        return image

def ocr_image(image_path):
    """
    Extract text from image using OCR
    """
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Preprocess image
        processed = preprocess_image(image)
        
        # OCR configuration for better results
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:,.<>?/~ '
        
        # Extract text
        text = pytesseract.image_to_string(processed, lang='eng', config=custom_config)
        
        # Clean up text
        text = text.strip()
        if not text:
            # Try with different PSM modes if no text found
            for psm in [3, 6, 8, 13]:
                try:
                    config = f'--oem 3 --psm {psm}'
                    text = pytesseract.image_to_string(processed, lang='eng', config=config)
                    if text.strip():
                        break
                except:
                    continue
        
        return text if text.strip() else "No text could be extracted from this image."
        
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        raise Exception(f"OCR failed: {str(e)}")

def ocr_scanned_pdf(pdf_path):
    """
    Extract text from scanned PDF using OCR
    """
    try:
        text = ""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info("Converting PDF pages to images...")
            
            # Convert PDF to images
            if POPPLER_PATH:
                images = convert_from_path(
                    pdf_path,
                    dpi=300,
                    output_folder=temp_dir,
                    poppler_path=POPPLER_PATH
                )
            else:
                images = convert_from_path(
                    pdf_path,
                    dpi=300,
                    output_folder=temp_dir
                )
            
            logger.info(f"Processing {len(images)} pages with OCR...")
            
            for i, img in enumerate(images):
                try:
                    # Save image temporarily
                    img_path = os.path.join(temp_dir, f"page_{i+1}.png")
                    img.save(img_path, "PNG")
                    
                    # Extract text from image
                    page_text = ocr_image(img_path)
                    
                    if page_text.strip():
                        text += f"\n--- Page {i+1} ---\n"
                        text += page_text + "\n"
                    
                    # Clean up individual image file
                    if os.path.exists(img_path):
                        os.remove(img_path)
                        
                except Exception as page_error:
                    logger.warning(f"Error processing page {i+1}: {str(page_error)}")
                    continue
        
        return text.strip() if text.strip() else "No text could be extracted from this PDF."
        
    except Exception as e:
        logger.error(f"Error in PDF OCR processing: {str(e)}")
        raise Exception(f"PDF OCR failed: {str(e)}")

def extract_text_from_image(path):
    """
    Main function to extract text from images or scanned PDFs
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    if os.path.getsize(path) == 0:
        raise ValueError("File is empty")
    
    ext = os.path.splitext(path)[-1].lower()
    
    logger.info(f"Processing {ext} file for OCR: {os.path.basename(path)}")
    
    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"]:
        return ocr_image(path)
    elif ext == ".pdf":
        return ocr_scanned_pdf(path)
    else:
        raise ValueError(f"Unsupported image file type: {ext}. Supported formats: PNG, JPG, JPEG, BMP, TIFF, PDF")

def test_ocr_setup():
    """
    Test if OCR setup is working correctly
    """
    try:
        # Test tesseract installation
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
        return True
    except Exception as e:
        logger.error(f"Tesseract test failed: {str(e)}")
        return False

# Test function
def test_image_extraction(image_path):
    """
    Test function to verify image text extraction works
    """
    try:
        text = extract_text_from_image(image_path)
        print(f"Successfully extracted {len(text)} characters")
        print(f"Preview: {text[:200]}...")
        return True
    except Exception as e:
        print(f"Extraction failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Test OCR setup
    print("OCR Module")
    print("Testing Tesseract setup...")
    if test_ocr_setup():
        print("✅ OCR setup is working correctly")
    else:
        print("❌ OCR setup needs configuration")
    
    print("Supported formats: PNG, JPG, JPEG, BMP, TIFF, PDF (scanned)")