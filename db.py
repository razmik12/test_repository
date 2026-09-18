from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession


test_engine = create_async_engine(url="test_db",pool_overflow=8,pool_size=3)
test_async_session = async_sessionmaker(bind=test_engine,expire_on_commit=False,autoflush=False,class_=AsyncSession)



async def get_db():
    async with test_async_session() as session:
        yield session