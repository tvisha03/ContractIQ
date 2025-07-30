from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Define the structure for a single Pain Point
class PainPoint(BaseModel):
    text: str
    sentence: str
    risk_level: str
    explanation: str

# Define the structure for a single Entity
class Entity(BaseModel):
    text: str
    label: str

# This is the main model for our API's response
class AnalysisResult(BaseModel):
    extracted_text: str
    contract_type: str
    pain_points: List[PainPoint]
    entities: List[Entity]
    summary: str
    risk_score: float  # Using float for scores is more flexible
    group_risk_levels: Dict[str, Any]

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
