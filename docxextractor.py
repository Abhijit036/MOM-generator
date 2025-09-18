import io
from docx import Document

def extract_text_from_docx(file_path):
    file_path.seek(0)
    docx_file=Document(io.BytesIO(file_path.read()))
    docx_text=' '.join([p.text for p in docx_file.paragraphs])
    return docx_text