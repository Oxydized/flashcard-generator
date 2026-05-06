from docx import Document
from pypdf import PdfReader

def load_file_text(file_name):
    # Handles TXT file type
    if file_name.lower().endswith(".txt"):
        with open(file_name, "r", encoding="utf8") as file:
            return file.readlines()
    
    # Handles DOCX file type
    elif file_name.lower().endswith(".docx"):
        document = Document(file_name)
        return [paragraph.text for paragraph in document.paragraphs]
    
    # Handles PDF file type
    elif file_name.lower().endswith(".pdf"):
        reader = PdfReader(file_name)
        lines = []

        for page in reader.pages:
            text = page.extract_text()
            if text: 
                lines.extend(text.splitlines())

        return lines
        
    print("Unsupported file type. Please use a .txt or .docx file for now")
    return None