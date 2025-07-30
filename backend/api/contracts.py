from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import AnalysisResult, User as UserSchema
from models.schema import User as UserModel, Contract as ContractModel
from services import extractor, classifier, painpoints, ner, summarizer
from .auth import get_current_user
# from database import get_db  # We'll add this when database is ready

router = APIRouter()

@router.post("/upload/", response_model=AnalysisResult, status_code=status.HTTP_201_CREATED)
async def upload_and_analyze_contract(
    file: UploadFile = File(...), 
    # db: AsyncSession = Depends(get_db),  # Uncomment when database is ready
    current_user: UserSchema = Depends(get_current_user)
):
    content = await file.read()

    # --- 1. Perform Analysis ---
    text = extractor.extract_text(file.filename, content)
    if not text:
        raise HTTPException(status_code=400, detail="Failed to extract text from the document.")

    contract_type = classifier.classify_contract(text)
    pain_points, risk_score, group_risk_levels = painpoints.detect_pain_points(text, contract_type)
    entities = ner.extract_contract_entities(text)
    
    try:
        summary = summarizer.summarize_text(text)
    except Exception as e:
        summary = f"Summarization failed: {str(e)}"

    # --- 2. Save Contract and Analysis to DB ---
    # TODO: Uncomment when database is ready
    # new_contract = ContractModel(
    #     filename=file.filename,
    #     original_text=text,
    #     contract_type=contract_type,
    #     summary=summary,
    #     risk_score=risk_score,
    #     user_id=current_user.id  # Link to the logged-in user
    # )
    # db.add(new_contract)
    # await db.commit()
    # await db.refresh(new_contract)

    # --- 3. Return the Analysis Result ---
    # Note: We are not saving pain points and entities to the DB in this model
    # but we still return them from the analysis.
    return AnalysisResult(
        extracted_text=text,
        contract_type=contract_type,
        pain_points=pain_points,
        entities=entities,
        summary=summary,
        risk_score=risk_score,
        group_risk_levels=group_risk_levels
    )
