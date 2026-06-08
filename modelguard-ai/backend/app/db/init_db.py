from app.db.session import Base, engine, SessionLocal
from app.models.entities import User, Provider, Policy, AIRequest


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(Provider).first():
            db.add_all([
                Provider(name="openai", cost_per_1k_input=0.00015, cost_per_1k_output=0.0006),
                Provider(name="anthropic", cost_per_1k_input=0.003, cost_per_1k_output=0.015),
                Provider(name="gemini", cost_per_1k_input=0.0035, cost_per_1k_output=0.0105),
                Provider(name="internal", cost_per_1k_input=0.00005, cost_per_1k_output=0.00005),
            ])
        if not db.query(Policy).first():
            db.add_all([
                Policy(name="Restricted data only internal", data_classification="restricted", allowed_roles_csv="security,admin", allowed_models_csv="internal-llama", action="block", severity="critical"),
                Policy(name="Confidential data requires approved roles", data_classification="confidential", allowed_roles_csv="admin,security,finance_lead", allowed_models_csv="any", action="block", severity="high"),
            ])
        db.commit()
    finally:
        db.close()
