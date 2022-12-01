from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from contextlib import asynccontextmanager

@asynccontextmanager
async def get_session() -> AsyncSession:
    db_uri = "postgresql+asyncpg://postgres:password@localhost:5432/postgres"
    engine = create_async_engine(db_uri, future=True, echo=True)
    session_maker = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
