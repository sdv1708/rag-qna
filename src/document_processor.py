import PyPDF2
import docx
import csv
import os
from config import app_config
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

class DocumentProcessor:
    """Class to process documents and extract text"""

    def __init__(self):
        self.documents_path = app_config.DOCUMENTS_PATH
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from a PDF file"""
        text = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extract_text()
        
        # Extract text from images in the PDF
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
        
        return text
    
    def extract_text_from_docx(self, file_path):
        """Extract text from a DOCX file"""
        text = ""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    def extract_text_from_csv(self, file_path):
        """Extract text from a CSV file"""
        text = ""
        with open(file_path, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                text += " ".join(row)
        return text
    
    def extract_text(self, file_path):
        """Extract text from a document file"""
        if file_path.endswith(".pdf"):
            return self.extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return self.extract_text_from_docx(file_path)
        elif file_path.endswith(".csv"):
            return self.extract_text_from_csv(file_path)
        else:
            raise ValueError("Unsupported file format")
        
    def process_documents(self):
        """Process all documents in the document folder"""
        documents = []
        for file_name in os.listdir(self.documents_path):
            file_path = os.path.join(self.documents_path, file_name)
            if os.path.isfile(file_path):
                text = self.extract_text(file_path)
                documents.append({"file_name": file_name, "text": text})
        return documents