import fitz  # PyMuPDF
import easyocr
import os
from PIL import Image
import numpy as np

reader = None

def get_ocr_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyMuPDF"""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text.strip()

def extract_text_from_image(file_path):
    """Extract text from image using EasyOCR"""
    try:
        ocr = get_ocr_reader()
        results = ocr.readtext(file_path, detail=0)
        return " ".join(results)
    except Exception as e:
        print(f"Image OCR error: {e}")
        return ""

def extract_text(file_path):
    """
    Main function - detects file type and extracts text
    Input:  file path (string)
    Output: raw extracted text (string)
    """
    if not os.path.exists(file_path):
        return ""

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
        # If PDF has no text (scanned), use OCR on images
        if len(text.strip()) < 50:
            doc = fitz.open(file_path)
            full_text = ""
            for page in doc:
                pix = page.get_pixmap()
                img_array = np.frombuffer(pix.samples, dtype=np.uint8)
                img_array = img_array.reshape(pix.height, pix.width, pix.n)
                ocr = get_ocr_reader()
                results = ocr.readtext(img_array, detail=0)
                full_text += " ".join(results) + "\n"
            doc.close()
            return full_text.strip()
        return text

    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        return extract_text_from_image(file_path)

    else:
        return ""


# ---------- TEST IT ----------
if __name__ == "__main__":
    # Change this path to any PDF on your computer to test
    test_path = "data/raw/resumes/sample_resume.pdf"
    if os.path.exists(test_path):
        text = extract_text(test_path)
        print("=== EXTRACTED TEXT ===")
        print(text[:500])
    else:
        print("Put a sample PDF at data/raw/resumes/sample_resume.pdf to test")