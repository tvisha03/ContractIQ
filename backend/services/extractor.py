import fitz  # PyMuPDF
import tempfile

def extract_text_from_pdf(content: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    full_text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return full_text
