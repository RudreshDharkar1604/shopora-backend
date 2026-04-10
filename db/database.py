from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from core.config import settings

# ----------------------------------------
# PostgreSQL Connection URL
# ----------------------------------------

DATABASE_URL = (
    f"postgresql+asyncpg://postgres:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

# ----------------------------------------
# Engine
# ----------------------------------------

engine = create_async_engine(
    DATABASE_URL,
    echo=True,   # Set False in production
    pool_size=10,
    max_overflow=20
)

# ----------------------------------------
# Session Factory
# ----------------------------------------

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ----------------------------------------
# Custom Async DB Class (RAW SQL)
# ----------------------------------------

class AsyncDatabase:

    async def execute(self, query: str, params: dict = None):
        """
        Execute INSERT / UPDATE / DELETE
        """
        async with AsyncSessionLocal() as session:
            async with session.begin():
                result = await session.execute(text(query), params or {})
                return result.rowcount

    async def fetch_all(self, query: str, params: dict = None):
        """
        Return all rows as list of dict
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(text(query), params or {})
            rows = result.mappings().all()
            return [dict(row) for row in rows]

    async def fetch_one(self, query: str, params: dict = None):
        """
        Return single row
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(text(query), params or {})
            row = result.mappings().first()
            return dict(row) if row else None

    async def execute_transaction(self, queries: list):
        """
        Execute multiple queries inside transaction
        """
        async with AsyncSessionLocal() as session:
            async with session.begin():
                for q in queries:
                    await session.execute(
                        text(q["query"]),
                        q.get("params", {})
                    )

# Singleton instance
db = AsyncDatabase()

async def get_db():
    return db