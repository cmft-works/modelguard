from pydantic import BaseModel, EmailStr
from typing import Literal

class AIRequestIn(BaseModel):
    user_email: EmailStr
    department: str
    role: str = "employee"
    app_name: str
    provider: Literal["openai", "anthropic", "gemini", "internal"]
    model: str
    prompt: str
    data_classification: Literal["public", "internal", "confidential", "restricted"] = "internal"

class AIResponseOut(BaseModel):
    request_id: str
    status: str
    response: str | None = None
    cost: float
    risk_score: int
    policy_reason: str

class PolicyIn(BaseModel):
    name: str
    data_classification: str = "any"
    allowed_roles_csv: str = "any"
    allowed_models_csv: str = "any"
    action: str = "allow"
    severity: str = "low"
    enabled: bool = True
