import pytest
from httpx import ASGITransport,AsyncClient
import pytest_asyncio
from main import app
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from db import get_db
from models import UserORM

test_engine = create_async_engine(url="test_db",pool_overflow=8,pool_size=3)
test_async_session = async_sessionmaker(bind=test_engine,expire_on_commit=False,autoflush=False,class_=AsyncSession)


@pytest_asyncio.fixture(scope="module")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(base_url="http://test",transport=transport) as client:
        yield client
        
        
@pytest_asyncio.fixture(scope="module")
async def test_db():
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection)
    try:
        user = UserORM(name="razmik",email="test_email@gmail.com",password="klara2004")
        session.add(user)
        await session.flush()
        yield session
    finally:
        await connection.aclose()
        await transaction.rollback()
        await session.aclose()
    
        

        
    
        


    


