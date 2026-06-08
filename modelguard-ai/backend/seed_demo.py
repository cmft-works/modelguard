import asyncio
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.schemas import AIRequestIn
from app.api.routes import guarded_chat

async def main():
    init_db()
    db = SessionLocal()
    samples = [
        AIRequestIn(user_email="cio@company.com", department="IT", role="admin", app_name="Copilot Pilot", provider="openai", model="gpt-4o-mini", prompt="Summarize public release notes", data_classification="public"),
        AIRequestIn(user_email="analyst@company.com", department="Finance", role="employee", app_name="Budget Bot", provider="anthropic", model="claude-3-5-sonnet", prompt="Analyze salary file for employee john@company.com", data_classification="confidential"),
        AIRequestIn(user_email="dev@company.com", department="Engineering", role="employee", app_name="Code Agent", provider="gemini", model="gemini-1.5-pro", prompt="Here is key sk-1234567890abcdefghijklmnop", data_classification="internal"),
        AIRequestIn(user_email="ciso@company.com", department="Security", role="security", app_name="Threat Review", provider="internal", model="internal-llama", prompt="Review restricted incident timeline", data_classification="restricted"),
    ]
    for s in samples:
        await guarded_chat(s, db)
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
