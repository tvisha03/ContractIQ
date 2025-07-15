
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.extractor import extract_text_from_pdf
from services.classifier import classify_contract
from services.painpoints import detect_pain_points  # 👈 new import
from services.ner import extract_contract_entities
from services.summarizer import summarize_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Contract Analyzer backend is running 🚀"}

@app.post("/upload/")
async def upload_contract(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text_from_pdf(content)
    contract_type = classify_contract(text)
    pain_points, risk_score, group_risk_levels = detect_pain_points(text, contract_type)
    entities = extract_contract_entities(text)
    try:
        summary = summarize_text(text)
    except Exception as e:
        summary = f"Summarization failed: {str(e)}"

    return {
        "extracted_text": text,
        "contract_type": contract_type,
        "pain_points": pain_points,
        "entities": entities,
        "summary": summary,
        "risk_score": risk_score,
        "group_risk_levels": group_risk_levels
    }
