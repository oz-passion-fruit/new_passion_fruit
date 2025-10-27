import os
from tortoise import Tortoise, run_async
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

async def init_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["app.db.models.user", "app.db.models.question", "app.db.models.diary", "app.db.models.quotes"]}
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    run_async(init_db())
