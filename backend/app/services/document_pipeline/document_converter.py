# app/services/document_converter.py

import os
import shutil
from typing import Optional

# Make sure to install 'docx2pdf' and 'Pillow' if you want to support DOCX and image -> PDF conversion.
# pip install docx2pdf Pillow
from docx2pdf import convert as docx2pdf_convert
from PIL import Image

# Import your paths from config.py; note that here we only need RAW_DATA_PATH for conversion.
from ..config import RAW_DATA_PATH

def convert_to_pdf(input_path: str, output_dir: str) -> Optional[str]:
    """
    Converts a single file to PDF if needed.
    Returns the path to the converted PDF (or the existing PDF if no conversion was needed).
    Returns None if conversion was not possible.
    """
    filename = os.path.basename(input_path)
    file_root, file_ext = os.path.splitext(filename)
    file_ext_lower = file_ext.lower()

    # If it's already a PDF, we could simply return the path.
    if file_ext_lower == ".pdf":
        # (Optionally, you might want to skip copying if input and output are the same.)
        return os.path.join(output_dir, filename)

    # Handle DOCX files
    if file_ext_lower == ".docx":
        # docx2pdf converts and writes the PDF to the output directory.
        docx2pdf_convert(input_path, output_dir)
        pdf_filename = file_root + ".pdf"
        output_path = os.path.join(output_dir, pdf_filename)
        return output_path if os.path.exists(output_path) else None

    # Handle common image files (PNG, JPG, JPEG)
    if file_ext_lower in [".png", ".jpg", ".jpeg"]:
        output_filename = file_root + ".pdf"
        output_path = os.path.join(output_dir, output_filename)
        try:
            with Image.open(input_path) as img:
                rgb_img = img.convert('RGB')
                rgb_img.save(output_path, "PDF", resolution=100.0)
            return output_path if os.path.exists(output_path) else None
        except Exception as e:
            print(f"Error converting image '{filename}' to PDF: {e}")
            return None

    print(f"No conversion rule for file type: {file_ext_lower}. Skipping.")
    return None

def convert_all_docs_in_raw_folder():
    """
    Goes through all files in RAW_DATA_PATH.
    For files that are not PDFs, converts them to PDFs and saves the result in RAW_DATA_PATH.
    Deletes the original non-PDF file after a successful conversion.
    """
    for filename in os.listdir(RAW_DATA_PATH):
        full_path = os.path.join(RAW_DATA_PATH, filename)
        # Skip directories
        if os.path.isdir(full_path):
            continue

        file_root, file_ext = os.path.splitext(filename)
        file_ext_lower = file_ext.lower()

        if file_ext_lower == ".pdf":
            # Already a PDF – no conversion needed.
            continue

        converted_path = convert_to_pdf(full_path, RAW_DATA_PATH)
        if converted_path:
            print(f"Converted '{filename}' to PDF -> {converted_path}")
            try:
                os.remove(full_path)
                print(f"Deleted original file: {full_path}")
            except Exception as e:
                print(f"Error deleting raw file '{full_path}': {e}")
        else:
            print(f"Could not convert file: {filename}")
