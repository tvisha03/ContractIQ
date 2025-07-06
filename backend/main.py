from fastapi import FastAPI, UploadFile, File
from services.extractor import extract_text_from_pdf
from services.classifier import classify_contract
from services.painpoints import detect_pain_points  # 👈 new import
from services.ner import extract_contract_entities


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Contract Analyzer backend is running 🚀"}

@app.post("/upload/")
async def upload_contract(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(content)
    contract_type = classify_contract(text)
    pain_points = detect_pain_points(text, contract_type)
    entities = extract_contract_entities(text)

    return {
        "extracted_text": text,
        "contract_type": contract_type,
        "pain_points": pain_points,
        "entities": entities
    }
