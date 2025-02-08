# app/services/document_converter.py

import os
import shutil
from typing import Optional

# Make sure to install 'docx2pdf' and 'Pillow' (PIL) if you want to support .docx and image -> PDF conversion.
# pip install docx2pdf Pillow
from docx2pdf import convert as docx2pdf_convert
from PIL import Image

# Import your paths from config.py
# Adjust this import path based on your actual project structure
from backend.config import RAW_DATA_PATH, PROCESSED_DATA_PATH


def convert_to_pdf(input_path: str, output_dir: str) -> Optional[str]:
    """
    Converts a single file to PDF, if it's not already a PDF.
    Returns the path to the converted PDF (or the existing PDF if no conversion was needed).
    Returns None if conversion was not possible.
    """
    filename = os.path.basename(input_path)
    file_root, file_ext = os.path.splitext(filename)
    file_ext_lower = file_ext.lower()

    # If it's already PDF, just copy it to output_dir.
    if file_ext_lower == ".pdf":
        output_path = os.path.join(output_dir, filename)
        shutil.copy2(input_path, output_path)
        return output_path

    # Handle DOCX files
    if file_ext_lower == ".docx":
        # docx2pdf will create a PDF in the same folder with the same name (except for .pdf extension)
        # e.g., "document.docx" -> "document.pdf"
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
                # Convert to RGB in case it’s a mode that can’t directly be saved as PDF
                rgb_img = img.convert('RGB')
                rgb_img.save(output_path, "PDF", resolution=100.0)
            return output_path if os.path.exists(output_path) else None
        except Exception as e:
            print(f"Error converting image '{filename}' to PDF: {e}")
            return None

    # Otherwise, no conversion rule is defined here.
    print(f"No conversion rule for file type: {file_ext_lower}. Skipping.")
    return None


def convert_all_docs_in_raw_folder():
    """
    Goes through all files in RAW_DATA_PATH.
    Converts any non-PDF files to PDF if supported,
    then places them (or the original PDF) in PROCESSED_DATA_PATH.
    Finally, deletes the original file from RAW_DATA_PATH if conversion is successful.
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

    for filename in os.listdir(RAW_DATA_PATH):
        full_path = os.path.join(RAW_DATA_PATH, filename)

        # Skip directories
        if os.path.isdir(full_path):
            continue

        converted_path = convert_to_pdf(full_path, PROCESSED_DATA_PATH)
        if converted_path:
            print(f"Converted (or copied) -> {converted_path}")
            
            # Remove the original file from RAW_DATA_PATH
            try:
                os.remove(full_path)
                print(f"Deleted raw file: {full_path}")
            except Exception as e:
                print(f"Error deleting raw file '{full_path}': {e}")
        else:
            print(f"Could not convert file: {filename}")