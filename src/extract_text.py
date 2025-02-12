import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_text_from_txt(txt_path):
    """Extracts text from a text file."""
    with open(txt_path, "r") as txt_file:
        text = txt_file.read()
    return text
