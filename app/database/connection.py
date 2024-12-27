from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config_reader import config

engine = create_async_engine(url=config.DB_URL, pool_pre_ping=True, pool_size=10,
                             max_overflow=200)
session = async_sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False,
                             expire_on_commit=False)
