from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.Config.Settings import Settings

engine = create_async_engine(
    Settings().database_url,
    pool_pre_ping=True,
    echo=Settings().debug,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def GetDb():
    async with AsyncSessionLocal() as session:
        yield session


async def GetReadOnlyDb():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
