import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
import pytest_asyncio
from models import UserORM
from db import get_db
from main import app
from httpx import ASGITransport,AsyncClient


@pytest.mark.asycio
async def test_get_user_name():
    amock=AsyncMock(return_value = UserORM(id=1,username="Razmik",age=20))
    with patch(target="service.get_user",new=amock):
        result = await get_user_name(1)  # type: ignore
        assert result == "Razmik"
    
    amock.assert_called_once()
        

@pytest.mark.asyncio
async def test_get_user_value():
    amock = AsyncMock(return_value=None)
    with patch("app.service.get_user", new=amock):
        with pytest.raises(ValueError,"User not found"):
            await get_user_name(1) # type: ignore
    amock.assert_called_once()
    
@pytest.mark.asyncio 
async def test_get_user_side():
    amock = AsyncMock(side_effect=ConnectionError("DB unavailable"))
    with patch("app.service.get_user", new=amock):
        with pytest.raises(ConnectionError,"DB unavailable"):
            await get_user_name(1) # type: ignore
    amock.assert_called_once()


@pytest.mark.asyncio    
async def test_age_of_value():
    amock = AsyncMock()
    amock.return_value = 18
    with patch("service.create_user",amock):
         with pytest.raises(ValueError, match="User must be 18+"):
            await get_user_name(1) # type: ignore  
    amock.assert_not_awaited()
    
@pytest.mark.asyncio    
async def test_access_reg_user():
    amock = AsyncMock()
    amock.user = UserORM(id=5, name="Alex", age=25)
    with patch("service.create_user",amock):
        result = await get_user_name(1) # type: ignore 
        result == "Alex"
    amock.assert_called_once()
    

@pytest.mark.parametrize(
    "age",
    [17,
     18,
     20,
     50]
)


@pytest.mark.asyncio
async def test_age_verify(age):
    amock = AsyncMock()
    amock.age = age
    with patch("service.create_user",amock):
        await get_user_name(1) # type: ignore 
         


test_engine = create_async_engine(url="test_db",pool_overflow=8,pool_size=3)
test_async_session = async_sessionmaker(bind=test_engine,expire_on_commit=False,autoflush=False,class_=AsyncSession)

async def get__test_db():
    async with test_async_session() as session:
        yield session

@pytest_asyncio.fixture
async def session():
    transport = ASGITransport(app=app)
    app.dependency_overrides[get_db] = get__test_db
    async with AsyncClient(transport=transport,base_url="http://test") as client:
        yield client
    
    
    
    
        
        
    
    
