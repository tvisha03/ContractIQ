import io
import docx  # For .docx files
import PyPDF2 # For .pdf files

def extract_text_from_pdf(content: bytes) -> str:
    """Extracts text from PDF file content."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_text_from_docx(content: bytes) -> str:
    """Extracts text from DOCX file content."""
    try:
        document = docx.Document(io.BytesIO(content))
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def extract_text_from_txt(content: bytes) -> str:
    """Extracts text from TXT file content."""
    try:
        # Decodes bytes into a string, ignoring errors
        return content.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error extracting TXT: {e}")
        return ""

def extract_text(filename: str, content: bytes) -> str:
    """
    Detects the file type from the filename and calls the appropriate
    text extraction function.
    """
    if filename.lower().endswith(".pdf"):
        print("Extracting text from PDF...")
        return extract_text_from_pdf(content)
    elif filename.lower().endswith(".docx"):
        print("Extracting text from DOCX...")
        return extract_text_from_docx(content)
    elif filename.lower().endswith(".txt"):
        print("Extracting text from TXT...")
        return extract_text_from_txt(content)
    else:
        # A fallback for unknown file types, attempting to read as text
        print("Unknown file type, attempting to read as text...")
        return extract_text_from_txt(content)
