from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from nobrain_bot.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=False)

async_session = sessionmaker[AsyncSession](
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()
