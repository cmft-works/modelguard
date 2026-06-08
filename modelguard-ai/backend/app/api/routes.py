import hashlib
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.entities import AIRequest, Policy
from app.schemas import AIRequestIn, AIResponseOut, PolicyIn
from app.services.policy_engine import evaluate_policy
from app.services.provider_router import call_model

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "ModelGuard AI"}

@router.post("/v1/ai/chat", response_model=AIResponseOut)
async def guarded_chat(payload: AIRequestIn, db: Session = Depends(get_db)):
    request_id = str(uuid.uuid4())
    policy_status, policy_reason, risk_score = evaluate_policy(
        db, payload.role, payload.model, payload.data_classification, payload.prompt
    )
    prompt_hash = hashlib.sha256(payload.prompt.encode()).hexdigest()

    response = None
    input_tokens = output_tokens = latency_ms = 0
    cost = 0.0
    if policy_status == "allowed":
        response, input_tokens, output_tokens, latency_ms, cost = await call_model(
            payload.provider, payload.model, payload.prompt
        )

    record = AIRequest(
        request_id=request_id,
        user_email=payload.user_email,
        department=payload.department,
        app_name=payload.app_name,
        provider=payload.provider,
        model=payload.model,
        data_classification=payload.data_classification,
        prompt_hash=prompt_hash,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=cost,
        latency_ms=latency_ms,
        risk_score=risk_score,
        policy_status=policy_status,
        policy_reason=policy_reason,
    )
    db.add(record)
    db.commit()

    return AIResponseOut(request_id=request_id, status=policy_status, response=response, cost=cost, risk_score=risk_score, policy_reason=policy_reason)

@router.get("/v1/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total_calls = db.query(func.count(AIRequest.id)).scalar() or 0
    total_cost = db.query(func.coalesce(func.sum(AIRequest.cost), 0)).scalar() or 0
    blocked = db.query(func.count(AIRequest.id)).filter(AIRequest.policy_status == "blocked").scalar() or 0
    avg_risk = db.query(func.coalesce(func.avg(AIRequest.risk_score), 0)).scalar() or 0
    return {"total_calls": total_calls, "total_cost": round(total_cost, 4), "blocked_calls": blocked, "avg_risk_score": round(avg_risk, 1)}

@router.get("/v1/dashboard/by-provider")
def by_provider(db: Session = Depends(get_db)):
    rows = db.query(AIRequest.provider, func.count(AIRequest.id), func.coalesce(func.sum(AIRequest.cost), 0)).group_by(AIRequest.provider).all()
    return [{"provider": r[0], "calls": r[1], "cost": round(r[2], 4)} for r in rows]

@router.get("/v1/dashboard/by-department")
def by_department(db: Session = Depends(get_db)):
    rows = db.query(AIRequest.department, func.count(AIRequest.id), func.coalesce(func.sum(AIRequest.cost), 0), func.max(AIRequest.risk_score)).group_by(AIRequest.department).all()
    return [{"department": r[0], "calls": r[1], "cost": round(r[2], 4), "max_risk": r[3]} for r in rows]

@router.get("/v1/requests")
def recent_requests(db: Session = Depends(get_db)):
    rows = db.query(AIRequest).order_by(AIRequest.created_at.desc()).limit(50).all()
    return [
        {
            "request_id": r.request_id,
            "user_email": r.user_email,
            "department": r.department,
            "provider": r.provider,
            "model": r.model,
            "classification": r.data_classification,
            "cost": r.cost,
            "risk_score": r.risk_score,
            "status": r.policy_status,
            "reason": r.policy_reason,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]

@router.get("/v1/policies")
def list_policies(db: Session = Depends(get_db)):
    return db.query(Policy).all()

@router.post("/v1/policies")
def create_policy(payload: PolicyIn, db: Session = Depends(get_db)):
    p = Policy(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p
