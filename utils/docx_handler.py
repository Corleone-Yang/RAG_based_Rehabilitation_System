from docx import Document
from io import BytesIO

def extract_text_from_docx(file_content):
    document = Document(BytesIO(file_content))
    doc_text = []
    for paragraph in document.paragraphs:
        doc_text.append(paragraph.text)
    return '\n'.join(doc_text)

