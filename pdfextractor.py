from pypdf import PdfReader

def text_extractor(file):
    # file is a BytesIO object from Streamlit uploader
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text
