import re
from sqlalchemy.orm import Session
from app.models.entities import Policy

SENSITIVE_PATTERNS = {
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "secret_key": r"\b(sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16})\b",
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
}

PUBLIC_MODEL_PREFIXES = ("gpt", "claude", "gemini")


def score_prompt_risk(prompt: str, data_classification: str) -> tuple[int, list[str]]:
    reasons = []
    score = {"public": 5, "internal": 20, "confidential": 55, "restricted": 80}.get(data_classification, 20)
    for name, pattern in SENSITIVE_PATTERNS.items():
        if re.search(pattern, prompt, flags=re.IGNORECASE):
            score += 20
            reasons.append(f"Detected {name}")
    return min(score, 100), reasons


def evaluate_policy(db: Session, role: str, model: str, data_classification: str, prompt: str) -> tuple[str, str, int]:
    risk, risk_reasons = score_prompt_risk(prompt, data_classification)

    if data_classification == "restricted" and model.lower().startswith(PUBLIC_MODEL_PREFIXES):
        return "blocked", "Restricted data cannot be sent to public models", risk

    if risk >= 90:
        return "blocked", "; ".join(risk_reasons) or "Risk score exceeded threshold", risk

    policies = db.query(Policy).filter(Policy.enabled == True).all()
    for p in policies:
        class_match = p.data_classification in ("any", data_classification)
        roles = [x.strip().lower() for x in p.allowed_roles_csv.split(",")]
        models = [x.strip().lower() for x in p.allowed_models_csv.split(",")]
        role_ok = "any" in roles or role.lower() in roles
        model_ok = "any" in models or model.lower() in models
        if class_match and (not role_ok or not model_ok):
            return "blocked" if p.action == "block" else "review", f"Policy '{p.name}' matched", risk

    return "allowed", "; ".join(risk_reasons) if risk_reasons else "Policy checks passed", risk
